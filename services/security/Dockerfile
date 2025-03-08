FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY src/ /app/src/
COPY static/ /app/static/
COPY templates/ /app/templates/

# Create the reports directory
RUN mkdir -p reports

# Expose the port
EXPOSE 8080

# Set the entry point
CMD ["python", "/app/src/scanner.py"]