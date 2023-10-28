#!/usr/bin/env bash

set -e

mkdir -p /etc/db

mkdir -p /var/log/supervisor/{gunicorn,nginx}

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
