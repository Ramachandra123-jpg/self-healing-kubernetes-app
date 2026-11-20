# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir \
    -r requirements.txt


# Stage 2: Production runtime
FROM python:3.12-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed dependencies from builder.
COPY --from=builder /opt/venv /opt/venv

# Copy application code.
COPY --chown=10001:10001 app/ /app/

# Create non-root application user.
RUN useradd --uid 10001 --no-create-home \
    --shell /usr/sbin/nologin appuser

USER 10001:10001

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
