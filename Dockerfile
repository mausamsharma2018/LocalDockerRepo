# FastAPI Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-asyncio

# Expose port
EXPOSE 8000
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

COPY . .

CMD ["pytest", "test_main.py"]
