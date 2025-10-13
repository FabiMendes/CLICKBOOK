from flask import request, jsonify, redirect, url_for, render_template
from models.livros import Livros
from config import conectar_bd

def homeLivros():
    return "<p>Hello, World!</p>"

def adicionar_livro():
    try:
        dados = request.form
        livro = Livros(
            titulo=dados["titulo"],
            autor=dados["autor"],
            publicacao=dados["publicacao"],
            tema=dados["tema"],
            imagem=dados["imagem"]
        )
        livro.salvar()
        return redirect(url_for('front.listar'))

    except Exception as e:
        return f"Erro ao adicionar livro: {str(e)}", 400

def deletar_livro():
    try:
        dados = request.json
        titulo = dados["titulo"]

        livro = Livros(
            titulo=titulo,
            autor=dados.get("autor"),
            publicacao=dados.get("publicacao"),
            tema=dados.get("tema"),
            imagem=dados.get("imagem")
        )
        livro.deletar(titulo)
        print("Livro excluído com sucesso!"), 200
        return jsonify({"mensagem": "Livro excluído com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400

def atualizar_livro():
    try:
        dados = request.json

        titulo_atual = dados["titulo"]
        atualizar = dados.get("atualizar")
        autor = dados.get("autor")
        publicacao = dados.get("publicacao")
        tema = dados.get("tema")
        imagem = dados.get("imagem")

        Livros.atualizar(titulo_atual, atualizar, autor, publicacao, tema, imagem)
        return jsonify({"mensagem": "Livro atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar livro: {str(e)}"}), 400

def listar_livros():
    try:
        livros_cadastrados = Livros.buscar_todos()
        return jsonify(livros_cadastrados), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar livros: {str(e)}"}), 400

def listar_um_livro(titulo):
    conexao = conectar_bd()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM livros_avaliacoes WHERE titulo = %s;", (titulo,))
            livro = cursor.fetchone()
            if not livro:
                return "Livro não encontrado", 404
            return render_template("livro.html", livro=livro)
    finally:
        conexao.close()
    
def livros_populares():
    conexao = conectar_bd()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM livros_populares;")
            return cursor.fetchall()
    finally:
        conexao.close()

def pesquisar_livros():
    try:
        tema = request.args.get("tema", "").strip()
        conexao = conectar_bd()
        with conexao.cursor(dictionary=True) as cursor:
            if tema:
                cursor.execute("""
                    SELECT id, titulo, autor, publicacao, tema, imagem
                    FROM livros
                    WHERE LOWER(tema) LIKE LOWER(%s)
                """, (f"%{tema}%",))
            else:
                cursor.execute("""
                    SELECT id, titulo, autor, publicacao, tema, imagem
                    FROM livros
                """)
            livros = cursor.fetchall()

        # Retorna sempre JSON para o JS
        return jsonify(livros), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao pesquisar livros: {str(e)}"}), 400

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def listar_livros_recentes():
    try:
        conexao = conectar_bd()
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT id, titulo, autor, publicacao, tema, imagem
                FROM livros
                ORDER BY data_cadastro DESC
                LIMIT 6;
            """)
            livros = cursor.fetchall()
        return jsonify(livros), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar livros recentes: {str(e)}"}), 400
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()