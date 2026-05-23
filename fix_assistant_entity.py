import subprocess

result = subprocess.run([
    "docker", "exec", "bookflow_assistant",
    "cat", "/app/app/application/use_cases.py"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

content = result.stdout

old = '''_STOPWORDS_PREFIX = [
    "tienen", "tienes", "hay", "cuanto cuesta", "cuánto cuesta",
    "cuanto vale", "cuánto vale", "precio de", "cuentame sobre",
    "cuéntame sobre", "hablame de", "háblame de", "informacion sobre",
    "información sobre", "sobre", "libros de", "obras de", "novelas de",
    "buscar", "muéstrame", "muestrame", "el libro", "el", "la", "los",
    "las", "un", "una",
]'''

new = '''_STOPWORDS_PREFIX = [
    "tienen", "tienes", "hay", "cuanto cuesta", "cuánto cuesta",
    "cuanto vale", "cuánto vale", "precio de", "cuentame sobre",
    "cuéntame sobre", "hablame de", "háblame de", "informacion sobre",
    "información sobre", "sobre", "libros de", "obras de", "novelas de",
    "buscar", "muéstrame", "muestrame", "el libro", "el", "la", "los",
    "las", "un", "una", "esta disponible", "está disponible",
    "esta", "está", "cual es el precio de", "cuál es el precio de",
    "que valor tiene", "qué valor tiene", "que precio tiene",
    "qué precio tiene", "me puedes decir el precio de",
    "me puedes decir cuanto cuesta",
]'''

content = content.replace(old, new)

with open("ai-assistant-service/app/application/use_cases.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done" if old in result.stdout else "Pattern not found - check manually")
