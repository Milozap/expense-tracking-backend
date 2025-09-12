FROM python:3.10.5

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements/ /app/requirements/
RUN pip install -r requirements/base.txt

ARG INSTALL_DEV=0
RUN if [ "$INSTALL_DEV" = "1" ]; then pip install -r requirements/dev.txt; fi

COPY . /app/

# Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (can be overridden by compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
