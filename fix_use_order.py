with open("frontend-bookflow/src/hooks/useOrders.ts", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "    enabled: !!orderId,\n    staleTime: 1000 * 30,",
    "    enabled: !!orderId,\n    staleTime: 0,\n    refetchOnWindowFocus: true,"
)

with open("frontend-bookflow/src/hooks/useOrders.ts", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
