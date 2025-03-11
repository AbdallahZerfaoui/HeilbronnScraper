# Use the official Miniconda3 image as the base image
FROM continuumio/miniconda3:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies using conda or pip
RUN conda install --yes --file requirements.txt || pip install -r requirements.txt
RUN apt-get update && apt-get upgrade -y && apt-get install nano
# Copy the rest of the project files into the container
# COPY . .
# Set the default command to bash
CMD ["bash"]
# Set the default command to run your Python script
# CMD ["python3", "main.py"]