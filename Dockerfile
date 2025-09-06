FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ttf-mscorefonts-installer \
    fontconfig \
    wget \
    cabextract \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Accept EULA for MS fonts
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

# Install MS fonts (alternative method if the package doesn't work)
RUN mkdir -p /usr/share/fonts/truetype/msttcorefonts
RUN wget -q -O /tmp/fonts.tar.gz https://sourceforge.net/projects/corefonts/files/the%20fonts/final/arial32.exe/download \
    && cabextract -q -d /tmp /tmp/fonts.tar.gz \
    && cabextract -q -d /usr/share/fonts/truetype/msttcorefonts /tmp/*.cab \
    && rm -rf /tmp/*

RUN wget -q -O /tmp/times32.exe https://sourceforge.net/projects/corefonts/files/the%20fonts/final/times32.exe/download \
    && cabextract -q -d /usr/share/fonts/truetype/msttcorefonts /tmp/times32.exe \
    && rm -rf /tmp/*

# Update font cache
RUN fc-cache -f -v

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