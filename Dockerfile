# --- Stage 1: Define the base image ---
FROM python:3.11-slim

# --- Stage 2: Set up the working environment ---
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- Stage 3: Create Swapfile to handle memory spikes ---
# This is the key fix for the "Out of Memory" error on Render's free tier.
# It creates a 1GB swap file (virtual RAM) inside the container.
RUN fallocate -l 1G /swapfile && \
    chmod 600 /swapfile && \
    mkswap /swapfile && \
    swapon /swapfile

# --- Stage 4: Install dependencies ---
# Copy requirements file first to leverage Docker's layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 5: Copy the application code ---
COPY . .

# --- Stage 6: Define the run command ---
# Gunicorn will run the app with a 120-second timeout.
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "app:app"]