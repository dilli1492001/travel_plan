from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

db = {
    'username': 'john',
    'password': '12345'
}

# HTML Templates
home_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h2>Home Page</h2>
    <nav>
        <a href="/">Home</a> |
        <a href="/login">Login</a> |
        <a href="/about">About</a> |
        <a href="/projects">Projects</a> |
        <a href="/contact">Contact</a>
    </nav>
</body>
</html>
'''

login_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/about">About</a> |
        <a href="/projects">Projects</a> |
        <a href="/contact">Contact</a>
    </nav>
    <h2>Login Page</h2>
    <form action='/submit' method='POST'>
        <div>
            <input type='text' placeholder='Email' name='email'>
        </div>
        <div>
            <input type='password' placeholder='Password' name='password'>
        </div>
        <button type='submit'>Login</button>
    </form>
</body>
</html>
'''

about_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>About</title>
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/login">Login</a> |
        <a href="/projects">Projects</a> |
        <a href="/contact">Contact</a>
    </nav>
    <h2>About Us</h2>
    <p>We are a small company building cool web applications with FastAPI.</p>
</body>
</html>
'''

projects_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Projects</title>
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/login">Login</a> |
        <a href="/about">About</a> |
        <a href="/contact">Contact</a>
    </nav>
    <h2>Our Projects</h2>
    <ul>
        <li>Project 1: FastAPI Blog</li>
        <li>Project 2: Todo App</li>
        <li>Project 3: E-commerce API</li>
    </ul>
</body>
</html>
'''

contact_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Contact</title>
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/login">Login</a> |
        <a href="/about">About</a> |
        <a href="/projects">Projects</a>
    </nav>
    <h2>Contact Us</h2>
    <p>Email: contact@example.com</p>
    <p>Phone: +91 9876543210</p>
</body>
</html>
'''


# Routes
@app.get('/')
def home():
    return HTMLResponse(home_html)

@app.get('/login')
def login():
    return HTMLResponse(login_html)

@app.get('/about')
def about():
    return HTMLResponse(about_html)

@app.get('/projects')
def projects():
    return HTMLResponse(projects_html)

@app.get('/contact')
def contact():
    return HTMLResponse(contact_html)

@app.post('/submit')
def submit(email: str = Form(...), password: str = Form(...)):
    if email == db.get('username') and password == db.get('password'):
        return HTMLResponse("<h2>Dashboard</h2>You are in dashboard. Welcome!")
    else:
        return HTMLResponse('<p>Invalid credentials</p>')
