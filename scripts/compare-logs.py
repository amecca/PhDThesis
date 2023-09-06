#!/usr/bin/env python3

from argparse import ArgumentParser
import re
from subprocess import run
from tempfile import NamedTemporaryFile

import ROOT

class Colour:
    s_terminator = '\033[00m'
    s_white      = '\033[0;07m'
    s_red        = '\033[0;31m'    
    s_green      = '\033[0;32m'    
    s_yellow     = '\033[0;33m'    
    s_blue       = '\033[0;34m'    
    s_violet     = '\033[0;35m'    
    s_important  = '\033[0;41m'    
    s_ok         = '\033[0;42m'    
    s_warn       = '\033[0;43m'    
    s_evidence   = '\033[1;91;103m'

    def white    (st): return Colour.s_white     + str(st) + Colour.s_terminator
    def red      (st): return Colour.s_red       + str(st) + Colour.s_terminator
    def green    (st): return Colour.s_green     + str(st) + Colour.s_terminator
    def yellow   (st): return Colour.s_yellow    + str(st) + Colour.s_terminator
    def blue     (st): return Colour.s_blue      + str(st) + Colour.s_terminator
    def violet   (st): return Colour.s_violet    + str(st) + Colour.s_terminator
    def important(st): return Colour.s_important + str(st) + Colour.s_terminator
    def ok       (st): return Colour.s_ok        + str(st) + Colour.s_terminator
    def warn     (st): return Colour.s_warn      + str(st) + Colour.s_terminator
    def evidence (st): return Colour.s_evidence  + str(st) + Colour.s_terminator


def diff_full(keys1, keys2, **kwargs):
    with NamedTemporaryFile(mode='w') as temp1, NamedTemporaryFile(mode='w') as temp2:
        temp1.write('\n'.join(sorted(keys1))+'\n')
        temp2.write('\n'.join(sorted(keys2))+'\n')
        diff_proc = run(['diff', '--minimal', temp1.name, temp2.name], capture_output=True, encoding='utf-8')
        if(diff_proc.returncode == 2):
            print('ERROR in diff')
            exit(2)
        print( diff_proc.stdout )


def get_fmt(a, b, tot):
    return '{:%dd}/{:%dd} ({:5.1f}) %%' % (
        max(
            len(str(a)),
            len(str(b))
        ),
        len(str(tot)),
    )


def print_missing(missing1, missing2, common, **kwargs):
    print_every_plot        = kwargs['verbosity'] >= 2
    print_every_plot_common = kwargs['verbosity'] >= 4
    total = int( kwargs['total'] )
    fmt = get_fmt( len(missing1), len(missing2), total )

    if(len(missing1) > 0):
        print( Colour.red('Missing'), 'from 1:', fmt.format(len(missing1), total, 100*len(missing1)/total) )
        if(print_every_plot):
            for plot in sorted(missing1):
                print(plot.rstrip('\n'))
            print()

    if(len(missing2) > 0):
        print( Colour.red('Missing'), 'from 2:', fmt.format(len(missing2), total, 100*len(missing2)/total) )
        if(print_every_plot):
            for plot in sorted(missing2):
                print(plot.rstrip('\n'))
            print()

    if(len(common) > 0): # and ((len(missing1) > 0 or len(missing2) > 0) or kwargs['verbosity'] >= 2)):
        print( Colour.green('Common'), 'in 1, 2:', fmt.format(len(common)  , total, 100*len(common  )/total) )
        if(print_every_plot_common):
            for plot in sorted(common):
                print(plot.rstrip('\n'))
            print()


def print_content_status(content_status):
    ok  = content_status['OK']
    bad = content_status['BAD']
    tot = ok + bad
    
    fmt = get_fmt(ok, bad, tot)

    print(Colour.green('Same content')+'  :', fmt.format(ok , tot, 100 * ok /tot))
    if(bad == 0):
        return
    print(Colour.red  ('Different')+'     :', fmt.format(bad, tot, 100 * bad/tot))


def diff_set(keys1, keys2, **kwargs):
    missing1 = keys2 - keys1
    missing2 = keys1 - keys2
    common = kwargs.get('common', keys1 & keys2)

    print_missing(missing1, missing2, common, total=len(keys1|keys2), **kwargs)


def get_messages_from_file(fname, error_patterns):
    messages = {}
    with open(fname) as f:
        current = None
        for line in f.readlines():
            if(current is None):
                for key, regex in error_patterns.items():
                    if(regex.search(line)):
                        current = {'key': key, 'message': line}
            else:
                # Check if the message has ended:
                if(len(line) <= 1):
                    messages.setdefault(current['key'],
                                                 set()).add(
                                                 # list()).append(
                                                     current['message'])
                    current = None
                else:
                    current['message'] += line
    return messages


def main():
    parser = ArgumentParser('Compare the error and warnings of two log files')

    parser.add_argument('file1', metavar='FILE1')
    parser.add_argument('file2', metavar='FILE2')
    parser.add_argument('--diff', action='store_true', help='use diff to compare the sorted lists of keys')
    parser.add_argument('-v', '--verbose', dest='verbosity',
                        action='count', default=1,
                        help='increase verbosity')
    parser.add_argument('--verbosity', type=int,
                        metavar='LEVEL',
                        help='set verbosity')
    parser.add_argument('-q', '--quiet', dest='verbosity',
                        action='store_const', const=0,
                        help='set verbose to minimum')

    args = parser.parse_args()

    error_patterns = {'Errors': '^!', 'LaTeX warnings': 'LaTeX(?= Warning)', 'Package warnings': '(?<=Package )[^ ]+(?= Warning)'}
    rest_of_message = '' #TODO

    for key, val in error_patterns.items():
        error_patterns[key] = re.compile(val)

    messages_1 = get_messages_from_file(args.file1, error_patterns)
    messages_2 = get_messages_from_file(args.file2, error_patterns)

    for key in error_patterns:
        if(messages_1.get(key) or messages_2.get(key)):
            print(Colour.red(key))
            diff_set(messages_1.get(key, set()), messages_2.get(key, set()), verbosity=args.verbosity)

    return 0  #TEMP

    with TFileContext(args.file1, 'READ') as tf:
        keys1 = { k.GetName() for k in tf.GetListOfKeys() }
    
    with TFileContext(args.file2, 'READ') as tf:
        keys2 = { k.GetName() for k in tf.GetListOfKeys() }
    
        
    if(args.plot is not None):
        plot_re = re.compile(args.plot)
        matching_keys = { k for k in keys1|keys2 if plot_re.search(k)}
        if(len(matching_keys) == 0):
            print('ERROR: no keys matching', plot_re.pattern)
            exit(1)
        
        missing_keys = {1:matching_keys - keys1, 2: matching_keys - keys2}
        common_keys = matching_keys & keys1 & keys2
    
        print('Plots matching regex', plot_re.pattern, '=', len(matching_keys))
        print()
    
        content_status = {'OK': 0, 'BAD': 0}
        with TFileContext(args.file1, 'READ') as tf1, TFileContext(args.file2, 'READ') as tf2:
            for plot in sorted(common_keys):
                h1 = tf1.Get(plot)
                h2 = tf2.Get(plot)
                assert h1 and h2, 'Unable to retrieve both plots "'+plot+'" from the files'
                ok_content = compare_plot(h1, h2, plot, verbosity=args.verbosity)
                if(ok_content): content_status['OK']  += 1
                else          : content_status['BAD'] += 1
    
        print_missing(missing_keys[1], missing_keys[2], common=common_keys, verbosity=args.verbosity, total=len(matching_keys))
        print()
        print_content_status(content_status)
    
    else:
        if  (args.diff):
            diff_full(keys1, keys2, verbosity=args.verbosity)
        else:
            diff_set(keys1, keys2, verbosity=args.verbosity)


if __name__ == '__main__':
    main()
