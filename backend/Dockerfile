# backend/Dockerfile

FROM python:3.10-slim

# System dependencies for Playwright
RUN apt-get update && apt-get install -y wget gnupg curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 libasound2 libgtk-3-0 libgbm-dev

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright + WebKit for iPhone emulation
RUN pip install playwright && playwright install --with-deps webkit

COPY . .

CMD ["python", "app.py"]

