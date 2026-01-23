FROM python:3.10-slim

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

# expose port
EXPOSE 8000

# run FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
