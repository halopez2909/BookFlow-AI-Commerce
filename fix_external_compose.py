content = open('docker-compose.yml', 'r', encoding='utf-8').read()
if 'external-service' not in content:
    new_service = """
  external-service:
    build: ./external-service
    container_name: bookflow_external
    ports:
      - "8009:8009"
    env_file:
      - ./external-service/.env
    networks:
      - bookflow_network
"""
    content = content.replace('  bff-bookflow:', new_service + '  bff-bookflow:')
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print('docker-compose.yml updated')
else:
    print('Already exists')
