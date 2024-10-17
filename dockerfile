# Use the official Python image from the DockerHub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder into the working directory
COPY . .

# Expose port 8501, which is the default port used by Streamlit
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
