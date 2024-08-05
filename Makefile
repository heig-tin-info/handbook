all:
	poetry run mkdocs build

serve:
	poetry run mkdocs serve --dirty

poetry.lock: pyproject.toml
	poetry lock

build:
	poetry run mkdocs build

latex: build/index.tex
	latexmk -cd build/index.tex -C
	latexmk --shell-escape -pdf -file-line-error -lualatex -cd build/index.tex

build/output-print.pdf: build/index.pdf
	gs -sDEVICE=pdfwrite -dPDFSETTINGS=/printer \
	   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ \
	   -dDownsampleColorImages=true -dDownsampleGrayImages=true \
	   -dDownsampleMonoImages=true -dColorImageResolution=200 \
	   -dGrayImageResolution=200 -dMonoImageResolution=200 $<

build/output-screen.pdf: build/index.pdf
	gs -sDEVICE=pdfwrite -dPDFSETTINGS=/screen \
	   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ \
	   -dDownsampleColorImages=true -dDownsampleGrayImages=true \
	   -dDownsampleMonoImages=true -dColorImageResolution=72 \
	   -dGrayImageResolution=72 -dMonoImageResolution=72 $<

update-viewer:
	wget https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/js/viewer.min.js -O docs/js/viewer.min.js

optimize: build/output-print.pdf

clean:
	rm -rf build site

.PHONY: all serve build clean optimize