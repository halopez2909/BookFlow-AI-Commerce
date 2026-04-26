import openpyxl
import httpx
import asyncio

CATALOG_URL = "http://localhost:8003"

async def load_dataset():
    wb = openpyxl.load_workbook('Dataset_Bookflow.xlsx', read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = rows[0]
    data_rows = rows[1:51]
    print(f"Cargando {len(data_rows)} libros del dataset de la profe...")

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{CATALOG_URL}/catalog/categories")
        categories = r.json()
        if not categories:
            r = await client.post(f"{CATALOG_URL}/catalog/categories", json={"name": "General", "description": "Categoria general"})
            category_id = r.json()["id"]
        else:
            category_id = categories[0]["id"]
        print(f"Usando categoria: {category_id}")

    registered = 0
    skipped = 0

    async with httpx.AsyncClient(timeout=30) as client:
        for row in data_rows:
            try:
                title = str(row[0]) if row[0] else None
                isbn13 = str(int(row[1])) if row[1] else None
                issn = str(row[3]) if row[3] else None
                condition = str(row[4]).lower() if row[4] else "new"
                observations = str(row[6]) if row[6] else None
                cover_url = str(row[9]) if row[9] else None

                if not title:
                    skipped += 1
                    continue

                condition_map = {
                    "nuevo": "new", "new": "new",
                    "bueno": "good", "good": "good",
                    "desgastado": "worn", "worn": "worn",
                    "danado": "damaged", "damaged": "damaged",
                    "nuevo - muestra": "new",
                }
                mapped_condition = "new"
                for key, val in condition_map.items():
                    if key.lower() in condition.lower():
                        mapped_condition = val
                        break

                book_data = {
                    "title": title[:200],
                    "author": "Autor Desconocido",
                    "publisher": "BookFlow Import",
                    "category_id": category_id,
                    "description": observations if observations and observations != "None" else None,
                }
                if isbn13 and len(isbn13) in [10, 13]:
                    book_data["isbn"] = isbn13
                if cover_url and cover_url != "None":
                    book_data["cover_url"] = cover_url

                r = await client.post(f"{CATALOG_URL}/catalog/books", json=book_data)
                if r.status_code == 201:
                    book_id = r.json()["id"]
                    await client.post(f"{CATALOG_URL}/catalog/books/{book_id}/publish")
                    registered += 1
                    print(f"  OK: {title[:60]}")
                else:
                    skipped += 1
                    print(f"  SKIP ({r.status_code}): {title[:40]}")
            except Exception as e:
                skipped += 1
                print(f"  ERROR: {str(e)[:60]}")

    print(f"\nResultado final: {registered} registrados, {skipped} omitidos")

asyncio.run(load_dataset())
