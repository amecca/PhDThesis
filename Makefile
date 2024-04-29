AN=thesis
outputdir=output
sources=$(shell find . -type d -name utils -prune -o -type d -name $(outputdir) -prune -o -type f -name "*.tex" -print)
bibliography=$(shell find . -type d -name utils -prune -o -type d -name $(outputdir) -prune -o -type f -name "*.bib" -print)
LATEX=latexmk
LATEXOPT=--pdf --pdflatex="pdflatex -interaction=nonstopmode -file-line-error -output-directory $(outputdir)" --output-directory=$(outputdir) --aux-directory=$(outputdir) --use-make --bibtex --quiet

.PHONY: $(AN)
$(AN): $(outputdir)/$(AN).pdf ;

# Do not search for rules to make a tex file
%.tex: ;
%.sty: ;

$(outputdir)/body:
	mkdir -p $@

$(outputdir)/head:
	mkdir -p $@

$(outputdir)/$(AN).pdf: $(sources) $(bibliography) bibliography/CMS_publications_pub.bib $(outputdir)/head $(outputdir)/body
	$(MAKE) -C standalone
	$(LATEX) $(LATEXOPT) $(AN).tex

bibliography/CMS_publications_pub.bib:
	wget -O $@ https://cms-results.web.cern.ch/cms-results/public-results/publications/CMS/CMS_publications_pub.bib

.PHONY: clean
clean:
	$(LATEX) -C --output-directory=$(outputdir) --aux-directory=$(outputdir)
	-rm $(outputdir)/head/*aux
	-rm $(outputdir)/body/*aux

.PHONY: cleanall
cleanall: clean
	$(MAKE) -C standalone clean

.PHONY: undefined-refs
undefined-refs:
	-./scripts/checkcites.lua --undefined $(outputdir)/$(AN).aux

.PHONY: unused-refs
unused-refs:
	-./scripts/checkcites.lua --unused $(outputdir)/$(AN).aux

.PHONY: summary-log
summary-log:
	./scripts/summary-log.sh $(outputdir)/$(AN).log
