# 1. Base image: Use an official Python runtime as a parent image
FROM python:3.12

# 2. Set the working directory in the container
WORKDIR /Travel

# 3. Copy the requirements.txt file to the working directory
COPY requirements.txt .

# 4. Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the current directory contents into the container at /app
COPY . .

# 6. Expose port 8000 (Django's default port)
EXPOSE 8000

# 7. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION=3.12.7


# 8. Run database migrations and start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
