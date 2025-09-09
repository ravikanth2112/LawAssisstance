FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy alembic pydantic psycopg2-binary

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
