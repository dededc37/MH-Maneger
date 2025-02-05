from flask import *
import os

app = Flask(__name__)

@app.route('/login')
def login():
    return(render_template('login.html'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
