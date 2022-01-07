FROM rackspacedot/python37


ADD main.py /

RUN pip install pymysql \
    && touch /app.log \


CMD ["tail","-f","app.log"]