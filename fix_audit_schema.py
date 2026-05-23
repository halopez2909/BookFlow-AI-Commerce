with open("audit-service/app/domain/schemas.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Fix CartHistoryItem to use Union[uuid.UUID, int] for id
old = """class CartHistoryItem(BaseModel):
    id: uuid.UUID
    customer_id: str"""

new = """class CartHistoryItem(BaseModel):
    id: Union[uuid.UUID, int, str]
    customer_id: str"""

content = content.replace(old, new)

# Make sure Union is imported
if "from typing import" in content and "Union" not in content:
    content = content.replace("from typing import", "from typing import Union,")

with open("audit-service/app/domain/schemas.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
