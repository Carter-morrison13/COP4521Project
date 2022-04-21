# import from python base image
FROM python:3.8

# expose port 5000, since flask listens on this port for connections
EXPOSE 5000

# specify the working directory for the application
WORKDIR /app

# the next 2 lines tell docker to copy the requirements.txt file
# and pip install them for python3
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy the remaining files to the image
COPY . .

# Finally, we tell Docker how to start up. Since we are running a flask app
# we mention we need python 3 and flask. The '-m' is to run it as a module and 
# we also pass the host port.
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
