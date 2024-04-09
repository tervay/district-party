# Use the official Python 3.11 image as a base
FROM python:3.11

# Set the working directory in the container
WORKDIR /app/backend

# Copy the requirements file
COPY requirements.txt .

# Install Flask and Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000
EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "main:app" ]