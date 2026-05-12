with open("frontend-bookflow/src/components/pricing/PricingTable.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "p.sources.length > 0\n                    ? p.sources.map((s) => s.name).join(', ')\n                    : '-'",
    "p.reference_count && p.reference_count > 0 ? `${p.reference_count} fuente(s)` : '-'"
)

with open("frontend-bookflow/src/components/pricing/PricingTable.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
