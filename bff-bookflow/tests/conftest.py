"""Configuracion compartida de tests Sprint 3."""
import os
os.environ.setdefault("JWT_SECRET_KEY", "supersecretkey123bookflow")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("CART_URL", "http://cart-service:8010")
os.environ.setdefault("ORDER_URL", "http://order-service:8011")
os.environ.setdefault("ASSISTANT_URL", "http://ai-assistant-service:8012")
os.environ.setdefault("RECOMMENDER_URL", "http://recommender-service:8013")
os.environ.setdefault("CATALOG_URL", "http://catalog-service:8003")
os.environ.setdefault("PRICING_URL", "http://pricing-service:8008")
os.environ.setdefault("INVENTORY_URL", "http://inventory-service:8002")
