# syntax=docker/dockerfile:1

FROM python:3.7.2-stretch

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["./gunicorn.sh"]

# Entrypoint replaces the initial command
# CMD ["gunicorn", "portfolio:create_app()"]