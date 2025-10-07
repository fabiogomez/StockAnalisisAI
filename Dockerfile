# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the dependencies file to the working directory
COPY requirements.txt .

# 4. Install any needed packages specified in requirements.txt
# Using --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code into the container
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Define the command to run your app using uvicorn
#    --host 0.0.0.0 makes it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]