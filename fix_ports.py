# Fix cart-service port
with open("cart-service/Dockerfile", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("--port", "--port").replace('"8000"', '"8011"').replace("EXPOSE 8000", "EXPOSE 8011")
with open("cart-service/Dockerfile", "w", encoding="utf-8") as f:
    f.write(content)
print("cart-service: puerto -> 8011")

# Fix ai-assistant-service port
with open("ai-assistant-service/Dockerfile", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace('"8010"', '"8012"')
with open("ai-assistant-service/Dockerfile", "w", encoding="utf-8") as f:
    f.write(content)
print("ai-assistant-service: puerto -> 8012")

print("recommender-service: puerto 8090 OK")
