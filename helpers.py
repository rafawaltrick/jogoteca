import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.data_required(), validators.length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.length(min=1, max=20)])
    salvar = SubmitField('Salvar')
    
class FormularioUsuario(FlaskForm):
    nickname = StringField('Nome de Usuário', [validators.data_required(), validators.length(min=1, max=8)] )
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
        
    return 'G4.jpg'  


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'G4.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))