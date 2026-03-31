#!/bin/bash

while true; do
    poetry run flask --app manage db upgrade

    if [[ "$?" == "0" ]]; then
        break
    fi

    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec poetry run gunicorn --workers 4 --bind 0.0.0.0:5000 manage:app