from flask import *
from config import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread

import sqlite3 as sl
import datetime


global response_counter
response_counter = 0
debug = True
server_url = "https://0neras.pythonanywhere.com"


app = Flask(
    __name__, 
    template_folder = "html", 
    static_folder = "static"
)

app.permanent_session_lifetime = datetime.timedelta(hours = 1)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours = 1)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



limiter = Limiter(
    app,
    key_func = get_remote_address,
    default_limits = [
        "49 per minute"
    ]
)


def update_counter():
    global response_counter

    if 'visit' in session:
        pass
    else:
        session['visit'] = True
        response_counter += 1
        with open('metrica.txt', 'w+') as f:
            f.write(str(response_counter))

    return response_counter


@app.route('/')
def index():
    return render_template('index.html', visits = update_counter(), title = "Арен Елчинян", description = "Арен Елчинян, 16 лет. Программист.", debug = debug, server_url = server_url)


@app.route('/about')
def about():
    return render_template('about.html', visits = update_counter(), title = "Обо мне", description = "Арен Елчинян, 16 лет. Готов учиться и работать.", debug = debug, server_url = server_url)


@app.route('/blog')
def blog():
    return render_template('blog.html', visits = update_counter(), title = "Блог", description = "Арен Елчинян, 16 лет. Блог.", debug = debug, server_url = server_url)



if __name__ == "__main__":
    try:
        with open('metrica.txt', 'r+') as f:
            response_counter = int(f.readline())
    except:
        with open('metrica.txt', 'w+') as f:
            f.write(str(response_counter))
    print(response_counter)
    app.run(debug = debug)