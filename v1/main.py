from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Монтируем статические файлы (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Простейшая HTML страница
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Мой первый сайт на FastAPI</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>Добро пожаловать на мой сайт!</h1>
    <p>Это простейший пример сайта на FastAPI.</p>
    <p>Попробуйте <a href="/api/hello">API endpoint</a></p>
</body>
</html>
"""

# Маршрут для главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content

# Простейший API endpoint
@app.get("/api/hello")
async def say_hello():
    return {"message": "Привет, мир!"}