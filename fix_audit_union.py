with open("audit-service/app/domain/schemas.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Fix Union import
if "from typing import" in content and "Union" not in content:
    content = content.replace("from typing import List", "from typing import List, Union")
elif "Union" not in content:
    content = "from typing import Union\n" + content

with open("audit-service/app/domain/schemas.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
