import subprocess
import json

# Get all enrichment data with real covers using psql
result = subprocess.run([
    "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "enrichment_db",
    "-t", "-A", "-F", "|",
    "-c", "SELECT req.book_reference, er.cover_url FROM enrichment_results er JOIN enrichment_requests req ON req.id = er.request_id WHERE er.cover_url IS NOT NULL AND er.cover_url != '' AND er.cover_url NOT LIKE '%placeholder%' AND er.cover_url NOT LIKE '%via.placeholder%';"
], capture_output=True, text=True)

rows = [line.strip() for line in result.stdout.strip().split("\n") if "|" in line]
print(f"Portadas reales encontradas: {len(rows)}")

updated = 0
for row in rows:
    parts = row.split("|")
    if len(parts) < 2:
        continue
    book_ref = parts[0].strip()
    cover_url = parts[1].strip()
    
    update_result = subprocess.run([
        "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db",
        "-t", "-A",
        "-c", f"UPDATE books SET cover_url = '{cover_url}', enriched_flag = true WHERE id::text = '{book_ref}' RETURNING title;"
    ], capture_output=True, text=True)
    
    title = update_result.stdout.strip()
    if title:
        print(f"OK: {title} -> {cover_url[:50]}")
        updated += 1

print(f"\nTotal actualizados: {updated}")
