# Add pricing_db to init-db.sh
init_db = open('init-db.sh', 'r', encoding='utf-8').read()
if 'pricing_db' not in init_db:
    init_db = init_db.replace('    CREATE DATABASE audit_db;', '    CREATE DATABASE audit_db;\n    CREATE DATABASE pricing_db;')
    with open('init-db.sh', 'w', encoding='utf-8', newline='\n') as f:
        f.write(init_db)
    print('init-db.sh updated with pricing_db')
else:
    print('pricing_db already in init-db.sh')

content = open('docker-compose.yml', 'r', encoding='utf-8').read()
if 'pricing-service' not in content:
    new_service = """
  pricing-service:
    build: ./pricing-service
    container_name: bookflow_pricing
    ports:
      - "8008:8008"
    env_file:
      - ./pricing-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network
"""
    content = content.replace('  bff-bookflow:', new_service + '  bff-bookflow:')
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print('docker-compose.yml updated with pricing-service')
else:
    print('pricing-service already in docker-compose.yml')
