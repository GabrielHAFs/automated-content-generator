FROM python:3.11-slim

# Set environment variables to ensure output is sent directly to the terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# Install Poetry and dependencies
RUN pip install poetry
RUN poetry install --no-root --no-dev

COPY script.py /app/
COPY src/core/ /app/src/core/

# Command to run the script
CMD ["poetry", "run", "python", "script.py", "/app/keywords.csv"]
