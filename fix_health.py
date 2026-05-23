content = """import requests

SERVICES = [
    ("auth-service",          "http://localhost:8001/health"),
    ("inventory-service",     "http://localhost:8002/health"),
    ("catalog-service",       "http://localhost:8003/health"),
    ("ai-enrichment-service", "http://localhost:8004/health"),
    ("normalization-service", "http://localhost:8005/health"),
    ("integration-service",   "http://localhost:8006/health"),
    ("audit-service",         "http://localhost:8007/health"),
    ("pricing-service",       "http://localhost:8008/health"),
    ("external-service",      "http://localhost:8009/health"),
    ("order-service",         "http://localhost:8010/health"),
    ("cart-service",          "http://localhost:8011/health"),
    ("ai-assistant-service",  "http://localhost:8012/health"),
    ("recommender-service",   "http://localhost:8090/health"),
    ("bff-bookflow",          "http://localhost:8000/health"),
]

print("\\n" + "="*60)
print("BOOKFLOW AI COMMERCE - HEALTH CHECK SPRINT 3")
print("="*60)

all_ok = True
for name, url in SERVICES:
    try:
        r = requests.get(url, timeout=5)
        status = "OK" if r.status_code == 200 else "ERROR"
        latency = r.elapsed.total_seconds() * 1000
        print(f"  {status:5} | {name:30} | {latency:.0f}ms")
        if r.status_code != 200:
            all_ok = False
    except Exception as e:
        print(f"  DOWN  | {name:30} | {str(e)[:30]}")
        all_ok = False

print("="*60)
print(f"RESULTADO: {'TODO OK' if all_ok else 'HAY SERVICIOS CAIDOS'}")
print("="*60)
"""

with open("e2e-tests/health_check.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
