import subprocess

# Get all pricing decisions
result = subprocess.run([
    "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "pricing_db",
    "-t", "-A", "-F", "|",
    "-c", "SELECT book_reference, suggested_price FROM pricing_decisions WHERE length(book_reference) = 36;"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

rows = [line.strip() for line in result.stdout.strip().split("\n") if "|" in line]
print(f"Precios encontrados: {len(rows)}")

updated = 0
for row in rows:
    parts = row.split("|")
    if len(parts) < 2:
        continue
    book_ref = parts[0].strip()
    price = parts[1].strip()
    if not price:
        continue

    update_result = subprocess.run([
        "docker", "exec", "bookflow_postgres", "psql", "-U", "bookflow", "-d", "catalog_db",
        "-t", "-A",
        "-c", f"UPDATE books SET suggested_price = {price} WHERE id::text = '{book_ref}' RETURNING title;"
    ], capture_output=True, text=True, encoding="utf-8", errors="replace")

    title = (update_result.stdout or "").strip()
    if title:
        print(f"OK: precio {price} -> {book_ref[:8]}...")
        updated += 1

print(f"\nTotal con precio: {updated}")
