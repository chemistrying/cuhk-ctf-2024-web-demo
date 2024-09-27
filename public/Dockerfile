FROM python:3.12-alpine

RUN apk add chromium-chromedriver

RUN mkdir /.cache/
RUN mkdir /.cache/selenium
RUN chmod -R 777 /.cache/selenium/

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
COPY ./flag5 /
COPY . /app/
RUN chmod 555 /app
RUN chmod +x ./entrypoint.sh

EXPOSE 8080

USER nobody

RUN ulimit -u 128

CMD ["/bin/sh", "-c", "./entrypoint.sh"]