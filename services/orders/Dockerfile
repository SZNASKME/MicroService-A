# Multi-stage build for smaller production image
FROM python:3.9-slim AS builder

# Install build dependencies in single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory and copy requirements
WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.9-slim

# Create non-root user and install runtime deps in one layer
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage with proper ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy only necessary application files
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser wsgi.py .
COPY --chown=appuser:appuser config.py .
COPY --chown=appuser:appuser .env.production .env
COPY --chown=appuser:appuser features/ features/

# Create necessary directories with proper permissions
RUN mkdir -p uploads logs \
    && chown -R appuser:appuser uploads logs \
    && chmod 755 uploads logs

# Switch to non-root user
USER appuser

# Set environment variables for production
ENV PATH=/home/appuser/.local/bin:$PATH \
    FLASK_ENV=production \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    WORKERS=4

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "sync", "--timeout", "30", "--keep-alive", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "wsgi:application"]