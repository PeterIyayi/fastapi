FROM python:3.11-slim

WORKDIR /app

# Install deps
RUN apt-get update && apt-get install -y \
    curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Download ngrok v3
RUN curl -sLo ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip \
    && unzip ngrok.zip \
    && mv ngrok /usr/local/bin/ \
    && rm ngrok.zip

# Expose FastAPI + ngrok web
EXPOSE 8000
EXPOSE 4040

# Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
