# ---- Stage 1: build the React front end ----
FROM node:20-slim AS frontend
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Django application ----
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Compiled React app (index.html + static bundle) served by Django
COPY --from=frontend /build/build /app/frontend/build

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
