FROM jfloff/alpine-python:3.8

RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk add --no-cache ffmpeg

COPY . /app
WORKDIR /app
RUN pip install pipenv

RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "bot.py"]
