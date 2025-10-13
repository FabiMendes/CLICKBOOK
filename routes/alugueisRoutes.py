from flask import Blueprint, session, request
from controllers.alugueisController import alugar_livro, devolver_livro, listar_alugueis, listar_alugueis_usuario
from decorators.autenticacao import login_required, somente_admin

alugueis_blueprint = Blueprint('alugueis', __name__, url_prefix='/alugueis')

@alugueis_blueprint.route('/alugar', methods=['POST'])
@login_required
def rota_alugar_livro():
    return alugar_livro()

@alugueis_blueprint.route('/devolver/<int:aluguel_id>', methods=['POST'])
@login_required
def rota_devolver_livro(aluguel_id):
    return devolver_livro(aluguel_id)

@alugueis_blueprint.route('/', methods=['GET'])
@login_required
def rota_listar_alugueis():
    return listar_alugueis()

@alugueis_blueprint.route('/meus-alugueis', methods=['GET'])
@login_required
def rota_listar_alugueis_usuario():
    return listar_alugueis_usuario()