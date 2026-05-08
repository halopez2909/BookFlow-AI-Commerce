with open("src/hooks/usePricingRecalculate.ts", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "const useMocks =\n  (import.meta.env.VITE_PRICING_USE_MOCKS as string | undefined) === 'true'",
    "const useMocks = true"
)

with open("src/hooks/usePricingRecalculate.ts", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
