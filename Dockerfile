FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend/auth/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/auth/ /app/

# Copy init.sql
COPY backend/auth/db/init.sql /tmp/init.sql

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start PostgreSQL in background\n\
echo "Starting PostgreSQL..."\n\
if [ ! -d /var/lib/postgresql/data ]; then\n\
  sudo -u postgres /usr/lib/postgresql/*/bin/initdb -D /var/lib/postgresql/data\n\
fi\n\
sudo -u postgres /usr/lib/postgresql/*/bin/pg_ctl -D /var/lib/postgresql/data -l /var/lib/postgresql/data/logfile start || true\n\
\n\
# Wait for PostgreSQL\n\
echo "Waiting for PostgreSQL..."\n\
for i in {1..30}; do\n\
  if pg_isready -U postgres > /dev/null 2>&1; then\n\
    echo "PostgreSQL ready!"\n\
    break\n\
  fi\n\
  echo "Attempt $i/30: PostgreSQL not ready yet..."\n\
  sleep 1\n\
done\n\
\n\
# Create user and database\n\
sudo -u postgres psql -c "CREATE USER rj_devs_user WITH PASSWORD '\''${POSTGRES_PASSWORD:-rj_devs_password}'\'';" 2>/dev/null || true\n\
sudo -u postgres psql -c "CREATE DATABASE rj_devs_auth OWNER rj_devs_user;" 2>/dev/null || true\n\
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE rj_devs_auth TO rj_devs_user;"\n\
\n\
# Initialize schema\n\
if [ ! -f /var/lib/postgresql/.db_initialized ]; then\n\
  echo "Initializing database schema..."\n\
  sudo -u postgres psql -d rj_devs_auth -f /tmp/init.sql || true\n\
  touch /var/lib/postgresql/.db_initialized\n\
fi\n\
\n\
# Set DATABASE_URL\n\
export DATABASE_URL=${DATABASE_URL:-postgresql://rj_devs_user:${POSTGRES_PASSWORD:-rj_devs_password}@localhost:5432/rj_devs_auth}\n\
\n\
echo "Starting application on port ${PORT:-8084}..."\n\
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8084}\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8084

# Use the startup script
CMD ["/app/start.sh"]

