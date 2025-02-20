from flask import *
import webbrowser
import os
import json
from datetime import datetime
from random import randint
from dados.usuarios import *
from dados.categorias import *
from dados.produtos import *
from dados.relatorios import *

app = Flask(__name__)
#save

# Funções de salvar e carregar para cada variável
def salvar_usuarios():
    with open("usuarios.txt", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=4)

def carregar_usuarios():
    global usuarios
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    else:
        salvar_usuarios()

def salvar_categorias():
    with open("categorias.txt", "w", encoding="utf-8") as arquivo:
        json.dump(categorias, arquivo, ensure_ascii=False, indent=4)

def carregar_categorias():
    global categorias
    if os.path.exists("categorias.txt"):
        with open("categorias.txt", "r", encoding="utf-8") as arquivo:
            categorias = json.load(arquivo)
    else:
        salvar_categorias()

def salvar_produtos():
    with open("produtos.txt", "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

def carregar_produtos():
    global produtos
    if os.path.exists("produtos.txt"):
        with open("produtos.txt", "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)
    else:
        salvar_produtos()

def salvar_relatorios():
    with open("relatorios.txt", "w", encoding="utf-8") as arquivo:
        json.dump(relatorios, arquivo, ensure_ascii=False, indent=4)

def carregar_relatorios():
    global relatorios
    if os.path.exists("relatorios.txt"):
        with open("relatorios.txt", "r", encoding="utf-8") as arquivo:
            relatorios = json.load(arquivo)
    else:
        salvar_relatorios()

# Função geral para carregar todos os dados
def carregar():
    carregar_usuarios()
    carregar_categorias()
    carregar_produtos()
    carregar_relatorios()

# Função geral para salvar todos os dados
def salvar():
    salvar_usuarios()
    salvar_categorias()
    salvar_produtos()
    salvar_relatorios()
#fim save
#Login
acesso = False
adm = False
codigo = 000000

@app.route('/')
def _():
   carregar()
   if acesso:
        return(redirect('/home'))
   else:
       return(redirect('/login'))

@app.route('/login')
def login():
    carregar()
    print(usuarios)
    return(render_template('login.html'))

@app.route('/login/code')
def login_code():
    global codigo
    global acesso
    global adm
    codigo = str(request.args.get('codigo'))
    print(codigo)
    if codigo in usuarios:
        acesso = True
        print('batatatatatatatatatatatatatattttttttttttttt')
        if usuarios[codigo]['is_admin'] == True:
            adm = True
        if usuarios[codigo]["nome"] == '':
            return(render_template('login_nome.html'))
        else:
            return(redirect('/home'))
    else:
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return(redirect('/login'))
    
@app.route('/login/nome')
def login_nome():
    return(render_template('login_nome.html'))

@app.route('/login/cad_nome')
def cad_nome():
    global acesso
    nome = str(request.args.get('nome'))
    usuarios[codigo]["nome"] = nome
    salvar_usuarios()
    return(redirect('/home'))
#fim login

#home
@app.route('/home')
def home():
    global acesso
    if acesso:
        return(render_template('home.html', nome = usuarios[codigo]['nome'], adm=adm))
    else:
        return(redirect('/login'))
#fim home

#categorias
@app.route('/categorias')
def categorias_page():
    if not acesso:
        return(redirect('/login'))
    return(render_template('categorias.html', categorias = categorias[1:], adm=adm))

@app.route('/categorias/criar')
def categorias_criar():
    if not acesso:
        return(redirect('/login'))
    return(render_template('categorias_criar.html'))

@app.route('/categorias/salvar')
def categorias_salvar():
    if not acesso:
        return(redirect('/login'))
    global categorias
    nome = str(request.args.get('nome'))
    categorias.append(nome)
    salvar_categorias()
    return(redirect('/categorias'))

@app.route('/categorias/confirmar/<pos>')
def categorias_confirmar(pos):
    if not acesso:
        return(redirect('/login'))
    pos = int(pos) + 1
    categoria = categorias[pos]
    return(render_template('categorias_confirmar.html', categoria = categoria, pos = pos))

@app.route('/categorias/excluir/<pos>')
def categorias_excluir(pos):
    if not acesso:
        return(redirect('/login'))
    global categorias
    global produtos
    pos = int(pos)
    for produto in produtos:
        if produto['categoria'] == categorias[pos]:
            produto['categoria'] = 'Sem Categoria'
    categorias.pop(pos)
    salvar_categorias()
    return(redirect('/categorias'))
#fim categorias

#produtos
@app.route('/produtos')
def produtos_page():
    if not acesso:
        return(redirect('/login'))
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

    return(render_template('produtos.html', produtos=produtos_filtro, categorias=categorias, adm=adm))

@app.route('/produtos/criar')
def produtos_criar():
    if not acesso:
        return(redirect('/login'))
    return(render_template('produtos_criar.html', categorias=categorias))

@app.route('/produtos/salvar')
def produtos_salvar():
    if not acesso:
        return(redirect('/login'))
    global produtos
    nome = request.args.get('nome')
    preco_str = request.args.get('preco')
    preco_float = float(preco_str.replace(',', '.'))
    codigo = request.args.get('codigo')
    categoria = request.args.get('categoria')
    estoque = 0
    produto = {
        'nome': nome,
        'categoria': categoria,
        'preco': preco_float,
        'codigo': codigo,
        'estoque': estoque
    }

    produtos.append(produto)
    salvar_produtos()
    return(redirect('/produtos?search=&categoria=todas'))

@app.route('/produtos/editar/<code>')
def produtos_editar(code):
    if not acesso:
        return(redirect('/login'))
    produto_edit = {}
    for produto in produtos:
        if produto['codigo'] == code:
            produto_edit = {
                'nome': produto['nome'],
                'categoria': produto['categoria'],
                'preco': produto['preco'],
                'codigo': produto['codigo'],
                'estoque': produto['estoque']
            }
            break
    return(render_template('produtos_editar.html', produto_edit=produto_edit, categorias=categorias, code=code))

@app.route('/produtos/editar/salvar/<code>')
def produtos_editar_salvar(code):
    if not acesso:
        return(redirect('/login'))
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
        'codigo': codigo,
        'estoque': 0
    }
    for pos, produto in enumerate(produtos):
        if produto['codigo'] == code:
            produto_novo['estoque'] = produto['estoque']
            produtos[pos] = produto_novo
            break
    salvar_produtos()
    return(redirect('/produtos?search=&categoria=todas'))

@app.route('/produtos/confirmar/<codigo>')
def produtos_confirmar(codigo):
    if not acesso:
        return(redirect('/login'))
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
    salvar_produtos()
    return(redirect('/produtos?search=&categoria=todas'))
#fim produtos

#estoque
@app.route('/estoque')
def estoque_page():
    if not acesso:
        return(redirect('/login'))
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

    return(render_template('estoque.html', produtos=produtos_filtro, categorias=categorias, adm=adm))

@app.route('/estoque/diminuir/<codigo>')
def estoque_diminuir(codigo):
    if not acesso:
        return(redirect('/login'))
    global produtos
    escolha = {}
    for produto in produtos:
        if produto['codigo'] == codigo:
            escolha = produto
    return(render_template('estoque_diminuir.html', produto = escolha))

@app.route('/estoque/diminuir/salvar/<codigo>')
def estoque_diminuir_salvar(codigo):
    if not acesso:
        return(redirect('/login'))
    global produtos
    diminuir = int(request.args.get('diminuir'))
    for produto in produtos:
        if produto['codigo'] == codigo:
            produto['estoque'] -= diminuir
            registro_venda(produto=produto, qtd_vendida=diminuir)
            break
    salvar_produtos()
    return(redirect('/estoque?search=&categoria=todas'))

@app.route('/estoque/aumentar/<codigo>')
def estoque_aumentar(codigo):
    if not acesso:
        return(redirect('/login'))
    global produtos
    escolha = {}
    for produto in produtos:
        if produto['codigo'] == codigo:
            escolha = produto
    return(render_template('estoque_aumentar.html', produto = escolha))

@app.route('/estoque/aumentar/salvar/<codigo>')
def estoque_aumentar_salvar(codigo):
    if not acesso:
        return(redirect('/login'))
    global produtos
    aumentar = int(request.args.get('aumentar'))
    for produto in produtos:
        if produto['codigo'] == codigo:
            produto['estoque'] += aumentar
    salvar_produtos()
    return(redirect('/estoque?search=&categoria=todas'))
#fim estoque

#relatórios
#Criação e armazenamento de relatórios
def registro_venda(produto, qtd_vendida):
    if not acesso:
        return(redirect('/login'))
    mes = datetime.now().strftime('%Y-%m')
    categoria = produto['categoria']
    nome = produto['nome']
    preco = produto['preco']

    if mes not in relatorios:
        relatorios[mes] = {}
        meses_disponiveis.append(mes)

    if categoria not in relatorios[mes]:
        relatorios[mes][categoria] = {}

    if nome not in relatorios[mes][categoria]:
        relatorios[mes][categoria][nome] = {
            'unidades_vendidas': 0,
            'valor_arrecadado': 0.0,
        }
    
    relatorios[mes][categoria][nome]["unidades_vendidas"] += qtd_vendida
    relatorios[mes][categoria][nome]["valor_arrecadado"] += qtd_vendida * preco
    salvar_relatorios()
#fim criação e armazenamento de relatórios
#relatorios
@app.route('/relatorios')
def relatorios_page():
    if not acesso:
        return(redirect('/login'))
    mes_escolhido = request.args.get('mes_escolhido', 'atual')
    mes_atual = datetime.now().strftime('%Y-%m')
    if mes_escolhido == 'atual':
        try:
            relatorios_filtro = relatorios[mes_atual]
        except:
            relatorios_filtro = {}
    else:
        try:
            relatorios_filtro = relatorios[mes_escolhido]
        except:
            relatorios_filtro = {}
    total_arrecadado = sum(
        dados["valor_arrecadado"]
        for produtos in relatorios_filtro.values()
        for dados in produtos.values()
    )
    return(render_template('relatorios.html', meses=meses_disponiveis, relatorio=relatorios_filtro, total = total_arrecadado, adm=adm))
#fim relatorios
#configurações
@app.route('/config')
def config_page():
    return(render_template('config.html', usuarios=usuarios, adm=adm))

@app.route('/config/excluir/<id>')
def config_excluir(id):
    global usuarios
    id = int(id)
    usuarios.pop(id)
    salvar_usuarios()
    return(redirect('/config'))

@app.route('/config/criar')
def config_criar():
    ids_existentes = set(usuarios.keys())
    while True:
        id = randint(100000, 999999)
        if id not in ids_existentes:
            break
    usuarios[id] = {"nome": "", "is_admin": False}
    salvar_usuarios()
    return(redirect('/config'))
#fim configurações
#sair
@app.route('/sair')
def sair():
    global codigo, adm, acesso
    codigo = 000000
    adm = False
    acesso = False
    salvar()
    return(redirect('/'))

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
