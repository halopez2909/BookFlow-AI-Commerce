content = "#!/bin/bash\nset -e\npsql -v ON_ERROR_STOP=1 --username \"bookflow\" <<-EOSQL\n    CREATE DATABASE auth_db;\n    CREATE DATABASE catalog_db;\n    CREATE DATABASE inventory_db;\n    CREATE DATABASE pricing_db;\n    CREATE DATABASE enrichment_db;\n    CREATE DATABASE normalization_db;\n    CREATE DATABASE integration_db;\n    CREATE DATABASE audit_db;\n    CREATE DATABASE order_db;\nEOSQL\n"
with open("init-db.sh", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done")
