all:
	poetry run mkdocs build

serve:
	poetry run mkdocs serve

poetry.lock: pyproject.toml
	poetry lock