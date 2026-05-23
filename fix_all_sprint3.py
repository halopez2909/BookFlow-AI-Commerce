# Fix init-db.sh
initdb = "#!/bin/bash\nset -e\npsql -v ON_ERROR_STOP=1 --username \"bookflow\" <<-EOSQL\n    CREATE DATABASE auth_db;\n    CREATE DATABASE catalog_db;\n    CREATE DATABASE inventory_db;\n    CREATE DATABASE pricing_db;\n    CREATE DATABASE enrichment_db;\n    CREATE DATABASE normalization_db;\n    CREATE DATABASE integration_db;\n    CREATE DATABASE audit_db;\n    CREATE DATABASE order_db;\n    CREATE DATABASE assistant_db;\n    CREATE DATABASE recommender_db;\nEOSQL\n"
with open("init-db.sh", "w", encoding="utf-8", newline="\n") as f:
    f.write(initdb)
print("init-db.sh actualizado")

# Fix docker-compose.yml
compose = """version: "3.9"
services:
  postgres:
    image: postgres:15
    container_name: bookflow_postgres
    environment:
      POSTGRES_USER: bookflow
      POSTGRES_PASSWORD: bookflow123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
    networks:
      - bookflow_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bookflow"]
      interval: 5s
      timeout: 5s
      retries: 10

  auth-service:
    build: ./auth-service
    container_name: bookflow_auth
    ports:
      - "8001:8001"
    env_file:
      - ./auth-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

  inventory-service:
    build: ./inventory-service
    container_name: bookflow_inventory
    ports:
      - "8002:8002"
    env_file:
      - ./inventory-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

  catalog-service:
    build: ./catalog-service
    container_name: bookflow_catalog
    ports:
      - "8003:8003"
    env_file:
      - ./catalog-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

  ai-enrichment-service:
    build: ./ai-enrichment-service
    container_name: bookflow_enrichment
    ports:
      - "8004:8004"
    env_file:
      - ./ai-enrichment-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

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

  external-service:
    build: ./external-service
    container_name: bookflow_external
    ports:
      - "8009:8009"
    env_file:
      - ./external-service/.env
    depends_on:
      - auth-service
      - inventory-service
      - catalog-service
      - ai-enrichment-service
    networks:
      - bookflow_network

  order-service:
    build: ./order-service
    container_name: bookflow_order
    ports:
      - "8010:8010"
    env_file:
      - ./order-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

  cart-service:
    build: ./cart-service
    container_name: bookflow_cart
    ports:
      - "8011:8011"
    env_file:
      - ./cart-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

  ai-assistant-service:
    build: ./ai-assistant-service
    container_name: bookflow_assistant
    ports:
      - "8012:8012"
    env_file:
      - ./ai-assistant-service/.env
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bookflow_network

  recommender-service:
    build: ./recommender-service
    container_name: bookflow_recommender
    ports:
      - "8090:8090"
    env_file:
      - ./recommender-service/.env
    depends_on:
      - catalog-service
    networks:
      - bookflow_network

  bff-bookflow:
    build: ./bff-bookflow
    container_name: bookflow_bff
    ports:
      - "8000:8000"
    env_file:
      - ./bff-bookflow/.env
    depends_on:
      - auth-service
      - inventory-service
      - catalog-service
      - ai-enrichment-service
    networks:
      - bookflow_network

  frontend-bookflow:
    build: ./frontend-bookflow
    container_name: bookflow_frontend
    ports:
      - "3000:80"
    depends_on:
      - bff-bookflow
    networks:
      - bookflow_network

networks:
  bookflow_network:
    driver: bridge

volumes:
  postgres_data:
"""

with open("docker-compose.yml", "w", encoding="utf-8", newline="\n") as f:
    f.write(compose)
print("docker-compose.yml actualizado")
