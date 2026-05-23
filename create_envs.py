# Cart service .env
with open("cart-service/.env", "w", encoding="utf-8", newline="\n") as f:
    f.write("DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/order_db\n")
    f.write("INVENTORY_URL=http://inventory-service:8002\n")
    f.write("PRICING_URL=http://pricing-service:8008\n")
    f.write("CART_MAX_ITEMS=50\n")
print("cart-service/.env creado")

# AI assistant .env
with open("ai-assistant-service/.env", "w", encoding="utf-8", newline="\n") as f:
    f.write("DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/assistant_db\n")
    f.write("OPENAI_API_KEY=sk-placeholder\n")
    f.write("OPENAI_MODEL=gpt-4o-mini\n")
    f.write("CATALOG_URL=http://catalog-service:8003\n")
    f.write("INVENTORY_URL=http://inventory-service:8002\n")
    f.write("PRICING_URL=http://pricing-service:8008\n")
    f.write("HTTP_TIMEOUT=5\n")
    f.write("AI_TIMEOUT=4\n")
    f.write("SERVICE_NAME=ai-assistant-service\n")
    f.write("SERVICE_PORT=8012\n")
print("ai-assistant-service/.env creado")

# Recommender .env
with open("recommender-service/.env", "w", encoding="utf-8", newline="\n") as f:
    f.write("DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/recommender_db\n")
    f.write("CATALOG_URL=http://catalog-service:8003\n")
    f.write("INVENTORY_URL=http://inventory-service:8002\n")
    f.write("ASSISTANT_URL=http://ai-assistant-service:8012\n")
    f.write("PORT=8090\n")
print("recommender-service/.env creado")
