FROM python:3.8.19-alpine3.20

#RUN apk add --no-cache gcc musl-dev linux-headers mariadb-dev
#RUN apk add --no-cache mariadb-connector-c

RUN pip3 install --upgrade pip
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install -r requirements.txt

COPY app.py app.py
COPY models/__init__.py models/__init__.py
COPY models/models.py models/models.py

CMD ["uvicorn", "--host", "0.0.0.0", "app:app"]