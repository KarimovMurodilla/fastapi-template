# Ruff
.PHONY: check
check:
	ruff check

# Alembic utils
.PHONY: generate
generate:
	python -m alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	python -m alembic upgrade head
