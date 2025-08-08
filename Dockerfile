# Lightweight container for static file serving only
FROM python:3.12-slim

# Set basic environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create workspace directory
WORKDIR /workspace

# Copy web files
COPY web_site/ ./web_site/

# Expose port for static server
EXPOSE 8080

# Start static file server
CMD ["python", "-m", "http.server", "8080", "--directory", "web_site"] 