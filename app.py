from flask import *
import os
from dados.usuarios import *

app = Flask(__name__)

@app.route('/login')
def login():
    return(render_template('login.html'))

@app.route('/login/code')
def login_code():
    codigo = int(request.args.get('codigo'))
    if usuarios[codigo]["nome"] == '':
        return('batata')
    else:
        return('torresmo')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
