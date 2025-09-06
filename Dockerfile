FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fontconfig \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft fonts using Liberation fonts as fallback
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -fv

# Create font configuration to map Times New Roman to Liberation Serif
RUN mkdir -p /etc/fonts/conf.d && \
    echo '<?xml version="1.0"?>' > /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">' >> /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '<fontconfig>' >> /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '  <alias>' >> /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '    <family>Times New Roman</family>' >> /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '    <prefer><family>Liberation Serif</family></prefer>' >> /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '  </alias>' >> /etc/fonts/conf.d/30-metric-aliases.conf && \
    echo '</fontconfig>' >> /etc/fonts/conf.d/30-metric-aliases.conf

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "bot.py"]