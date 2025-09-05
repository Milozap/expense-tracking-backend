FROM python:3.10.5

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev postgresql-client \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ARG INSTALL_DEV=0
COPY requirements-dev.txt /app/
RUN if [ "$INSTALL_DEV" = "1" ]; then pip install --no-cache-dir -r requirements-dev.txt; fi

COPY . /app/

EXPOSE 8000

CMD ["/bin/bash", "-lc", "\
until pg_isready -h ${POSTGRES_HOST:-db} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres}; do \
  echo 'Waiting for database...'; sleep 1; \
done; \
python manage.py migrate && \
"]
