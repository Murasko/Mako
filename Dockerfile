# Erste Phase: Installieren von Abhängigkeiten und Erstellen von Wheel-Paketen
FROM python:3.11-slim-bullseye AS builder

# ENV for poetry https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# Installieren von Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

# Setzen des Arbeitsverzeichnisses
WORKDIR /app

# Kopieren von pyproject.toml und poetry.lock
COPY pyproject.toml poetry.lock ./

# Installieren von Abhängigkeiten
RUN poetry install --no-root --no-dev

# Kopieren des restlichen Quellcodes
COPY . .

# Erstellen von Wheel-Paketen
RUN poetry build -f wheel

# Zweite Phase: Erstellen des finalen Images
FROM python:3.11-slim-bullseye

# Setzen des Arbeitsverzeichnisses
WORKDIR /mako

# Kopieren von Wheel-Paketen
COPY --from=builder /app/dist/*.whl /mako/

# Installieren von Abhängigkeiten aus Wheel-Paketen
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /mako/*.whl

# Kopieren des restlichen Quellcodes
COPY . .

# Starten der Anwendung
CMD ["python", "src/main.py"]