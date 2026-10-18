# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first
# This helps Docker reuse the dependency layer when app code changes
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FoodOps application into the container
COPY . .

# Flask listens on port 5000
EXPOSE 5000

# Start the FoodOps Flask application
CMD ["python", "app.py"]