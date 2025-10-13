from flask import Blueprint, request, jsonify, redirect, url_for,render_template, session
from controllers.usuariosController import (
    adicionar_usuario,
    excluir_usuario,
    atualizar_usuario,
    processar_login
)
from decorators.autenticacao import  somente_admin

usuarios_blueprint = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_blueprint.route('/adicionar_usuario', methods=['POST'])
def adicionar():
    return adicionar_usuario()

@usuarios_blueprint.route('/deletar_usuario', methods=['DELETE'])
@somente_admin()
def excluir():
    return excluir_usuario()

@usuarios_blueprint.route('/atualizar_usuario', methods=['PUT'])
def atualizar():
    return atualizar_usuario()

@usuarios_blueprint.route("/login", methods=["GET", "POST"])
def logar():
    if request.method == "GET":
        return render_template("login.html")
    return processar_login()  # Mantém sua lógica POST existente

@usuarios_blueprint.route('/cadastro_usuario')
def cadastro_usuario():
    return render_template('cadastro_user.html')

@usuarios_blueprint.route("/teste-sessao")
def teste_sessao():
    return f"Sessão atual: {dict(session)}"

@usuarios_blueprint.route('/meu-espaco', methods=['GET'])
def meu_espaco():
    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.logar'))

    from config import conectar_bd
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = %s", (session['usuario_id'],))
    usuario = cursor.fetchone()
    conn.close()

    return render_template('usuario.html', usuario=usuario)

@usuarios_blueprint.route('/editar_perfil', methods=['POST'])
def editar_perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('usuarios.logar'))

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    from config import conectar_bd
    conn = conectar_bd()
    cursor = conn.cursor()

    if senha.strip():
        cursor.execute("""
            UPDATE usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?
        """, (nome, email, senha, session['usuario_id']))
    else:
        cursor.execute("""
            UPDATE usuarios SET nome = ?, email = ? WHERE id = ?
        """, (nome, email, session['usuario_id']))

    conn.commit()
    conn.close()

    return redirect(url_for('usuarios.meu_espaco'))