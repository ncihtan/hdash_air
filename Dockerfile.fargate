FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /htan

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Python code
COPY *.py .
COPY hdash ./hdash
CMD ["python", "hdash.py"]