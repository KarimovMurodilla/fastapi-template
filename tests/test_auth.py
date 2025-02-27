from httpx import AsyncClient


async def test_register_user(async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "string", "name": "Test User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["is_active"] is True
    assert data["is_superuser"] is False
    assert data["is_verified"] is False


async def test_login_user(async_client: AsyncClient):
    # Сначала регистрируем пользователя
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "string", "name": "Test User"},
    )

    # Пытаемся залогиниться
    response = await async_client.post(
        "/auth/jwt/login",
        data={
            "username": "test@example.com",
            "password": "string",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
