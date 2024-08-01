all:
	poetry run mkdocs build

serve:
	poetry run mkdocs serve --dirty

poetry.lock: pyproject.toml
	poetry lock

build:
	poetry run mkdocs build
	latexmk -C
	latexmk --shell-escape -pdf -file-line-error -lualatex -cd build/index.tex
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer \
	   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=build/output-print.pdf \
	   -dDownsampleColorImages=true -dDownsampleGrayImages=true \
	   -dDownsampleMonoImages=true -dColorImageResolution=200 \
	   -dGrayImageResolution=200 -dMonoImageResolution=200 \
	   build/index.pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
	-dNOPAUSE -dQUIET -dBATCH -sOutputFile=output-screen.pdf \
	-dDownsampleColorImages=true -dDownsampleGrayImages=true \
	-dDownsampleMonoImages=true -dColorImageResolution=72 \
	-dGrayImageResolution=72 -dMonoImageResolution=72 build/index.pdf

.PHONY: all serve build