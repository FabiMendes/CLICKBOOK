from flask import Flask, render_template, session, Blueprint, redirect, url_for
from decorators.autenticacao import login_required, somente_admin
from dotenv import load_dotenv
from controllers.livrosController import livros_populares

load_dotenv()
front_blueprint = Blueprint('front', __name__)

@front_blueprint.route("/", methods=["GET"])
def home():
    from controllers.livrosController import livros_populares
    livros = livros_populares()  # pega os livros mais alugados
    return render_template("index.html", livros_populares=livros)

@front_blueprint.route('/login')
def login():
    return render_template('login.html')

@front_blueprint.route('/listar')
@login_required
def listar():
    try:
        usuario = session['user']
        if usuario['perfil'] == 'admin':
            return render_template('listarAdmin.html', usuario=usuario)
        return render_template('listar.html', usuario=usuario)
    except KeyError:
        return redirect(url_for('usuarios.logar'))
    
@front_blueprint.route('/cadastro')
@login_required
@somente_admin()
def cadastro():
    return render_template('cadastro.html')


@front_blueprint.route('/aluguel')
@login_required
def alugueis():
    usuario = session.get('user')
    return render_template('alugueis.html', usuario=usuario)

