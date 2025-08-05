# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Expose port (Flask default)
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
