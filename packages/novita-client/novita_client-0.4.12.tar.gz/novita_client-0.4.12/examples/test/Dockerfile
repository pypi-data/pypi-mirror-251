FROM python:3.11.1-slim-buster

COPY ./install.sh /install.sh

RUN chmod +x /install.sh

RUN /install.sh

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt 

COPY start.sh /start.sh

RUN chmod +x /start.sh

COPY ./app.py /app.py
RUN chmod +x /app.py

CMD ["./start.sh"]