SRCDIR=.
OBJDIR=../Figures
PDF=pdflatex
PDFOPT=-interaction=batchmode -aux-directory=.
SOURCES=$(shell find $(SRCDIR) -maxdepth 1 -type f -name "*.tex")
OBJECTS=$(patsubst $(SRCDIR)/%.tex,$(OBJDIR)/%.pdf,$(SOURCES))

.PHONY: all
all: $(OBJECTS)

Makefile: ;
%.tex: ;

$(OBJDIR)/%.pdf: $(SRCDIR)/%.tex
	$(PDF) $(PDFOPT) -output-directory=$(OBJDIR) $<

.PHONY: clean
clean:
	-rm *.aux *.log $(OBJECTS)
