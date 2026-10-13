#!/bin/sh
set -e

echo "⏳ Waiting for MySQL database ($DB_HOST:$DB_PORT) to become available..."

python << 'END'
import sys
import time
import os
import pymysql

host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', '3306'))
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', 'rootpassword')
db_name = os.getenv('DB_NAME', 'social_posts')

max_tries = 60
for i in range(max_tries):
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        print("✓ MySQL database is ready!")
        sys.exit(0)
    except Exception as e:
        print(f"Waiting for database ({i+1}/{max_tries})... {e}")
        time.sleep(2)

print("❌ Could not connect to MySQL in time.")
sys.exit(1)
END

echo "🚀 Applying database migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations posts
python manage.py migrate --noinput

echo "🌱 Seeding demo data if database is fresh..."
python seed_demo.py || true

echo "🌐 Starting Django server..."
exec "$@"
