FROM python:3.11-slim as BASE

COPY . /app
WORKDIR /app

RUN python -m venv venv \
    && source venv/bin/activate \
    && pip install -r requirements.

EXPOSE 5000
CMD ["python", "app.py"]