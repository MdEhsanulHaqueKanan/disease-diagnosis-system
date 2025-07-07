# --- Stage 1: Define the base image ---
# Use an official, slim Python image. 'slim' versions are smaller, leading to a smaller final image size.
# Pinning the version (e.g., 3.9) is a best practice for reproducibility.
FROM python:3.9-slim

# --- Stage 2: Set up the working environment ---
# Set the working directory inside the container. All subsequent commands run from here.
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- Stage 3: Install dependencies ---
# Copy the requirements file first. This leverages Docker's layer caching.
# If requirements.txt doesn't change, Docker won't re-run this layer, speeding up builds.
COPY requirements.txt .

# Install dependencies using pip. --no-cache-dir keeps the image size down.
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy the application code ---
# Now, copy the rest of your application files into the working directory.
COPY . .

# --- Stage 5: Define the run command ---
# Use Gunicorn as the production WSGI server, not the Flask development server.
# This command tells the container what to run when it starts.
# - "app:app": Tells Gunicorn to run the 'app' variable from the 'app.py' file.
# - "--bind 0.0.0.0:10000": Binds the server to all network interfaces on port 10000.
#   Render will automatically map its public URL to this internal port.
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]