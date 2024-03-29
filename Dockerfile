# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Update Database
CMD ["alembic", "upgrade", "head"]

# Set the entrypoint command for the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
