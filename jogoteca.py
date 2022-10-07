from crypt import methods
from flask import Flask,render_template, request, redirect

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

@app.route('/')
def index():
    return render_template('lista.html', titulo = 'Novos Jogos', jogos = listaJogos)

@app.route('/cadastro')
def cadastro():
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
    return render_template('login.html')

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    if '123456' == request.form['senha']:
        return redirect('/')
    else:
        return redirect('/login')

app.run(debug = True)