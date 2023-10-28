FROM python:3.12.0-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        sqlite3 \
        supervisor \
    && apt-get clean \
    && rm -Rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/
RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

COPY ./app /app

RUN ln -s /app/entrypoint.sh / \
    && ln -s /app/nginx.conf /etc/nginx/conf.d/ \
    && ln -s /app/supervisord.conf /etc/supervisor/conf.d/ \
    && ln -s /app/gunicorn.py /etc/

# TODO: connect to persistent database. this will get deleted between container restarts during development
ENV DB_PATH=/etc/db/sqlite.db
ENV FLASK_APP=application:create_app()

EXPOSE 8080

ENTRYPOINT [ "/entrypoint.sh" ]