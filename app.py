from flask import *
import os
from dados.usuarios import *
from dados.categorias import *
from dados.produtos import *

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

#categorias
@app.route('/categorias')
def categorias_page():
    return(render_template('categorias.html', categorias = categorias))

@app.route('/categorias/criar')
def categorias_criar():
    return(render_template('categorias_criar.html'))

@app.route('/categorias/salvar')
def categorias_salvar():
    global categorias
    nome = str(request.args.get('nome'))
    categorias.append(nome)
    return(redirect('/categorias'))

@app.route('/categorias/confirmar/<pos>')
def categorias_confirmar(pos):
    pos = int(pos)
    categoria = categorias[pos]
    return(render_template('categorias_confirmar.html', categoria = categoria, pos = pos))

@app.route('/categorias/excluir/<pos>')
def categorias_excluir(pos):
    global categorias
    pos = int(pos)
    categorias.pop(pos)
    return(redirect('/categorias'))
#fim categorias

#produtos
@app.route('/produtos')
def produtos_page():
    produtos_filtro = []
    categoria = request.args.get('categoria')
    search = request.args.get('search')
    if categoria == 'todas' and search == '':
        produtos_filtro = produtos
    else:
        if categoria != 'todas':
            for produto in produtos:
                if produto['categoria'] == categoria:
                    produtos_filtro.append(produto)

        if search != '':
            for produto in produtos:
                if produto['codigo'] == search:
                    produtos_filtro.append(produto)

    return(render_template('produtos.html', produtos=produtos_filtro, categorias=categorias))

@app.route('/produtos/criar')
def produtos_criar():
    return(render_template('produtos_criar.html', categorias=categorias))

@app.route('/produtos/salvar')
def produtos_salvar():
    global produtos
    nome = request.args.get('nome')
    preco_str = request.args.get('preco')
    preco_float = float(preco_str.replace(',', '.'))
    codigo = request.args.get('codigo')
    categoria = request.args.get('categoria')
    produto = {
        'nome': nome,
        'categoria': categoria,
        'preco': preco_float,
        'codigo': codigo
    }

    produtos.append(produto)
    return(redirect('/produtos?search=&categoria=todas'))

@app.route('/produtos/editar/<code>')
def produtos_editar(code):
    produto_edit = {}
    for produto in produtos:
        if produto['codigo'] == code:
            produto_edit = {
                'nome': produto['nome'],
                'categoria': produto['categoria'],
                'preco': produto['preco'],
                'codigo': produto['codigo']
            }
            break
    return(render_template('produtos_editar.html', produto_edit=produto_edit, categorias=categorias, code=code))

@app.route('/produtos/editar/salvar/<code>')
def produtos_editar_salvar(code):
    global produtos
    nome = request.args.get('nome')
    preco_str = request.args.get('preco')
    preco_float = float(preco_str.replace(',', '.'))
    codigo = request.args.get('codigo')
    categoria = request.args.get('categoria')
    produto_novo = {
        'nome': nome,
        'categoria': categoria,
        'preco': preco_float,
        'codigo': codigo
    }
    for pos, produto in enumerate(produtos):
        if produto['codigo'] == code:
            produtos[pos] = produto_novo
            break
    return(redirect('/produtos?search=&categoria=todas'))

@app.route('/produtos/confirmar/<codigo>')
def produtos_confirmar(codigo):
    nome = ''
    for produto in produtos:
        if produto['codigo'] == codigo:
            nome = produto['nome']
            break
    return(render_template('produtos_confirmar.html', nome=nome, codigo=codigo))

@app.route('/produtos/excluir/<codigo>')
def produtos_excluir(codigo):
    global produtos
    for pos, produto in enumerate(produtos):
        if produto['codigo'] == codigo:
            produtos.pop(pos)
    return(redirect('/produtos?search=&categoria=todas'))
#fim produtos

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
