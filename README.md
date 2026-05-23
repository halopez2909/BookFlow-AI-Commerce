# BookFlow AI Commerce

Plataforma inteligente de comercio de libros con microservicios e IA.

## Requisitos
- Docker Desktop
- Docker Compose

## Levantar el sistema
```bash
docker compose up --build -d
```

## Verificar que todo funciona
```bash
python e2e-tests/health_check.py
```

## Cargar datos de demo
```bash
python seed_data.py
```

## Demo completa
1. Abrir http://localhost:3000
2. Login: admin@bookflow.com / admin123
3. Explorar catalogo con libros enriquecidos con IA
4. Ver ficha de libro con precio IA y recomendaciones
5. Agregar al carrito
6. Confirmar pedido
7. Consultar asistente IA en /assistant
8. Ver historial en /orders

## Servicios

| Servicio | Puerto |
|---|---|
| BFF Gateway | 8000 |
| Auth | 8001 |
| Inventory | 8002 |
| Catalog | 8003 |
| AI Enrichment | 8004 |
| Normalization | 8005 |
| Integration | 8006 |
| Audit | 8007 |
| Pricing | 8008 |
| External | 8009 |
| Order | 8010 |
| Cart | 8011 |
| AI Assistant | 8012 |
| Recommender | 8090 |
| Frontend | 3000 |
