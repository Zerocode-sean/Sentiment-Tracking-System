FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY Sentiments/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data reports models

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# Run the application
CMD streamlit run src/enhanced_dashboard.py --server.port=8080 --server.address=0.0.0.0 --server.enableXsrfProtection=false --server.enableCORS=false
