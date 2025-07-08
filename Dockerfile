# --- Stage 1: Define the base image ---
FROM python:3.11-slim

# --- Stage 2: Set up the working environment ---
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- Stage 3: Install dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy the application code ---
COPY . .

# --- Stage 5: Define the run command ---
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "app:app"]