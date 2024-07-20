all:
	poetry run mkdocs build

poetry.lock: pyproject.toml
	poetry lock