for f in ["src/tests/CartPage.test.tsx", "src/tests/OrdersPage.test.tsx"]:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    content = content.replace(
        "expect(screen.getByText(/Iniciar sesi/i)).toBeDefined()",
        "expect(screen.getAllByText(/Iniciar sesi/i).length).toBeGreaterThan(0)"
    )
    with open(f, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Fixed: {f}")
