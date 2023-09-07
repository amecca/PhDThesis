# PhD Thesis

### Compilation instructions
Run make with default target to generate the PDF:
```
make
```
It uses latexmk to solve the maze of compilation steps required by LaTeX.

A script from https://github.com/islandoftex/checkcites is provided to check the correctness of the references in the project.
I added a couple of phony targets in the Makefile to run it with the correct options:
```
make undefined-refs
```
```
make unused-refs
```
There is also a script to print only erors and warnings from the (verbose) output from pdflatex:
```
make summary-log
```

### Folder structure
```
.                
└── Thesis folder            # The folder containing this repository
    ├── thesis.tex           # The main file
    ├── head                 # place for the tex files of the introductory part
        ├── frontPage.tex
        ├── dedication.tex
        └── abstract.tex
    ├── body                 # place for the tex files of the body part
        ├── chapter1.tex
        ├── chapter2.tex
        ├── ...
        └── conclusions.tex
    ├── tail                 # place for the tex files for the final part
        ├── appendix1.tex
        ├── acknowledgments.tex
        ├── bibliography.tex
        └── ...
    ├── scripts              # utilities
    ├── images               # Will probably have sub-folders
    └── bibliography
        └── bibThesis.bib
```
