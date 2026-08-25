import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite://"


engine =create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        
        
@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally: 
            pass
        
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()
    
    
# 認証済みClient
@pytest.fixture
def auth_client(client):
    # テスト用Userを作成
    res = client.post(
        "/users",
        json={
            "name": "test1",
            "email": "test1@example.com",
            "password": "test1234"
        }
    )
    
    assert res.status_code == 201
    
    # ログイン
    res = client.post(
        "/auth/login",
        data={
            "username": "test1@example.com",
            "password": "test1234"
        }
    )
    
    assert res.status_code == 200
    
    token = res.json()["access_token"]
    
    # JWTを付けたClient
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client