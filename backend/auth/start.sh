#!/bin/bash
set -e

# Wait for database to be ready (useful for Render)
echo "Waiting for database connection..."
python -c "
import os
import time
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

database_url = os.getenv('DATABASE_URL')
if not database_url:
    print('ERROR: DATABASE_URL environment variable is not set!')
    print('Please configure DATABASE_URL in Render environment variables.')
    sys.exit(1)

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        print('Database connection successful!')
        break
    except OperationalError as e:
        retry_count += 1
        if retry_count >= max_retries:
            print(f'ERROR: Could not connect to database after {max_retries} attempts')
            print(f'Last error: {e}')
            sys.exit(1)
        print(f'Database not ready yet, retrying... ({retry_count}/{max_retries})')
        time.sleep(2)
"

# Get port from environment variable (Render sets this)
PORT=${PORT:-8084}
echo "Starting application on port $PORT..."

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port $PORT
