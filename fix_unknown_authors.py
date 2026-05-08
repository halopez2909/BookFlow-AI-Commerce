import requests
import subprocess
import time

BASE = "http://localhost:8000"
ENRICH = "http://localhost:8004"

token = requests.post(f"{BASE}/api/auth/login", json={"email":"admin@bookflow.com","password":"admin1234"}).json()["access_token"]

unknown_books = [
    ("37fef084-109d-4c99-b202-ea16dda73009", "Sistemas de energia fotovoltaica manual del instalador", "9788495693440"),
    ("a78c5e8b-2db5-409a-bfc5-ccc6b4553be2", "BIOLOGIA LA UNIDAD Y LA DIVERSIDAD DE LA VIDA", "9786074811377"),
    ("47ae8e85-76ea-4426-998e-ab6154cf1bf7", "La energia solar aplicaciones practicas", "9788495693501"),
    ("a43cfc0b-8fde-4014-a7aa-ede01169c889", "Fotovoltaica para profesionales", "9788495693358"),
    ("c1e1e660-a3ca-4ef6-a954-729c35ae593b", "Energia Solar Fotovoltaica", "9788495693471"),
    ("83a842cd-8b69-4c6c-84d8-ab4566997527", "Manual de Urgencias Cardiovasculares", ""),
    ("4d0f7867-834a-4cbc-bda7-94bd13a0e07e", "ARTROSIS Y ARTRITIS", "9788480190404"),
    ("5ffd811d-fc15-4400-b23f-af4cd09e50dd", "Biomecanica Del Aparato Locomotor", "9782481740677"),
    ("b59e166e-9b35-40fe-9566-aeacc8344e6a", "Clinicas Medicas de Norteamerica", "9701030869"),
    ("20a0a99e-b7f2-4ba2-9de1-8bea8523dbd0", "Radiacion Solar y dispositivos fotovoltaicos", "9788495693310"),
    ("acfe820d-5b6b-4c56-bb7c-658886019504", "Clinical Approach to Infection in the Compromised Host", "9780306466939"),
    ("64c7cc18-bbaa-4eae-9337-c0bb8493d2de", "Medicina Laboratorio Vol 17 2011", ""),
    ("8f1384fb-40cc-4d65-9d34-c461b90a60de", "Futbol Preparacion Fisica En El Futbol", "9788480196680"),
    ("f4d19d3b-ce2d-4ab0-bb0f-a049470aa4cf", "Futbol Como y cuando entrenar la resistencia", "9788499100692"),
    ("de49ebd9-51f0-4956-a797-193d9e8b9305", "TRATADO DE NATACION De la iniciacion al perfeccionamiento", "9788480199544"),
]

for book_id, title, isbn in unknown_books:
    payload = {"book_reference": book_id, "title": title, "author": "", "isbn": isbn}
    try:
        r = requests.post(f"{ENRICH}/enrichment/enrich", json=payload, timeout=15)
        result = r.json()
        author = result.get("normalized_author", "")
        if author and author != "Autor Desconocido":
            author_sql = author.replace("'", "''")
            sql = f"UPDATE books SET author = '{author_sql}' WHERE id::text = '{book_id}';"
            subprocess.run([
                "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db",
                "-t", "-A", "-c", sql
            ], capture_output=True, text=True, encoding="utf-8", errors="replace")
            print(f"OK: {title[:40]} -> {author[:40]}")
        else:
            print(f"Sin autor: {title[:40]}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error: {title[:40]} - {e}")

print("Done")
