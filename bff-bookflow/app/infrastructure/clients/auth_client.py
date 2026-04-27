import os
import httpx
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = os.getenv("AUTH_URL")


class AuthClient:

    async def login(self, email: str, password: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AUTH_URL}/auth/login", json={"email": email, "password": password})
            response.raise_for_status()
            return response.json()

    async def register(self, email: str, password: str, role: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AUTH_URL}/auth/register", json={"email": email, "password": password, "role": role})
            response.raise_for_status()
            return response.json()

    async def get_me(self, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{AUTH_URL}/auth/me", headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()
