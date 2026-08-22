# GET
def test_create_user(client):
    res = client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com"
        }
    )

    assert res.status_code == 201

    data = res.json()

    assert data["id"] == 1
    assert data["name"] == "test1"
    assert data["email"] == "test1@example.com"


def test_create_user_duplicate_email(client):
    client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com"
        }
    )

    res = client.post(
        "/users",
        json={
            "name": "another test1",
            "email": "test1@example.com"
        }
    )

    assert res.status_code == 400

    assert res.json() == {
        "detail": "Email already registered"
    }


def test_get_users(client):
    client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com"
        }
    )

    client.post(
        "/users",
        json={
            "name": "test2",
            "email": "test2@example.com"
        }
    )

    res = client.get("/users")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 2
    assert data[0]["name"] == "test1"
    assert data[1]["name"] == "test2"


# GET_ID
def test_get_user(client):
    client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com"
        }
    )

    res = client.get("/users/1")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == 1
    assert data["name"] == "test1"
    assert data["email"] == "test1@example.com"


def test_get_user_not_found(client):
    res = client.get("/users/999")

    assert res.status_code == 404

    assert res.json() == {"detail": "User not found"}


# POST
def test_create_users(client):
    res = client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com"
        }
    )
    
    assert res.status_code == 201
    
    data = res.json()
    
    assert data["id"] == 1
    assert data["name"] == "test1"
    assert data["email"] == "test1@example.com"
    
    
# 重複Email
def test_create_user_duplicate_email(client):
    client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com"
        }
    )
    
    res = client.post(
        "/users",
        json={
            "name": "another test1",
            "email": "test1@example.com"
        }
    )
    
    assert res.status_code == 400
    assert res.json() == {"detail": "Email already registered"}