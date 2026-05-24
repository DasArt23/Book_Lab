MODE ?= sequential
W ?= 4

install:
	uv sync
build:
	uv build
project:
	uv run start -m $(MODE) -w $(W)
lint:
	uv tool run ruff check
teleg:
	uv run start -m teleg
