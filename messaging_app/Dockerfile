# Official Python 3.10 image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# Install python dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the applicatin code
COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Run the Django development server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
