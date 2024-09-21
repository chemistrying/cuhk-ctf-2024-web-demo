FROM python:3.12-alpine

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/

EXPOSE 8080

USER nobody

CMD ["gunicorn", "-w", "1", "app:app"]