DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARENT_DIR="$(dirname "$DIR")"

set -o allexport
[[ -f "$PARENT_DIR/.env" ]] && source "$PARENT_DIR/.env"
set +o allexport


alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 5000
