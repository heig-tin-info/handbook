all:
	poetry run mkdocs build

serve:
	poetry run mkdocs serve --dirty

poetry.lock: pyproject.toml
	poetry lock

build:
	poetry run mkdocs build
	latexmk --shell-escape -pdf -lualatex -cd build/index.tex