
#our base image
FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/

# Installing python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#specify the port number that the container should expose
EXPOSE 5000

#run the application
CMD ["python", "/app/run.py"]
