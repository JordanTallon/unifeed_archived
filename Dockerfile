FROM python:3.12.0-slim
LABEL maintainer="jordan.tallon3@mail.dcu.ie"

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./project_files /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && apt-get install -y --no-install-recommends postgresql-client && \
    # Add temporary dependencies required for installing postgresql
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    /py/bin/pip install -r /requirements.txt && \
    # Install spaCy and the efficiency pipeline en_core_web_sm
    /py/bin/pip install -U setuptools wheel && \
    /py/bin/pip install -U spacy && \
    /py/bin/python -m spacy download en_core_web_sm && \
    # Cleanup to reduce image size
    apt-get purge -y --auto-remove build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --no-create-home app && \
    # Create directories for media and static files
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    # Assign ownership
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
