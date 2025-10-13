from flask import Blueprint, request, jsonify, session
from config import conectar_bd

avaliacoes_blueprint = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")

@avaliacoes_blueprint.route("/avaliar", methods=["POST"])
def avaliar():
    dados = request.get_json()
    print("DADOS RECEBIDOS:", dados)

    if not dados or "id_livro" not in dados or "avaliacao" not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    id_livro = dados["id_livro"]
    avaliacao = dados["avaliacao"]
    id_usuario = session ['user']['id']

    print(id_livro, id_usuario, avaliacao, dados)
    if not id_usuario:
        return jsonify({"erro": "Usuário não autenticado"}), 401

    if avaliacao not in [1, -1]:
        return jsonify({"erro": "Avaliação inválida"}), 400

    conexao = conectar_bd()
    try:
        with conexao.cursor(buffered=True) as cursor:
            cursor.execute("""
                INSERT INTO avaliacoes (id_livro, id_usuario, avaliacao)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE avaliacao = VALUES(avaliacao), data = CURRENT_TIMESTAMP
            """, (id_livro, id_usuario, avaliacao))
            conexao.commit()
        return jsonify({"mensagem": "Avaliação registrada com sucesso!"}), 201
    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": str(e)}), 400
    finally:
        conexao.close()


@avaliacoes_blueprint.route("/ranking")
def ranking():
    conexao = conectar_bd()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM livros_avaliacoes ORDER BY likes DESC")
            livros = cursor.fetchall()
        return jsonify(livros)
    finally:
        conexao.close()
