import requests
import time

BASE = "http://localhost:8000"
ENRICH = "http://localhost:8004"

# 1. Login
token_resp = requests.post(f"{BASE}/api/auth/login", json={"email":"admin@bookflow.com","password":"admin1234"})
token = token_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Traer todos los libros
all_books = []
page = 1
while True:
    r = requests.get(f"{BASE}/api/catalog/books", params={"page": page, "page_size": 50}, headers=headers)
    data = r.json()
    items = data.get("items", [])
    all_books.extend(items)
    if len(all_books) >= data.get("total", 0):
        break
    page += 1

print(f"Total libros: {len(all_books)}")

# 3. Enriquecer los que no tienen cover_url
enriched = 0
for book in all_books:
    if book.get("cover_url"):
        print(f"Ya tiene portada: {book['title']}")
        continue
    payload = {
        "book_reference": book["id"],
        "title": book["title"],
        "author": book["author"],
        "isbn": book.get("isbn", "")
    }
    try:
        r = requests.post(f"{ENRICH}/enrichment/enrich", json=payload, timeout=15)
        result = r.json()
        source = result.get("metadata_json", {}).get("source", "?") if isinstance(result.get("metadata_json"), dict) else "?"
        cover = result.get("cover_url", "")
        print(f"OK [{source}] {book['title']} - portada: {'si' if cover else 'no'}")
        enriched += 1
        time.sleep(0.5)
    except Exception as e:
        print(f"Error {book['title']}: {e}")

print(f"\nEnriquecidos: {enriched} de {len(all_books)}")
