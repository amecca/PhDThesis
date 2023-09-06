AN=thesis
outputdir=output
sources=$(shell find . -type d -name utils -prune -o -type d -name $(outputdir) -prune -o -type f -name "*.tex" -print)
bibliography=$(shell find . -type d -name utils -prune -o -type d -name $(outputdir) -prune -o -type f -name "*.bib" -print)
LATEX=latexmk
LATEXOPT=--pdf --pdflatex="pdflatex -interaction=nonstopmode -file-line-error" --output-directory=$(outputdir) --use-make --bibtex --quiet

.PHONY: $(AN)
$(AN): $(outputdir)/$(AN).pdf ;

# Do not search for rules to make a tex file
%.tex: ;

$(outputdir)/$(AN).pdf: $(sources) $(bibliography)
	$(LATEX) $(LATEXOPT) $(AN).tex

.PHONY: clean
clean:
	$(LATEX) -C --output-directory=$(outputdir)

.PHONY: undefined-refs
undefined-refs:
	-./scripts/checkcites.lua --undefined $(outputdir)/$(AN).aux

.PHONY: unused-refs
unused-refs:
	-./scripts/checkcites.lua --unused $(outputdir)/$(AN).aux

.PHONY: summary-log
summary-log:
	./scripts/summary-log.sh $(outputdir)/$(AN).log
