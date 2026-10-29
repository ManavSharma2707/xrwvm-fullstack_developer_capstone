FROM python:3.11-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Hosts such as Render/Code Engine inject PORT; default to 5000 locally
ENV PORT=5000
EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:${PORT} app:app
