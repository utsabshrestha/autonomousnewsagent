# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the FastAPI server with uvicorn directly for better production performance
# Use multiple workers for production (adjust based on CPU cores)
CMD ["uvicorn", "Server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
