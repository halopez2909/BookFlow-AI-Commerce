import subprocess

# Get all enrichment data with real authors
result = subprocess.run([
    "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "enrichment_db",
    "-t", "-A", "-F", "|||",
    "-c", "SELECT req.book_reference, er.normalized_author, er.normalized_description FROM enrichment_results er JOIN enrichment_requests req ON req.id = er.request_id WHERE length(req.book_reference) = 36 AND er.normalized_author IS NOT NULL AND er.normalized_author != '';"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

rows = [line.strip() for line in result.stdout.strip().split("\n") if "|||" in line]
print(f"Registros encontrados: {len(rows)}")

updated = 0
for row in rows:
    parts = row.split("|||")
    if len(parts) < 2:
        continue
    book_ref = parts[0].strip()
    author = parts[1].strip().replace("'", "''")
    description = parts[2].strip().replace("'", "''") if len(parts) > 2 and parts[2].strip() else None

    if description:
        sql = f"UPDATE books SET author = '{author}', description = '{description}' WHERE id::text = '{book_ref}' AND (author = 'Autor Desconocido' OR author IS NULL) RETURNING title;"
    else:
        sql = f"UPDATE books SET author = '{author}' WHERE id::text = '{book_ref}' AND (author = 'Autor Desconocido' OR author IS NULL) RETURNING title;"

    update_result = subprocess.run([
        "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db",
        "-t", "-A", "-c", sql
    ], capture_output=True, text=True, encoding="utf-8", errors="replace")

    title = (update_result.stdout or "").strip()
    if "UPDATE 1" in title or (title and "UPDATE" not in title):
        print(f"OK: {book_ref[:8]}... autor: {author[:40]}")
        updated += 1

print(f"\nTotal actualizados: {updated}")
