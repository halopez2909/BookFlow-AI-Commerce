import requests
import time

BASE = "http://localhost:8000"
ENRICHMENT = "http://localhost:8004"

# Login
token = requests.post(f"{BASE}/api/auth/login", json={"email":"admin@bookflow.com","password":"admin1234"}).json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Traer todos los libros
all_books = []
page = 1
while True:
    r = requests.get(f"{BASE}/api/catalog/books", params={"page": page, "page_size": 50}, headers=headers)
    data = r.json()
    all_books.extend(data.get("items", []))
    if len(all_books) >= data.get("total", 0):
        break
    page += 1

print(f"Total libros en catalogo: {len(all_books)}")

# Para cada libro buscar su enriquecimiento y actualizar en catalog_db directamente
import psycopg2
catalog_conn = psycopg2.connect("postgresql://bookflow:bookflow123@localhost:5432/catalog_db")
enrichment_conn = psycopg2.connect("postgresql://bookflow:bookflow123@localhost:5432/enrichment_db")

cat_cur = catalog_conn.cursor()
enr_cur = enrichment_conn.cursor()

updated = 0
for book in all_books:
    enr_cur.execute("""
        SELECT cover_url, normalized_description 
        FROM enrichment_results 
        WHERE book_reference = %s 
        ORDER BY created_at DESC LIMIT 1
    """, (book["id"],))
    row = enr_cur.fetchone()
    if row and row[0]:
        cover_url = row[0]
        description = row[1] or book.get("description", "")
        cat_cur.execute("""
            UPDATE books SET cover_url = %s, enriched_flag = true, description = %s
            WHERE id = %s
        """, (cover_url, description, book["id"]))
        print(f"Actualizado: {book['title']} - {cover_url[:50]}")
        updated += 1
    else:
        print(f"Sin portada: {book['title']}")

catalog_conn.commit()
cat_cur.close()
enr_cur.close()
catalog_conn.close()
enrichment_conn.close()
print(f"\nActualizados: {updated} de {len(all_books)}")
