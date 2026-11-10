FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir pip==26.2.0

COPY . .

CMD ["python3", "app.py"]
