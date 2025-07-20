import pytest
from fastapi.testclient import TestClient
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)

client = TestClient(app)

def test_signup_and_login_and_profile(monkeypatch):
    # Dummy user data - use unique email with timestamp to avoid conflicts
    import time
    timestamp = str(int(time.time()))
    email = f"test{timestamp}@example.com"
    password = "Secret123!"
    full_name = "Test User"
    role = "student"  # Changed from "user" to "student" (valid enum value)
    confirm_password = "Secret123!"
    terms_agreed = True

    # Mock supabase responses for signup
    class DummyUser:
        def __init__(self):
            self.id = "dummy-user-id"
        
        def get(self, key):
            return getattr(self, key, None)
    
    class DummySession:
        def __init__(self):
            self.access_token = "dummy-access-token"
        
        def get(self, key):
            return getattr(self, key, None)
    
    class DummySignUpResult:
        def __init__(self):
            self.user = DummyUser()
    
    class DummySignInResult:
        def __init__(self):
            self.session = DummySession()
    
    class DummyGetUserResult:
        def __init__(self):
            self.user = DummyUser()
    
    class DummyAuth:
        def sign_up(self, data):
            return DummySignUpResult()
        
        def sign_in_with_password(self, data):
            return DummySignInResult()
        
        def get_user(self, token):
            return DummyGetUserResult()
    
    class DummyExecuteResult:
        def __init__(self):
            self.data = {
                'user_id': 'dummy-user-id', 
                'email': email, 
                'full_name': full_name, 
                'user_type': role
            }
    
    class DummyTable:
        def insert(self, data):
            return self
        def select(self, *args, **kwargs):
            return self
        def eq(self, *args, **kwargs):
            return self
        def single(self):
            return self
        def execute(self):
            return DummyExecuteResult()
    
    class DummySupabase:
        def __init__(self):
            self.auth = DummyAuth()
        
        def table(self, name):
            return DummyTable()
    
    # Apply the monkeypatch
    import app.config
    monkeypatch.setattr(app.config, "supabase", DummySupabase())
    
    # Also patch the imported supabase in the routers
    import app.routers.auth
    import app.routers.users
    monkeypatch.setattr(app.routers.auth, "supabase", DummySupabase())
    monkeypatch.setattr(app.routers.users, "supabase", DummySupabase())

    # Test signup
    resp = client.post("/auth/signup", json={
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "full_name": full_name,
        "role": role,
        "terms_agreed": terms_agreed
    })
    print("Signup response:", resp.json())
    assert resp.status_code == 200
    assert "user_id" in resp.json()

    # Test login/token
    resp = client.post("/auth/token", data={
        "username": email,
        "password": password
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    # Test profile
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/users/profile", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == email
    assert data["full_name"] == full_name