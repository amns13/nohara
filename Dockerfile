FROM python:3.8.5-alpine

RUN adduser -D nohara

WORKDIR /home/nohara

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY nohara.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP nohara.py

RUN chown -R nohara:nohara ./
USER nohara

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]