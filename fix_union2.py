with open("audit-service/app/domain/schemas.py", "rb") as f:
    content = f.read().decode("utf-8", errors="replace")

content = content.replace(
    "from typing import Optional, List",
    "from typing import Optional, List, Union"
)

with open("audit-service/app/domain/schemas.py", "w", encoding="utf-8") as f:
    f.write(content)

# Verify
with open("audit-service/app/domain/schemas.py", "r", encoding="utf-8") as f:
    first_line = f.readline()
print("First import line:", first_line.strip())
