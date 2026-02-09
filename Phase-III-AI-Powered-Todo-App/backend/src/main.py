from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel, Session, select
from typing import Annotated
from uuid import UUID, uuid4

from .models.todo import Todo
from .models.user import User
from .services.database import create_db_and_tables, get_session
from .api.auth import get_authenticated_user, create_access_token, UserCreate, Token
from .api.endpoints import todo # Import todo endpoints router
from .mcp_server import router as mcp_router # Corrected: mcp_server is in src directly
from .api.endpoints import chat as chat_endpoints
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

# Placeholder for user management - In a real app, users would be created via registration
# For now, a simple 'login' endpoint will simulate authentication
@app.post("/token", response_model=Token)
async def login_for_access_token(user_data: UserCreate, session: Session = Depends(get_session)):
    # In a real app, verify username and hashed password from DB
    # For this basic implementation, we'll create a user if not exists and issue a token
    user = session.exec(select(User).where(User.username == user_data.username)).first()
    if not user:
        # Simulate password hashing
        hashed_password = f"hashed_{user_data.password}"
        user = User(username=user_data.username, hashed_password=hashed_password, email=user_data.email)
        session.add(user)
        session.commit()
        session.refresh(user)
    elif user.hashed_password != f"hashed_{user_data.password}": # Simple check
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
        print("INFO: Database tables created/verified.")
    except SQLAlchemyError as e:
        print(f"WARNING: Could not connect to database or create tables: {e}")
        print("WARNING: Application will start without database connectivity.")
        print("WARNING: Ensure your DATABASE_URL is correct and the database is running.")


@app.get("/")
def read_root():
    return {"message": "Todo AI Chatbot Backend"}

# Example protected route
@app.get("/protected-route")
async def protected_route(current_user: Annotated[User, Depends(get_authenticated_user)]):
    return {"message": f"Hello, {current_user.username}! This is a protected route."}

app.include_router(todo.router)
app.include_router(mcp_router)
app.include_router(chat_endpoints.router) # Correctly include the chat router
