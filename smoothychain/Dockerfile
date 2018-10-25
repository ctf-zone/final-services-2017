FROM python:3.6

#COPY team_service/ /home/smoothychain/
COPY docker/start.sh /root/start.sh

RUN chmod +x /root/start.sh && \
    pip install sanic && \
    pip install pycrypto && \
    pip install coloredlogs && \
    pip install peewee && \
    pip install psycopg2 && \
    pip install aiohttp && \
    pip install apscheduler 

CMD ["/root/start.sh"]
