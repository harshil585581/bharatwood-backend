FROM python:3.11-slim

WORKDIR /app

# Install dependencies (only copy requirements file first to cache this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Command to run the application
CMD ["fastapi", "run", "main.py", "--port", "8000"]
