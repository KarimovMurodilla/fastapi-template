from httpx import AsyncClient


async def test_get_user(ac: AsyncClient):
    response = await ac.get("/users/id/1")

    assert response.json() == {
        "id": 1,
        "name": "test",
        "email": "test@gmail.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }

    assert response.status_code == 200


async def test_get_user_by_name(ac: AsyncClient):
    response = await ac.get("/users/name/test")

    assert response.json()['id'] == 1
    assert response.status_code == 200


async def test_get_all_users(ac: AsyncClient):
    response = await ac.get("/users/all")

    assert len(response.json()) == 1
    assert response.status_code == 200


async def test_find_users_by_name(ac: AsyncClient):
    response = await ac.get("/users/filter?name=test")

    assert len(response.json()) == 1
    assert response.status_code == 200


async def test_edit_user(ac: AsyncClient):
    response1 = await ac.patch("/users/edit?id=1", json={
        "name": "new name",
        "email": "changed@gmail.com",
        "password": "pass_changed",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    })

    response2 = await ac.get("/users/id/1")

    assert response2.json()['name'] == "new name"
    assert response2.json()['email'] == "changed@gmail.com"
    assert response1.status_code == 200


async def test_delete_user(ac: AsyncClient):
    response = await ac.delete("/users/delete?id=1")
    users = await ac.get("/users/id/1")

    assert users.json() is None
    assert response.status_code == 200