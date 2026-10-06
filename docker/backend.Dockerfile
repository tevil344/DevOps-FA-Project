FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system cropleaf && adduser --system --ingroup cropleaf cropleaf

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY backend/ /app/
COPY docker/backend-entrypoint.sh /usr/local/bin/backend-entrypoint
RUN chmod 755 /usr/local/bin/backend-entrypoint && \
    mkdir -p /app/media /app/staticfiles /app/app/ml_models && \
    chown -R cropleaf:cropleaf /app

USER cropleaf
EXPOSE 8000
ENTRYPOINT ["backend-entrypoint"]
CMD ["gunicorn", "CropLeaf.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "180"]
