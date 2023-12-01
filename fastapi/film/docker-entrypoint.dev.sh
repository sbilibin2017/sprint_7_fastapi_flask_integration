#!/bin/bash

echo "Waiting for postgres ..."
while ! nc -z postgres_film $POSTGRES_PORT; do
  sleep 1
done
echo "Postgres started"

echo "Waiting for redis..."
while ! nc -z redis_film $REDIS_PORT; do
  sleep 1
done
echo "Redis started"

echo "Waiting for elasticsearch..."
while ! nc -z elasticsearch_film $ELASTIC_PORT; do
  sleep 1
done
echo "Elasticsearch started"

python3 main.py

