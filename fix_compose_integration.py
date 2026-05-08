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
    content = content.replace('  bff-bookflow:', new_service + '  bff-bookflow:')
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print('integration-service agregado al docker-compose.yml')
else:
    print('Ya existe en docker-compose.yml')
