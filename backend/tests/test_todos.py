from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.todo import Todo


def test_create_todo(client: TestClient):
    response = client.post("/todos", json={"title": "牛乳を買う"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "牛乳を買う"
    assert data["completed"] is False
    assert data["description"] is None
    assert data["id"] is not None


def test_create_todo_with_empty_title(client: TestClient):
    response = client.post("/todos", json={"title": ""})

    assert response.status_code == 422


def test_read_todos(client: TestClient, session: Session):
    session.add(Todo(title="1件目"))
    session.add(Todo(title="2件目"))
    session.commit()

    response = client.get("/todos")

    assert response.status_code == 200
    assert [todo["title"] for todo in response.json()] == ["1件目", "2件目"]


def test_read_todos_with_limit(client: TestClient, session: Session):
    for i in range(3):
        session.add(Todo(title=f"ToDo {i}"))
    session.commit()

    response = client.get("/todos", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    assert [todo["title"] for todo in response.json()] == ["ToDo 1"]


def test_read_todo(client: TestClient, session: Session):
    todo = Todo(title="牛乳を買う")
    session.add(todo)
    session.commit()

    response = client.get(f"/todos/{todo.id}")

    assert response.status_code == 200
    assert response.json()["title"] == "牛乳を買う"


def test_read_todo_not_found(client: TestClient):
    response = client.get("/todos/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo(client: TestClient, session: Session):
    todo = Todo(title="牛乳を買う")
    session.add(todo)
    session.commit()

    response = client.patch(f"/todos/{todo.id}", json={"completed": True})

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    # 送らなかった項目は変わらない
    assert data["title"] == "牛乳を買う"


def test_update_todo_not_found(client: TestClient):
    response = client.patch("/todos/999", json={"completed": True})

    assert response.status_code == 404


def test_delete_todo(client: TestClient, session: Session):
    todo = Todo(title="牛乳を買う")
    session.add(todo)
    session.commit()

    response = client.delete(f"/todos/{todo.id}")

    assert response.status_code == 204
    assert session.get(Todo, todo.id) is None


def test_delete_todo_not_found(client: TestClient):
    response = client.delete("/todos/999")

    assert response.status_code == 404
