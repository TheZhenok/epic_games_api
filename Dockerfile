FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    locales \
    build-essential \
    libpq-dev \ 
    curl && \
    python manage.py makemigrations && \
    python manage.py migrate

CMD [ "python", "manage.py", "runserver", "127.0.0.1:7890" ]

EXPOSE 7890