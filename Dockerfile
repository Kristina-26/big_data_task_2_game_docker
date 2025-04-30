FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies for Tkinter and X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN #pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create a simple startup script
RUN echo '#!/bin/bash\n\
echo "Starting Simon Game..."\n\
export DISPLAY=host.docker.internal:0.0\n\
echo "Running game with DISPLAY=$DISPLAY"\n\
python main.py\n' > /app/start.sh && \
chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]