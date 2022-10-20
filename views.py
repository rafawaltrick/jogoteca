from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from  models import Usuarios, Jogos

@app.route('/')
def index():
    listaJogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo = 'Novos Jogos', jogos = listaJogos)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('cadastro')))
    return render_template('cadastrarJogo.html', titulo = 'Cadastro de jogos' )

@app.route('/criar', methods = ['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    jogo = Jogos.query.filter_by(nome = nome).first()
    
    if jogo:
        flash('Jogo Já Existente!!!')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
    db.session.add(novo_jogo)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}.jpg')
    
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo = 'Editando jogos', jogo = jogo )

@app.route('/atualizar', methods = ['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    
    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/apagar/<int:id>')
def apagar(id):
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Jogo Apagado com sucesso!!!")
    return redirect(url_for('index'))
    

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session ['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' Logado com Sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário Não Logado!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session ['usuario_logado'] = None
    flash('Logout Efetuado com Sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)