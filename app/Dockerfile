FROM python:3-alpine

EXPOSE 1123

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/app

RUN pip install --no-cache-dir psycopg2 config configparser flask flask_restful python-twitter oauth2 waitress

CMD ["python", "-u", "./server.py"]
