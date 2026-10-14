# Multi-platform production container for MovieMatch
FROM python:3.11-slim

WORKDIR /app

# Ensure stdout/stderr are flushed immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application assets & data
COPY . .

# Expose standard container port
EXPOSE 5000

# Health check instruction for container orchestrators
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

# Launch production WSGI server
CMD ["sh", "-c", "gunicorn --workers 4 --bind 0.0.0.0:${PORT:-5000} app:app"]
