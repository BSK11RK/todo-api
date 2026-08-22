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