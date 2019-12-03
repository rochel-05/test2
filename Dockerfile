
#our base image
FROM python:3-onbuild

RUN mkdir /app2
WORKDIR /app2
ADD . /app2/

# Installing python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#specify the port number that the container should expose
EXPOSE 5000

#run the application
CMD ["python", "/app2/run.py"]
