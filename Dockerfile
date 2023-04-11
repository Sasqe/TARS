# Use an official Python runtime as a parent image
FROM python:3.9.12-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt
RUN python -m spacy download en_core_web_sm
RUN pip install nltk
RUN pip install pyenchant
RUN apt-get update && apt-get install -y enchant

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME Tars

# Run tars.py when the container launches
CMD ["python", "tars.py"]
