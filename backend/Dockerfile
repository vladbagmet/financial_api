# Use an official Python runtime as a parent image
FROM python:3.9-alpine3.14

# Adding backend directory to make absolute filepaths consistent across services
WORKDIR /backend
ENV PYTHONPATH=${PYTHONPATH}:/backend

RUN apk add --update --no-cache postgresql-client jpeg-dev

# Install Python dependencies
COPY requirements.txt /backend
RUN apk add --update --no-cache --virtual build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
    && pip install -r requirements.txt \
    && apk del build-deps

# Add the rest of the code
COPY . /backend

# Make port 8000 as main port for the app
EXPOSE 8000
CMD rainbow-saddle gunicorn --config python:root.gunicorn root.wsgi
