content = open('docker-compose.yml', 'r', encoding='utf-8').read()

new_services = """
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

content = content.replace('  bff-bookflow:', new_services + '  bff-bookflow:')
with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(content)
print('docker-compose.yml updated!')
