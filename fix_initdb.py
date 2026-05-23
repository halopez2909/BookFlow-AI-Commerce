content = """#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "bookflow" <<-EOSQL
    CREATE DATABASE auth_db;
    CREATE DATABASE catalog_db;
    CREATE DATABASE inventory_db;
    CREATE DATABASE pricing_db;
    CREATE DATABASE enrichment_db;
    CREATE DATABASE assistant_db;
    CREATE DATABASE normalization_db;
    CREATE DATABASE integration_db;
    CREATE DATABASE audit_db;
    CREATE DATABASE order_db;
EOSQL
"""

with open("init-db.sh", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
