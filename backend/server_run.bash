#!/bin/bash

if [[ $1 != 'deploy' ]]; then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    PARENT_DIR="$(dirname "$DIR")"

    set -a
    source <(cat $PARENT_DIR/.env | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
    set +a
fi


# Run migrations
# alembic revision --autogenerate 
alembic upgrade head 


# Run server
uvicorn app.main:app --host 0.0.0.0 --port 5000