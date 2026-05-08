import subprocess

result = subprocess.run([
    "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "enrichment_db",
    "-t", "-A", "-F", "|||",
    "-c", "SELECT req.book_reference, er.normalized_description FROM enrichment_results er JOIN enrichment_requests req ON req.id = er.request_id WHERE length(req.book_reference) = 36 AND er.normalized_description IS NOT NULL AND er.normalized_description != '';"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

rows = [line.strip() for line in result.stdout.strip().split("\n") if "|||" in line]
print(f"Descripciones encontradas: {len(rows)}")

updated = 0
for row in rows:
    parts = row.split("|||")
    if len(parts) < 2:
        continue
    book_ref = parts[0].strip()
    description = parts[1].strip().replace("'", "''")
    if not description:
        continue

    sql = f"UPDATE books SET description = '{description}' WHERE id::text = '{book_ref}' RETURNING title;"
    update_result = subprocess.run([
        "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db",
        "-t", "-A", "-c", sql
    ], capture_output=True, text=True, encoding="utf-8", errors="replace")

    title = (update_result.stdout or "").strip()
    if title:
        print(f"OK: {book_ref[:8]}...")
        updated += 1

print(f"\nTotal con descripcion: {updated}")
