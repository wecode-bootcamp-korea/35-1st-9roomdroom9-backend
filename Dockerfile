FROM python:3

WORKDIR /usr/src/app

COPY requirements/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["nohup", "gunicorn", "--bind", "0.0.0.0:8000", "guroom.wsgi", "&"]