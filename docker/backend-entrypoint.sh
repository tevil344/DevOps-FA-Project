#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Download is intentionally opt-in. It avoids baking 380MB ML files or credentials
# into the image. The script exits successfully if no model source is configured.
if [ -n "${TF_MODEL_URL:-}${TF_MODEL_GOOGLE_DRIVE_ID:-}${PT_MODEL_URL:-}${PT_MODEL_GOOGLE_DRIVE_ID:-}" ]; then
  python download_models.py
fi

if [ -n "${OTEL_EXPORTER_OTLP_ENDPOINT:-}" ]; then
  set -- opentelemetry-instrument "$@"
fi

exec "$@"
