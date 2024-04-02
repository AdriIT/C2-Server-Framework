FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir server
COPY . ./server

RUN python3 -m pip install -U "channels[daphne]"
RUN python3 -m pip install channels_redis
RUN python3 -m pip install "psycopg[binary]"
#RUN python3 -m pip install docker
#RUN python3 ./server/manage.py makemigrations


#RUN python3 ./server/manage.py migrate
#RUN rm ./server/db.sqlite3
EXPOSE 8000

WORKDIR ./server
#ENTRYPOINT ["python", "manage.py", "migrate" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
