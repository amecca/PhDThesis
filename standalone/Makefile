SRCDIR=.
OBJDIR=../Figures/Feynman
PDF=pdflatex
PDFOPT=-interaction=batchmode # -aux-directory=. # pdflatex does not support it
SOURCES=$(shell find $(SRCDIR) -maxdepth 1 -type f -name "*.tex")
OBJECTS=$(patsubst $(SRCDIR)/%.tex,$(OBJDIR)/%.pdf,$(SOURCES))

.PHONY: all
all: $(OBJDIR) $(OBJECTS)

$(OBJDIR):
	mkdir -p $(OBJDIR)

Makefile: ;
%.tex: ;

$(OBJDIR)/%.pdf: $(SRCDIR)/%.tex
	TEXINPUTS=".:../lib:" \
	$(PDF) $(PDFOPT) -output-directory=$(OBJDIR) $<

.PHONY: clean
clean:
	-rm $(OBJDIR)/*.aux $(OBJDIR)/*.log $(OBJECTS)
