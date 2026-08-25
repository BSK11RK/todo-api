# GET
def test_get_todos(auth_client):
    auth_client.post(
        "/todos",
        json={
            "title": "Todo 1",
            "completed": False
        }
    )

    auth_client.post(
        "/todos",
        json={
            "title": "Todo 2",
            "completed": True
        }
    )

    res = auth_client.get("/todos")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"


# GET_ID
def test_get_todo(auth_client):
    create_res = auth_client.post(
        "/todos",
        json={
            "title": "取得テスト",
            "completed": False
        }
    )

    todo_id = create_res.json()["id"]

    res = auth_client.get(f"/todos/{todo_id}")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == todo_id
    assert data["title"] == "取得テスト"
    assert data["completed"] is False


# 存在しないTodo
def test_get_todo_not_found(auth_client):
    res = auth_client.get("/todos/999")

    assert res.status_code == 404

    data = res.json()

    assert data["detail"] == "Todo not found"


# 検索
def test_search_todos(auth_client):
    auth_client.post(
        "/todos",
        json={
            "title": "FastAPIを勉強する",
            "description": "APIを作る",
            "completed": False
        }
    )

    auth_client.post(
        "/todos",
        json={
            "title": "Pythonを勉強する",
            "description": "Python 基礎",
            "completed": False
        }
    )

    auth_client.post(
        "/todos",
        json={
            "title": "FastAPIでToDoを作る",
            "description": "ToDo API",
            "completed": False
        }
    )

    res = auth_client.get("/todos?keyword=FastAPI")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 2
    assert data[0]["title"] == "FastAPIを勉強する"
    assert data[1]["title"] == "FastAPIでToDoを作る"


# completed
def test_filter_todos_by_completed(auth_client):
    auth_client.post(
        "/todos",
        json={
            "title": "未完了のtodo",
            "description": "まだ終わっていない",
            "completed": False
        }
    )

    auth_client.post(
        "/todos",
        json={
            "title": "完了したTodo",
            "description": "終わった",
            "completed": True
        }
    )

    res = auth_client.get("/todos?completed=true")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1
    assert data[0]["title"] == "完了したTodo"
    assert data[0]["completed"] is True


# 検索とcompleted
def test_search_and_filter_todos(auth_client):
    auth_client.post(
        "/todos",
        json={
            "title": "FastAPIを勉強する",
            "description": "未完了",
            "completed": False
        }
    )

    auth_client.post(
        "/todos",
        json={
            "title": "FastAPIを完成させる",
            "description": "完了済み",
            "completed": True
        }
    )

    auth_client.post(
        "/todos",
        json={
            "title": "Pythonを勉強する",
            "description": "未完了",
            "completed": False
        }
    )

    res = auth_client.get("/todos?keyword=FastAPI&completed=False")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1
    assert data[0]["title"] == "FastAPIを勉強する"


# ページネーション
def test_pagination(auth_client):
    for i in range(10):
        auth_client.post(
            "/todos",
            json={
                "title": f"Todo {i + 1}",
                "description": None,
                "completed": False
            }
        )

    res = auth_client.get("/todos?skip=0&limit=5")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 5
    assert data[0]["title"] == "Todo 1"
    assert data[4]["title"] == "Todo 5"


def test_pagination_skip(auth_client):
    for i in range(10):
        auth_client.post(
            "/todos",
            json={
                "title": f"Todo {i + 1}",
                "description": None,
                "completed": False
            }
        )

    res = auth_client.get("/todos?skip=5&limit=5")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 5
    assert data[0]["title"] == "Todo 6"
    assert data[4]["title"] == "Todo 10"


# limit
def test_pagination_limit_validation(auth_client):
    res = auth_client.get("/todos?limit=0")

    assert res.status_code == 422


def test_pagination_limit_max(auth_client):
    res = auth_client.get("/todos?limit=101")

    assert res.status_code == 422


# POST
def test_create_todo(auth_client):
    res = auth_client.post(
        "/todos",
        json={
            "title": "FastAPIを勉強する",
            "description": "pytestをやる",
            "completed": False
        }
    )

    assert res.status_code == 201

    data = res.json()

    assert data["id"] == 1
    assert data["title"] == "FastAPIを勉強する"
    assert data["description"] == "pytestをやる"
    assert data["completed"] is False
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


# PUT
def test_update_todo(auth_client):
    create_res = auth_client.post(
        "/todos",
        json={
            "title": "変更前",
            "completed": False
        }
    )

    todo_id = create_res.json()["id"]

    res = auth_client.put(
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


def test_update_todo_not_found(auth_client):
    res = auth_client.put(
        "/todos/999",
        json={
            "title": "存在しないTodo",
            "description": "テスト",
            "completed": False
        }
    )

    assert res.status_code == 404

    assert res.json() == {"detail": "Todo not found"}


# PATCH
def test_patch_todo(auth_client):
    create_res = auth_client.post(
        "/todos",
        json={
            "title": "元のタイトル",
            "description": "元の説明",
            "completed": False
        }
    )

    todo_id = create_res.json()["id"]

    res = auth_client.patch(
        f"/todos/{todo_id}",
        json={
            "description": "新しい説明"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == todo_id
    assert data["title"] == "元のタイトル"
    assert data["description"] == "新しい説明"
    assert data["completed"] is False


def test_patch_todo_not_found(auth_client):
    res = auth_client.patch(
        "/todos/999",
        json={
            "title": "存在しないTodo"
        }
    )

    assert res.status_code == 404

    assert res.json() == {"detail": "Todo not found"}


# DELETE
def test_delete_todo(auth_client):
    create_res = auth_client.post(
        "/todos",
        json={
            "title": "削除するTodo",
            "completed": False
        }
    )

    todo_id = create_res.json()["id"]

    res = auth_client.delete(f"/todos/{todo_id}")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == todo_id
    assert data["title"] == "削除するTodo"

    get_res = auth_client.get(f"/todos/{todo_id}")

    assert get_res.status_code == 404


def test_delete_todo_not_found(auth_client):
    res = auth_client.delete("/todos/999")

    assert res.status_code == 404

    assert res.json() == {"detail": "Todo not found"}