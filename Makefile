install:
	uv sync
build:
	uv build
project:
	uv run start
lint:
	uv tool run ruff check
