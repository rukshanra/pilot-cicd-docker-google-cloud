# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Python script to the container
COPY riyasewana.py .

# Set the command to run when the container starts
CMD ["python", "riyasewana.py"]
