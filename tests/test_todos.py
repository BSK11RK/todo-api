# GET
def test_get_todos(client):
    client.post(
       "/todos",
        json={
            "title": "Todo 1",
            "completed": False
        }
    )
    
    client.post(
        "/todos",
        json={
            "title": "Todo 2",
            "completed": True
        }
    )
    
    res = client.get("/todos")
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"
    
    
# GET_ID
def test_get_todo(client):
    create_res = client.post(
        "/todos",
        json={
            "title": "取得テスト",
            "completed": False
        }
    )
    
    todo_id = create_res.json()["id"]
    
    res = client.get(f"/todos/{todo_id}")
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert data["id"] == todo_id
    assert data["title"] == "取得テスト"
    assert data["completed"] is False
    
    
# 存在しないTodo
def test_get_todo_not_found(client):
    res = client.get("/todos/999")
    
    assert res.status_code == 404
    
    data = res.json()
    
    assert data["detail"] == "Todo not found"


# POST
def test_create_todo(client):
    res = client.post(
        "/todos",
        json={
            "title": "FastAPIを勉強する",
            "completed": False
        }
    )
    
    assert res.status_code == 201
    
    data = res.json()
    
    assert data["id"] == 1
    assert data["title"] == "FastAPIを勉強する"
    assert data["completed"] is False
    
    
# PUT
def test_update_todo(client):
    create_res = client.post(
        "/todos",
        json={
            "title": "変更前",
            "completed": False
        }
    )
    
    todo_id = create_res.json()["id"]
    
    res = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "変更後",
            "completed": True
        }
    )
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert data["id"] == todo_id
    assert data["title"] == "変更後"
    assert data["completed"] is True
    
    
# PATCH
def test_patch_todo(client):
    create_res = client.post(
        "/todos",
        json={
            "title": "元のタイトル",
            "completed": False
        }
    )
    
    todo_id = create_res.json()["id"]
    
    res = client.patch(
        f"/todos/{todo_id}",
        json={"completed": True}
    )
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert data["id"] == todo_id
    assert data["title"] == "元のタイトル"
    assert data["completed"] is True
    
    
# DELETE
def test_delete_todo(client):
    create_res = client.post(
        "/todos",
        json={
            "title": "削除するTodo",
            "completed": False
        }
    )
    
    todo_id = create_res.json()["id"]
    
    res = client.delete(f"/todos/{todo_id}")
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert data["id"] == todo_id
    assert data["title"] == "削除するTodo"
    
    get_res = client.get(f"/todos/{todo_id}")
    
    assert get_res.status_code == 404