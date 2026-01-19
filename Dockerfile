# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies (required for RDKit and document generation)
RUN apt-get update && apt-get install -y \
    build-essential \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the dashboard port
EXPOSE 8501

# Healthcheck to ensure streamlit is up
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Default command: Open the Interactive Dashboard
ENTRYPOINT ["streamlit", "run", "scripts/v3_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
