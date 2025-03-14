from flask import Blueprint, request, jsonify,render_template, redirect, url_for
from models.livros import Livros

livros_blueprint = Blueprint('livros', __name__, url_prefix='/livros')

@livros_blueprint.route('/')
def homeLivros():
    return "<p>Hello, World!</p>"


@livros_blueprint.route('/adicionar_livro', methods=['POST'])
def adicionar_livro():
    try:
        dados = request.form  # Pegando os dados corretamente
        livro = Livros(
            titulo=dados["titulo"], 
            autor=dados["autor"], 
            publicacao=dados["publicacao"], 
            tema=dados["tema"],
            imagem=dados["imagem"]
        )

        livro.salvar()
        return redirect(url_for('livros.listar_livros'))

    except Exception as e:
        return jsonify({"erro": str(e)}), 400  # Retorna erro caso algo dê errado

@livros_blueprint.route('/deletar_livro', methods=['DELETE'])
def deletar_livro():
    try:
        dados = request.json  # Pegando os dados corretamente
        titulo = dados["titulo"]

        livro = Livros(
            titulo=titulo, 
            autor=dados.get("autor"), 
            publicacao=dados.get("publicacao"), 
            tema=dados.get("tema"),
            imagem=dados.get("imagem")
        )

        livro.deletar(titulo)
        return jsonify({"mensagem": "Livro excluido com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400  # Retorna erro caso algo dê errado

@livros_blueprint.route('/atualizar_livro', methods=['PUT'])
def atualizar_livro():
    try:
        dados = request.json

        titulo_atual = dados["titulo"]        
        atualizar = dados.get("atualizar")  # Novo título (opcional)
        autor = dados.get("autor")
        publicacao = dados.get("publicacao")
        tema = dados.get("tema")
        imagem = dados.get("imagem")

        # Agora chamamos o método estático diretamente
        Livros.atualizar(titulo_atual, atualizar, autor, publicacao, tema, imagem)

        return jsonify({"mensagem": "Livro atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar livro: {str(e)}"}), 400


@livros_blueprint.route('/listar_livros')
def listar_livros():
    livros_cadastrados = Livros.buscar_todos()
    return jsonify(livros_cadastrados), 200

