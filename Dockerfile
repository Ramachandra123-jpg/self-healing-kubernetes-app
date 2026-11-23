
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy dependency file
COPY app/requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir \
    -r requirements.txt


# Stage 2: Production runtime
FROM python:3.12-slim AS runtime

# Configure Python environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY --chown=10001:10001 app/ /app/

# Create non-root user
RUN useradd --uid 10001 --no-create-home \
    --shell /usr/sbin/nologin appuser

# Run as non-root user
USER 10001:10001

# FastAPI port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

