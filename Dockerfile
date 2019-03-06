FROM python:3.6-slim
# FROM python:3.6-slim-stretch

COPY . /webserver
WORKDIR /webserver

# apt-get for Raspberry Pi
# https://geoffboeing.com/2016/03/scientific-python-raspberry-pi/
RUN apt-get -y update
RUN apt-get install -y python3-pandas
RUN apt-get install python3-scipy

RUN pip install -r requirements.txt
# TODO: break here into a seperate container to save build time?

#RUN pip install gunicorn
#RUN pip install falcon

RUN python -m unittest discover -v

EXPOSE 80
#EXPOSE 8000

ENV NAME 'Energy Exploration'

# Should overwrite local envs in .env file
ENV ENERGY_DB_HOST 'influx'

#CMD ["gunicorn", "app:app"]
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
