FROM python:3.9-alpine

RUN apk --update add \
    libc-dev \
    gcc
RUN python3 -m ensurepip

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "application.py" ]