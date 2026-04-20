# Fix init-db.sh
init_db = """#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "bookflow" <<-EOSQL
    CREATE DATABASE auth_db;
    CREATE DATABASE catalog_db;
    CREATE DATABASE inventory_db;
    CREATE DATABASE pricing_db;
    CREATE DATABASE enrichment_db;
    CREATE DATABASE assistant_db;
    CREATE DATABASE normalization_db;
EOSQL
"""
with open('init-db.sh', 'w', encoding='utf-8', newline='\n') as f:
    f.write(init_db)
print('init-db.sh updated')

# Read current docker-compose
content = open('docker-compose.yml', 'r', encoding='utf-8').read()

# Add normalization-service if not present
if 'normalization-service' not in content:
    new_service = """
  normalization-service:
    build: ./normalization-service
    container_name: bookflow_normalization
    ports:
      - "8005:8005"
    env_file:
      - ./normalization-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network
"""
    content = content.replace('  bff-bookflow:', new_service + '  bff-bookflow:')
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print('docker-compose.yml updated')
else:
    print('normalization-service already in docker-compose.yml')
