FROM ubuntu:20.04

# Install dependencies and Python
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-browser \
    python3 \
    python3-pip \
    && apt-get clean

# Install ChromeDriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chromedriver-linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Command to run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]


