from crypt import methods
from flask import Flask,render_template, request, redirect, session, flash

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console
        
jogo1 = Jogo('Pac-Man', 'Come-Come', 'Atari')
jogo2 = Jogo('Pitfull', 'Tarzam', 'PC')
jogo3 = Jogo('MonPatroll', 'Lunar', 'Mini-Game')
listaJogos = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'g4'

@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Novos Jogos', jogos = listaJogos)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect('/login?proxima=cadastro')
    return render_template('cadastrarJogo.html', titulo = 'Cadastro de jogos' )

@app.route('/criar', methods = ['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    listaJogos.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    if '123456' == request.form['senha']:
        session ['usuario_logado'] = request.form['usuario']
        flash(session ['usuario_logado'] + ' Logado com Sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect('/{}'.format(proxima_pagina))
    else:
        flash('Usuário Não Logado!')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session ['usuario_logado'] = None
    flash('Logout Efetuado com Sucesso!')
    return redirect('/')

app.run(debug = True)