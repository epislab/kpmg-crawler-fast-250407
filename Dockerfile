FROM python:3.12.7-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .  

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
