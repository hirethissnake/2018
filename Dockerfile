# Use an official Python runtime as a parent image
FROM python:3 
# Add requirements file to pre-process python requirements
ADD requirements.txt /data/
# Set working directory
WORKDIR /data
# VOLUME - create mount-point for a volume
VOLUME /data/app
# Install any needed packages specified in requirements.txt
RUN pip install -r /data/requirements.txt
# # Make port 80 available to the world outside this container
EXPOSE 8080
