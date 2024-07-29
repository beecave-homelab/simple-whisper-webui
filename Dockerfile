FROM python:3.11-slim as BASE

COPY . /app
WORKDIR /app

RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]