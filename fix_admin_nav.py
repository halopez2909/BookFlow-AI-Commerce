content = open("frontend-bookflow/src/pages/admin/AdminBatches.tsx", encoding="utf-8").read()

nav = """    <>
    <div style={{ padding: "8px 16px", background: "#1E6FBC", display: "flex", gap: 16, alignItems: "center" }}>
      <span style={{ color: "white", fontWeight: "bold" }}>Admin Panel</span>
      <button onClick={() => navigate("/admin/batches")} style={{ background: "transparent", border: "none", color: "white", cursor: "pointer", fontWeight: "bold" }}>Inventario</button>
      <button onClick={() => navigate("/admin/pricing")} style={{ background: "transparent", border: "none", color: "white", cursor: "pointer", fontWeight: "bold" }}>Pricing</button>
      <button onClick={() => navigate("/admin/config")} style={{ background: "transparent", border: "none", color: "white", cursor: "pointer", fontWeight: "bold" }}>Config</button>
      <span style={{ marginLeft: "auto" }}><a href="/catalog" style={{ color: "white", fontSize: 12 }}>Ver catalogo</a></span>
    </div>
    <div>"""

content = content.replace("  return (", "  return (\n" + nav)
content = content.replace("  )\n}", "    </div>\n    </>\n  )\n}")

open("frontend-bookflow/src/pages/admin/AdminBatches.tsx", "w", encoding="utf-8").write(content)
print("Done")
