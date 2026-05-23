import subprocess

result = subprocess.run([
    "docker", "exec", "bookflow_assistant",
    "cat", "/app/app/domain/intents.py"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

content = result.stdout

# Add recommendation keywords to BOOK_SEARCH
old = '''        "qué libros", "que libros",
    ],
}'''

new = '''        "qué libros", "que libros",
        "recomienda", "recomiéndame", "sugiere", "sugiéreme",
        "qué me recomiendas", "que recomiendas", "similar", "parecido",
        "alternativa", "otro libro", "otros libros",
    ],
}'''

content = content.replace(old, new)

with open("ai-assistant-service/app/domain/intents.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
