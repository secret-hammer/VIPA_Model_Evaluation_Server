FROM python:3.8
RUN apt-get install default-libmysqlclient-dev mysql-server -y

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt 
COPY . .
EXPOSE 8000
CMD ["bash","start.sh"]
