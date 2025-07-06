# Use a minimal Python image
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Use non-root user
USER appuser

# Expose the port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
