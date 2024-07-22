all:
	poetry run mkdocs build

serve:
	poetry run mkdocs serve --dirty

poetry.lock: pyproject.toml
	poetry lock