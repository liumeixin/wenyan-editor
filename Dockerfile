FROM python:3.11-slim

LABEL maintainer="design-shi"
LABEL description="文颜 Markdown 排版器"

WORKDIR /app

RUN pip install --no-cache-dir flask

# Create data directory for persistent storage
RUN mkdir -p /app/data

ENV DATA_DIR=/app/data

EXPOSE 8080

# Default: copy files for standalone use.
# With docker-compose, frontend/ and backend/ are mounted as volumes.
COPY backend/app.py ./backend/app.py
COPY backend/markdown_parser.py ./backend/markdown_parser.py
COPY backend/static/ ./backend/static/
COPY frontend/ ./frontend/

CMD ["python", "backend/app.py"]
