#!/usr/bin/env python3


def check_file(fname, print_fname=False):
    fail = 0
    with open(fname, 'rb') as f:
        for n, line in enumerate(f):
            try:
                line.decode('ascii')
            except UnicodeDecodeError as e:
                line = line.decode('utf-8')
                prefix = '{:s}:{:d}'.format(fname, n+1) if print_fname else str(n+1)
                ndigits_prefix = len(prefix)
                print('{:s}: {:s}'.format(prefix, line.rstrip('\n')))
                print(' '*(ndigits_prefix + 2 + e.start) + '^-- {}'.format(e))
                fail += 1
    return fail


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('fnames', metavar='FILE', nargs='+')
    args = parser.parse_args()

    print_fname = len(args.fnames) > 1
    failure = False
    for fname in args.fnames:
        status = check_file(fname, print_fname=print_fname)
        if(status != 0):
            failure = True
    return failure

if __name__ == '__main__':
    exit(main())
