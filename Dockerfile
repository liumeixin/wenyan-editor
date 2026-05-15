FROM python:3.11-slim

LABEL maintainer="design-shi"
LABEL description="文颜 Markdown 排版器"

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/

EXPOSE 8080

CMD ["python", "backend/app.py"]
