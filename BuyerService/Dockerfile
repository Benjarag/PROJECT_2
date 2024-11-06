FROM python:3.8-slim-buster

WORKDIR /aplication

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "-u", "application.py" ]
