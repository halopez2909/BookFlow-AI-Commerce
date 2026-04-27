#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "bookflow" <<-EOSQL
    CREATE DATABASE auth_db;
    CREATE DATABASE catalog_db;
    CREATE DATABASE inventory_db;
    CREATE DATABASE pricing_db;
    CREATE DATABASE enrichment_db;
    CREATE DATABASE assistant_db;
EOSQL
