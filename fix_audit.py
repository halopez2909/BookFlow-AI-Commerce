# Add audit_db to init-db.sh
init_db = open('init-db.sh', 'r', encoding='utf-8').read()
if 'audit_db' not in init_db:
    init_db = init_db.replace('    CREATE DATABASE integration_db;', '    CREATE DATABASE integration_db;\n    CREATE DATABASE audit_db;')
    with open('init-db.sh', 'w', encoding='utf-8', newline='\n') as f:
        f.write(init_db)
    print('init-db.sh updated with audit_db')
else:
    print('audit_db already in init-db.sh')

# Add audit-service to docker-compose.yml
content = open('docker-compose.yml', 'r', encoding='utf-8').read()
if 'audit-service' not in content:
    new_service = """
  audit-service:
    build: ./audit-service
    container_name: bookflow_audit
    ports:
      - "8007:8007"
    env_file:
      - ./audit-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network
"""
    content = content.replace('  bff-bookflow:', new_service + '  bff-bookflow:')
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print('docker-compose.yml updated with audit-service')
else:
    print('audit-service already in docker-compose.yml')
