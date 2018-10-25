FROM python:2.7

COPY . /root/

RUN pip install -r /root/requirements.txt

WORKDIR /root/

CMD gunicorn -b 0.0.0.0:8081 -w 4 app:app