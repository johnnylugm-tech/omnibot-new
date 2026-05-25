#syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
COPY src/ /app/src/
RUN pip install --no-cache-dir -e /app/src
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.infrastructure.config:app", "--host", "0.0.0.0", "--port", "8000"]