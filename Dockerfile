FROM python:3.9-apline3.13

ENV PYTHONUNBUFFERED 1

COPY ./project /app
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /app
EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \ 
    /venv/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/venv/bin:$PATH"

USER django-user

