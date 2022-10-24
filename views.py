from sqlite3 import Timestamp
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from  models import Usuarios, Jogos
from helpers import FormularioJogo, recupera_imagem, deleta_arquivo, FormularioUsuario
import time

@app.route('/')
def index():
    listaJogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo = 'Novos Jogos', jogos = listaJogos)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('cadastro')))
    form = FormularioJogo()
    return render_template('cadastrarJogo.html', titulo = 'Cadastro de jogos', form = form )

@app.route('/criar', methods = ['POST',])
def criar():
    form = FormularioJogo(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for('cadastro'))
    
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    jogo = Jogos.query.filter_by(nome = nome).first()
    
    if jogo:
        flash('Jogo Já Existente!!!')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
    db.session.add(novo_jogo)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo = 'Editando jogos', id = id, capa_jogo = capa_jogo, form = form )

@app.route('/atualizar', methods = ['POST',])
def atualizar():
    form = FormularioJogo(request.form)
    
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        Timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{Timestamp}.jpg')

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
    form = FormularioUsuario(request.form)
    return render_template('login.html', proxima=proxima, form = form)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    form = FormularioUsuario()
    usuario = Usuarios.query.filter_by(nickname = form.nickname.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
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

