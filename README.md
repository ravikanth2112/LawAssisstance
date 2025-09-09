# LawAssistance

This repository uses a monorepo layout:

- Frontend: Next.js (TypeScript)  `apps/web`
- Backend: FastAPI (Python)  `apps/api`
- Database: PostgreSQL
- Redis: Redis (for future background jobs)

## Quick start with Docker Compose

1. Copy example env:
```
cp .env.example .env
```

2. Build and start services:
```
docker-compose up --build
```

Services:
- API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- Web: http://localhost:3000 (if `apps/web` provides a dev server or Dockerfile)

## Run backend locally (dev)

From repository root:
```
powershell
cd apps/api
python -m venv .venv
.venv\\Scripts\\Activate.ps1     # PowerShell on Windows
pip install -U pip
pip install fastapi uvicorn[standard] sqlalchemy pydantic psycopg2-binary
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open API docs at http://127.0.0.1:8000/docs

## Run frontend locally (dev)

From repository root:
```
cd apps/web
# use your package manager (pnpm / npm / yarn)
pnpm install
pnpm dev
# open http://localhost:3000
```

## Removing legacy Node/Express (already done or optional)

Legacy Node/Express server files (if present) should be removed. See the commands below for safe removal.

## Notes

- `apps/api` includes a minimal, runnable scaffold. Expand `app/models`, `app/services` and add Alembic migrations as needed.
- Update `.env` with strong `SECRET_KEY` and production DB credentials for production deployments.
