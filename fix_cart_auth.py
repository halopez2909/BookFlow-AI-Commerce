with open("frontend-bookflow/src/pages/cart/CartPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix handleConfirmOrder to check auth first
old = """  async function handleConfirmOrder() {
    if (!cart || cart.items.length === 0) return
    setConfirming(true)"""

new = """  async function handleConfirmOrder() {
    if (!cart || cart.items.length === 0) return
    if (!state.isAuthenticated) {
      navigate('/login')
      return
    }
    setConfirming(true)"""

content = content.replace(old, new)

with open("frontend-bookflow/src/pages/cart/CartPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
