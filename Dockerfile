FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the shared and data directories first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/location_service/ ./services/location_service/
COPY shared/ ./shared/
COPY data/ ./data/

CMD ["uvicorn", "services.location_service.app:app", "--host", "0.0.0.0", "--port", "8001"]
