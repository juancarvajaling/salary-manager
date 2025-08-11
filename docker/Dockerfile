# Lightweight container for static file serving only
FROM python:3.12-slim

# Set basic environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create workspace directory
WORKDIR /workspace

# Copy web files
COPY frontend/ ./frontend/

# Expose port for static server
EXPOSE 8080

# Start static file server
CMD ["python", "-m", "http.server", "8080", "--directory", "frontend"] 