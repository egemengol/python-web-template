default: run

migrate:
    refinery migrate -e DATABASE_URL --table-name zz_migrations

clean:
    usql $DATABASE_URL --command="drop schema if exists public cascade; create schema public;"

ruff:
    ruff check --select I --fix
    ruff format

run:
    uv run fastapi dev src/main.py --host 0.0.0.0
# uv run python -m src.main
