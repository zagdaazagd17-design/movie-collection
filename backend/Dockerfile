# Start from official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (faster rebuilds)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Run the Flask app
CMD ["python", "app.py"]