#!/bin/sh

set -e

wait_for_database() {
  WAIT_DB_NAME=$1
  WAIT_DB_USER=$2
  WAIT_DB_PASSWORD=$3
  WAIT_DB_HOST=$4
  WAIT_DB_PORT=$5

  echo "Waiting for PostgreSQL database: $WAIT_DB_NAME..."
  echo "HOST=$WAIT_DB_HOST PORT=$WAIT_DB_PORT USER=$WAIT_DB_USER"

  while ! WAIT_DB_NAME="$WAIT_DB_NAME" WAIT_DB_USER="$WAIT_DB_USER" WAIT_DB_PASSWORD="$WAIT_DB_PASSWORD" WAIT_DB_HOST="$WAIT_DB_HOST" WAIT_DB_PORT="$WAIT_DB_PORT" python -c "
import os
import psycopg

try:
    psycopg.connect(
        dbname=os.getenv('WAIT_DB_NAME'),
        user=os.getenv('WAIT_DB_USER'),
        password=os.getenv('WAIT_DB_PASSWORD'),
        host=os.getenv('WAIT_DB_HOST'),
        port=os.getenv('WAIT_DB_PORT'),
    ).close()
except Exception as error:
    print(error)
    raise SystemExit(1)
"; do
    echo "Database $WAIT_DB_NAME is unavailable - sleeping"
    sleep 1
  done

  echo "Database $WAIT_DB_NAME is available"
}

wait_for_database "$CAT_POSTGRES_DB" "$CAT_POSTGRES_USER" "$CAT_POSTGRES_PASSWORD" "$CAT_DB_HOST" "$CAT_DB_PORT"
wait_for_database "$SHELTER_POSTGRES_DB" "$SHELTER_POSTGRES_USER" "$SHELTER_POSTGRES_PASSWORD" "$SHELTER_DB_HOST" "$SHELTER_DB_PORT"

echo "Applying migrations on default database..."
python manage.py migrate --database=default --noinput

echo "Applying shelter migrations on shelter database..."
python manage.py migrate shelter --database=shelter --noinput

echo "Seeding authorized users..."
python manage.py seed_users

echo "Seeding initial cats data..."
python manage.py seed_data

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000