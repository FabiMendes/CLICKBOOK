from flask import Blueprint, request, jsonify, session
from config import conectar_bd

favoritos_blueprint = Blueprint("favoritos", __name__, url_prefix="/favoritos")

# Adicionar livro aos favoritos
@favoritos_blueprint.route("/adicionar", methods=["POST"])
def adicionar_favorito():
    dados = request.get_json()
    id_livro = dados.get("id_livro")
    id_usuario = session["user"]["id"]

    if not id_livro or not id_usuario:
        return jsonify({"erro": "Dados inválidos"}), 400

    conexao = conectar_bd()
    try:
        with conexao.cursor(buffered=True) as cursor:
            cursor.execute("""
                INSERT INTO favoritos (id_usuario, id_livro)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE data = CURRENT_TIMESTAMP
            """, (id_usuario, id_livro))
            conexao.commit()
        return jsonify({"mensagem": "Livro adicionado aos favoritos!"}), 201
    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": str(e)}), 400
    finally:
        conexao.close()


# Listar favoritos do usuário
@favoritos_blueprint.route("/meus-favoritos", methods=["GET"])
def listar_favoritos():
    id_usuario = session["user"]["id"]

    conexao = conectar_bd()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT l.id, l.titulo, l.autor, l.imagem
                FROM favoritos f
                JOIN livros l ON f.id_livro = l.id
                WHERE f.id_usuario = %s
            """, (id_usuario,))
            favoritos = cursor.fetchall()
        return jsonify(favoritos)
    finally:
        conexao.close()
