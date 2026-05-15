import requests
import time

BASE = "http://localhost:8000"
PRICING = "http://localhost:8008"

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

print(f"Total libros: {len(all_books)}")

conditions = ["new", "good", "worn", "good", "new"]
categories = ["fiction", "technical", "science", "literature", "philosophy"]

calculated = 0
for i, book in enumerate(all_books):
    condition = conditions[i % len(conditions)]
    category = categories[i % len(categories)]
    payload = {
        "book_reference": book["id"],
        "isbn": book.get("isbn", ""),
        "condition": condition,
        "category": category,
        "title": book["title"]
    }
    try:
        r = requests.post(f"{PRICING}/pricing/calculate", json=payload, timeout=10)
        if r.status_code in [200, 201]:
            price = r.json().get("suggested_price", 0)
            print(f"OK: {book['title'][:40]} -> ${price}")
            calculated += 1
        else:
            print(f"Error {r.status_code}: {book['title'][:40]}")
        time.sleep(0.2)
    except Exception as e:
        print(f"Error: {book['title'][:40]} - {e}")

print(f"\nCalculados: {calculated} de {len(all_books)}")
