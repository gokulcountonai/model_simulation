FROM ubuntu:20.04

#Makedir /app
RUN mkdir /app
RUN mkdir /install

# Install zip and unzip packages
RUN apt-get update && apt-get install -y zip unzip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Add your application files to the container
COPY requirements.txt /install
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --no-cache-dir -r /install/requirements.txt
COPY main.zip /app
# Set the working directory in the container
WORKDIR /app

RUN unzip main.zip
# Set the default command to run your application
CMD [ "python3","app.py" ]
