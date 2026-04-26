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
    CREATE DATABASE integration_db;
EOSQL
"""
with open('init-db.sh', 'w', encoding='utf-8', newline='\n') as f:
    f.write(init_db)
print('init-db.sh updated')

content = open('docker-compose.yml', 'r', encoding='utf-8').read()

if 'integration-service' not in content:
    new_service = """
  integration-service:
    build: ./integration-service
    container_name: bookflow_integration
    ports:
      - "8006:8006"
    env_file:
      - ./integration-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network
"""
    content = content.replace('  normalization-service:', new_service + '  normalization-service:')
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print('docker-compose.yml updated')
else:
    print('Already in docker-compose.yml')
