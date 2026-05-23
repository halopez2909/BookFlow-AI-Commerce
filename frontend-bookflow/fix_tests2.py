# Fix CartPage test
with open("src/tests/CartPage.test.tsx", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("/iniciar sesion/i", "/Iniciar sesi/i")
with open("src/tests/CartPage.test.tsx", "w", encoding="utf-8") as f:
    f.write(content)

# Fix OrdersPage test
with open("src/tests/OrdersPage.test.tsx", "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("/iniciar sesion/i", "/Iniciar sesi/i")
with open("src/tests/OrdersPage.test.tsx", "w", encoding="utf-8") as f:
    f.write(content)

# Fix AssistantPage test - add scrollIntoView mock
with open("src/tests/AssistantPage.test.tsx", "r", encoding="utf-8") as f:
    content = f.read()
content = "window.HTMLElement.prototype.scrollIntoView = () => {}\n\n" + content
with open("src/tests/AssistantPage.test.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
