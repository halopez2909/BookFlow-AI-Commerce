import requests, time

BFF = "http://localhost:8000"

def log(msg): print(f"  {msg}")

def register_users():
    users = [
        {"email": "admin@bookflow.com", "password": "admin123", "role": "admin"},
        {"email": "cliente@bookflow.com", "password": "cliente123", "role": "user"},
    ]
    for u in users:
        try:
            r = requests.post(f"{BFF}/api/auth/register", json=u, timeout=5)
            log(f"Usuario: {u['email']} - {'OK' if r.status_code in [200,201,409] else r.text}")
        except Exception as e:
            log(f"Error usuario: {e}")

def check_health():
    try:
        r = requests.get(f"{BFF}/api/system/health", timeout=10)
        data = r.json()
        ok = sum(1 for s in data.get("services",{}).values() if s.get("status")=="ok")
        total = len(data.get("services",{}))
        log(f"Health: {ok}/{total} servicios OK")
        return ok == total
    except Exception as e:
        log(f"Health error: {e}")
        return False

def main():
    print("BookFlow AI Commerce - Seed Data Sprint 3")
    print("=" * 50)
    print("Verificando servicios...")
    if not check_health():
        print("ADVERTENCIA: Algunos servicios no responden")
    print("Registrando usuarios demo...")
    register_users()
    print("=" * 50)
    print("Seed completado!")
    print("  admin@bookflow.com / admin123")
    print("  cliente@bookflow.com / cliente123")

if __name__ == "__main__":
    main()
