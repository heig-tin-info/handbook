# The two books `texsmith site build` writes, one folder per book of
# `mkdocs.yml`.
BOOKS = build/book/book.pdf build/tools/tools.pdf

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	RUNCMD = PYTHONBREAKPOINT=ipdb.set_trace uv run
else
	RUNCMD = uv run
endif

# The site is built with Zensical: the generated assets first (Zensical
# empties the site directory and caches pages, so nothing Python writes during
# a build survives), then the site, then the two books. The search index needs
# no step of its own: a page's index entries are its tags, and the extension
# writes them while the page renders. `make zensical` is the whole chain, the
# one CI runs before publishing.
all: zensical

zensical:
	$(RUNCMD) texsmith site assets mkdocs.yml
	$(RUNCMD) zensical build -f mkdocs.yml
	$(RUNCMD) texsmith site build mkdocs.yml

serve:
	$(RUNCMD) texsmith site assets mkdocs.yml
	$(RUNCMD) zensical serve -f mkdocs.yml

# MkDocs, which no longer publishes anything: CI publishes the Zensical site.
mkdocs:
	$(RUNCMD) mkdocs build

serve-mkdocs:
	$(RUNCMD) mkdocs serve

servefast:
	$(RUNCMD) mkdocs serve --dirty

uv.lock: pyproject.toml
	uv lock

build: zensical

# The books compressed for print, the ones a release attaches.
optimize: $(BOOKS:.pdf=-print.pdf)

%-print.pdf: %.pdf
	gs -sDEVICE=pdfwrite -dPDFSETTINGS=/printer \
	   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ \
	   -dDownsampleColorImages=true -dDownsampleGrayImages=true \
	   -dDownsampleMonoImages=true -dColorImageResolution=200 \
	   -dGrayImageResolution=200 -dMonoImageResolution=200 $<

update: docs/js/viewer.min.js
	uv lock --upgrade

docs/js/viewer.min.js: FORCE
	wget https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/js/viewer.min.js -O docs/js/viewer.min.js

clean:
	$(RM) -rf build site __pycache__ _minted-*

mrproper: clean
	$(RM) -rf build site home

FORCE:

.PHONY: all serve zensical mkdocs serve-mkdocs servefast build clean update optimize
