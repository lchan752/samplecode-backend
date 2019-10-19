FROM python:3.7.5-alpine
ENV PYTHONUNBUFFERED 1
RUN apk add build-base postgresql-dev
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
CMD python manage.py runserver