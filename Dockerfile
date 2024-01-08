FROM python:alpine3.19
LABEL maintainer = "jordan.tallon3@mail.dcu.ie"

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./project_files /app


WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \ # Add temporary dependencies required for installing postgresql
	build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \ # Delete temporary dependencies 
    adduser --disabled-password --no-create-home app

ENV PATH="/py/bin:$PATH"

USER app
