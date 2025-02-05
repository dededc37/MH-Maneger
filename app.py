from flask import *
import os
from dados.usuarios import *

app = Flask(__name__)
#Login
acesso = False
codigo = 000000

@app.route('/')
def _():
   return(redirect('/login'))

@app.route('/login')
def login():
    return(render_template('login.html'))

@app.route('/login/code')
def login_code():
    global codigo
    global acesso
    codigo = int(request.args.get('codigo'))
    if codigo in usuarios:
        acesso = True
        if usuarios[codigo]["nome"] == '':
            return(render_template('login_nome.html'))
        else:
            return(redirect('/home'))
    else:
        return(redirect('/login'))
    
@app.route('/login/nome')
def login_nome():
    return(render_template('login_nome.html'))

@app.route('/login/cad_nome')
def cad_nome():
    global acesso
    nome = str(request.args.get('nome'))
    usuarios[codigo]["nome"] = nome
    return(redirect('/home'))
#fim login

#home
@app.route('/home')
def home():
    global acesso
    if acesso:
        return(render_template('home.html', nome = usuarios[codigo]['nome']))
    else:
        return(redirect('/login'))
#fim home

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
