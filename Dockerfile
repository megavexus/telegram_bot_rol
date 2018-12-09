FROM python:3.6

WORKDIR /$APP_HOME

COPY . $APP_HOME/

RUN pip3 install -e .

CMD python3 src/rol_bot/main.py