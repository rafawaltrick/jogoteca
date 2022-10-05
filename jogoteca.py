from flask import Flask,render_template

class jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

app = Flask(__name__)

@app.route('/inicio')
def inicio():
    jogo1 = jogo('Pac-Man', 'Come-Come', 'Atari')
    jogo2 = jogo('Pitfull', 'Tarzam', 'PC')
    jogo3 = jogo('MonPatroll', 'Lunar', 'Mini-Game')
    listaJogos = [jogo1, jogo2, jogo3]
    return render_template('lista.html', titulo = 'Jogos', jogos = listaJogos)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastrarJogo.html', titulo = 'Cadastro de jogos' )

app.run()