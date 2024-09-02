BUILD_DIR=build/book

all:
	poetry run mkdocs build

serve:
	poetry run mkdocs serve

servefast:
	poetry run mkdocs serve --dirty

poetry.lock: pyproject.toml
	poetry lock

build:
	poetry run mkdocs build

latex-clean:
	$(RM) -rf $(BUILD_DIR)/_minted-index
	latexmk -cd $(BUILD_DIR)/index.tex -C

latex: $(BUILD_DIR)/index.tex | latex-clean
	latexmk -cd $(BUILD_DIR)/index.tex -gg \
	-time -logfilewarninglist --interaction=nonstopmode --halt-on-error

$(BUILD_DIR)/output-print.pdf: $(BUILD_DIR)/index.pdf
	gs -sDEVICE=pdfwrite -dPDFSETTINGS=/printer \
	   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ \
	   -dDownsampleColorImages=true -dDownsampleGrayImages=true \
	   -dDownsampleMonoImages=true -dColorImageResolution=200 \
	   -dGrayImageResolution=200 -dMonoImageResolution=200 $<

docker-image: Dockerfile
	docker build -t latex-ycr .

ci:
	docker run -v $(shell pwd):/workspace \
				-w /workspace \
				-u $(shell id -u):$(shell id -g) \
				-v /etc/passwd:/etc/passwd:ro \
				latex-ycr \
				make latex optimize

update: docs/js/viewer.min.js
	poetry update

docs/js/viewer.min.js: FORCE
	wget https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/js/viewer.min.js -O docs/js/viewer.min.js


optimize: $(BUILD_DIR)/output-print.pdf

clean:
	$(RM) -rf build site __pycache__ _minted-*

FORCE:

.PHONY: all serve build clean update optimize latex latex-clean docker-image ci update-viewer