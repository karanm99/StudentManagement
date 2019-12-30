FROM ubuntu:16.04
LABEL maintainer="Karan Meghani <karanm99@gmail.com>"
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi
COPY ./requirements.txt ./app/requirements.txt
WORKDIR ./app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "handler.py" ]
