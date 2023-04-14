# Use an official Python runtime as a parent image
FROM python:3.9.12
# Set the working directory to /app
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install enchant-2
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet');"
# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME Tars

# Run tars.py when the container launches
CMD ["python", "tars.py"]
