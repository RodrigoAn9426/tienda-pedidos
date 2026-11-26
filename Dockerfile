FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home appuser \
    && mkdir /app \
    && chown appuser:appuser /app

WORKDIR /app
USER appuser

COPY --chown=appuser:appuser requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY --chown=appuser:appuser . .

CMD ["python", "-m", "pytest", "-q"]