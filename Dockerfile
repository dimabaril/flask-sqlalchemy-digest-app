FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
