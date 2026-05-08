import os

hooks = [
    "src/hooks/usePricingList.ts",
    "src/hooks/usePricingDetail.ts", 
    "src/hooks/usePricingOverride.ts",
    "src/hooks/usePricingRecalculate.ts",
]

for hook in hooks:
    try:
        with open(hook, "r", encoding="utf-8") as f:
            content = f.read()
        
        old = "const useMocks =\n  (import.meta.env.VITE_PRICING_USE_MOCKS as string | undefined) === 'true'"
        new = "const useMocks = true"
        
        if old in content:
            content = content.replace(old, new)
            with open(hook, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {hook}")
        elif "const useMocks = true" in content:
            print(f"Already fixed: {hook}")
        else:
            print(f"Pattern not found: {hook}")
    except Exception as e:
        print(f"Error {hook}: {e}")
