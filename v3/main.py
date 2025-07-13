from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse  # Добавьте этот импорт
from sqlalchemy.orm import Session
import models.base
from models.crud import get_users, create_user, get_user_by_email
import os

app = FastAPI()

# Создаем папку для БД, если её нет
os.makedirs("db", exist_ok=True)

# Инициализация БД
models.base.Base.metadata.create_all(bind=models.base.engine)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблонизатор
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = models.base.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    users = get_users(db)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "FastAPI + SQLite",
            "users": users
        }
    )

@app.post("/add-user/")
async def add_user(
    username: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверка на существующего пользователя
    db_user = get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        user = create_user(db, username=username, email=email)
        return {"message": "User created successfully", "user": user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/users")
async def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users