import requests
import subprocess
import time

BASE = "http://localhost:8000"
ENRICH = "http://localhost:8004"
PRICING = "http://localhost:8008"

# Login
print("Haciendo login...")
token = requests.post(f"{BASE}/api/auth/login", json={"email":"admin@bookflow.com","password":"admin1234"}).json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Traer todos los libros
print("Obteniendo libros...")
all_books = []
page = 1
while True:
    r = requests.get(f"{BASE}/api/catalog/books", params={"page": page, "page_size": 50}, headers=headers)
    data = r.json()
    items = data.get("items", [])
    if not items:
        break
    all_books.extend(items)
    if len(all_books) >= data.get("total", 0):
        break
    page += 1

print(f"Total libros: {len(all_books)}")

if len(all_books) == 0:
    print("ERROR: No hay libros en la BD. Necesitas cargar el dataset primero.")
    exit(1)

# Enriquecer libros
print("\nEnriqueciendo libros con IA...")
enriched = 0
for book in all_books:
    if book.get("cover_url"):
        continue
    payload = {"book_reference": book["id"], "title": book["title"], "author": book["author"], "isbn": book.get("isbn", "")}
    try:
        r = requests.post(f"{ENRICH}/enrichment/enrich", json=payload, timeout=15)
        if r.status_code in [200, 201]:
            result = r.json()
            cover = result.get("cover_url", "")
            author = result.get("normalized_author", "")
            # Update cover in catalog
            if cover and "placeholder" not in cover:
                subprocess.run(["docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db", "-t", "-A",
                    "-c", f"UPDATE books SET cover_url = '{cover}', enriched_flag = true WHERE id::text = '{book['id']}';"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
            # Update author
            if author and author != "Autor Desconocido":
                author_sql = author.replace("'", "''")
                subprocess.run(["docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db", "-t", "-A",
                    "-c", f"UPDATE books SET author = '{author_sql}' WHERE id::text = '{book['id']}' AND (author = 'Autor Desconocido' OR author IS NULL);"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
            enriched += 1
            print(f"OK: {book['title'][:40]}")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error: {book['title'][:30]} - {e}")

print(f"\nEnriquecidos: {enriched}")

# Calcular precios
print("\nCalculando precios...")
conditions = ["new", "good", "worn", "good", "new"]
categories = ["fiction", "technical", "science", "literature", "philosophy"]
calculated = 0
for i, book in enumerate(all_books):
    payload = {"book_reference": book["id"], "isbn": book.get("isbn", ""), "condition": conditions[i % 5], "category": categories[i % 5], "title": book["title"]}
    try:
        r = requests.post(f"{PRICING}/pricing/calculate", json=payload, timeout=10)
        if r.status_code in [200, 201]:
            price = r.json().get("suggested_price", 0)
            subprocess.run(["docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db", "-t", "-A",
                "-c", f"UPDATE books SET suggested_price = {price} WHERE id::text = '{book['id']}';"],
                capture_output=True, text=True, encoding="utf-8", errors="replace")
            calculated += 1
        time.sleep(0.2)
    except Exception as e:
        print(f"Error precio: {book['title'][:30]}")

print(f"Precios calculados: {calculated}")
print("\nListo! Recarga http://localhost:3000/catalog")
