FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies (install standard litellm if proprietary wheel is inaccessible)
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir fastapi uvicorn motor python-dotenv pyjwt bcrypt httpx pydantic litellm requests

COPY . .

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
