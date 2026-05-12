import subprocess

result = subprocess.run([
    "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "enrichment_db",
    "-t", "-A", "-F", "|",
    "-c", "SELECT req.book_reference, er.cover_url FROM enrichment_results er JOIN enrichment_requests req ON req.id = er.request_id WHERE er.cover_url IS NOT NULL AND er.cover_url NOT LIKE '" + "%" + "placeholder" + "%" + "' AND length(req.book_reference) = 36;"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

rows = [line.strip() for line in result.stdout.strip().split("\n") if "|" in line]
print(f"Portadas encontradas: {len(rows)}")

updated = 0
for row in rows:
    parts = row.split("|")
    if len(parts) < 2:
        continue
    book_ref = parts[0].strip()
    cover_url = parts[1].strip()
    if not cover_url:
        continue

    update_result = subprocess.run([
        "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db",
        "-t", "-A",
        "-c", f"UPDATE books SET cover_url = '{cover_url}', enriched_flag = true WHERE id::text = '{book_ref}' RETURNING title;"
    ], capture_output=True, text=True, encoding="utf-8", errors="replace")

    title = (update_result.stdout or "").strip()
    if "UPDATE 1" in title or title:
        print(f"OK: {book_ref[:8]}... -> portada actualizada")
        updated += 1

print(f"\nTotal actualizados: {updated}")
