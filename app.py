from flask import *
import os
from dados.usuarios import *

app = Flask(__name__)
codigo = 000000

@app.route('/login')
def login():
    return(render_template('login.html'))

@app.route('/login/code')
def login_code():
    global codigo
    codigo = int(request.args.get('codigo'))
    if codigo in usuarios:
        if usuarios[codigo]["nome"] == '':
            return(render_template('login_nome.html'))
        else:
            return('nome cadastrado')
    else:
        return(redirect('/login'))
    
@app.route('/login/nome')
def login_nome():
    return(render_template('login_nome.html'))

@app.route('/login/cad_nome')
def cad_nome():
    nome = str(request.args.get('nome'))
    usuarios[codigo]["nome"] = nome
    return('nome cadastrado')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
