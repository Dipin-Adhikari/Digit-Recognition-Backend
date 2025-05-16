# Use the official TensorFlow image (includes Python + TF preinstalled)
FROM tensorflow/tensorflow:2.13.0

# Set the working directory inside the container
WORKDIR /code

# Install OpenCV and required system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Create uploads directory
RUN mkdir -p /code/uploads

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
