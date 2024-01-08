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
    # Add temporary dependencies required for installing postgresql
    apk add --update --no-cache --virtual .tmp-deps \ 
	build-base postgresql-dev musl-dev libpq && \
    /py/bin/pip install -r /requirements.txt && \
    # Delete temporary dependencies
    apk del .tmp-deps && \  
    adduser --disabled-password --no-create-home app && \
    # Create directories for media and static files
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    # Assign ownership
    chown -R app:app /vol && \
    chmod -R 755 /vol


ENV PATH="/py/bin:$PATH"

USER app
