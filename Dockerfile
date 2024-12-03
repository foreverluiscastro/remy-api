FROM python:3.8.13 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

ENV PIPENV_VENV_IN_PROJECT=1 \
    PIPENV_CUSTOM_VENV_NAME=.venv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
FROM python:3.8.13-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

CMD ["/app/.venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]