BUILD_BASE_DIR = build
BUILD_DIRS=$(shell find $(BUILD_BASE_DIR) -mindepth 1 -maxdepth 1 -type d)

BUILD_INDEXES=$(foreach dir,$(BUILD_DIRS),$(dir)/index.tex)
BUILD_PDFS=$(foreach dir,$(BUILD_DIRS),$(dir)/index.pdf)
BUILD_OUTPUTS=$(foreach dir,$(BUILD_DIRS),$(dir)/output-print.pdf)

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	RUNCMD = PYTHONBREAKPOINT=ipdb.set_trace uv run
else
	RUNCMD = uv run
endif

all:
	$(RUNCMD) mkdocs build

serve:
	$(RUNCMD) mkdocs serve

# The Zensical chain: the generated assets first (Zensical empties the site
# directory and caches pages, so nothing Python writes during a build
# survives), then the site, then the two books. The search index needs no
# step of its own: a page's index entries are its tags, and the extension
# writes them while the page renders.
zensical:
	$(RUNCMD) texsmith site assets mkdocs.yml
	$(RUNCMD) zensical build -f mkdocs.yml
	$(RUNCMD) texsmith site build mkdocs.yml

serve-zensical:
	$(RUNCMD) texsmith site assets mkdocs.yml
	$(RUNCMD) zensical serve -f mkdocs.yml -a 127.0.0.1:8100

servefast:
	$(RUNCMD) mkdocs serve --dirty

uv.lock: pyproject.toml
	uv lock

build:
	$(RUNCMD) mkdocs build

latex-clean:
	$(RM) -rf $(BUILD_DIR)/_minted-index
	latexmk -cd $(BUILD_DIR)/index.tex -C

%.pdf: %.tex | FORCE
	latexmk -cd -gg \
	-time -logfilewarninglist --interaction=nonstopmode --halt-on-error \
	$<

latex: $(BUILD_PDFS) | FORCE

%/output-print.pdf: %/index.pdf
	gs -sDEVICE=pdfwrite -dPDFSETTINGS=/printer \
	   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ \
	   -dDownsampleColorImages=true -dDownsampleGrayImages=true \
	   -dDownsampleMonoImages=true -dColorImageResolution=200 \
	   -dGrayImageResolution=200 -dMonoImageResolution=200 $<

image: Dockerfile
	docker build -t latex-ycr .

ci:
	docker run -v $(shell pwd):/workspace \
	-w /workspace \
	-u $(shell id -u):$(shell id -g) \
	-v /etc/passwd:/etc/passwd:ro \
	latex-ycr \
	make latex optimize

update: docs/js/viewer.min.js
	uv lock --upgrade

docs/js/viewer.min.js: FORCE
	wget https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/js/viewer.min.js -O docs/js/viewer.min.js

optimize: $(BUILD_OUTPUTS)

clean:
	$(RM) -rf build site __pycache__ _minted-*

mrproper: clean
	$(RM) -rf build site home

FORCE:

.PHONY: all serve zensical serve-zensical build clean update optimize latex latex-clean docker-image ci update-viewer
