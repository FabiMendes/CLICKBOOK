from config import conexao, cursor
import mysql.connector
from config import conectar_bd

class Livros:
    def __init__(self, titulo, autor, publicacao, tema, imagem):
        self.titulo = titulo
        self.autor = autor
        self.publicacao = publicacao
        self.tema = tema
        self.imagem = imagem

    def salvar(self):
        try:
            if conexao.is_connected():
                sql = """INSERT INTO livros 
                         (titulo, autor, publicacao, tema, imagem, disponivel)
                         VALUES (%s, %s, %s, %s, %s, TRUE)"""
                valores = (self.titulo, self.autor, self.publicacao, self.tema, self.imagem)
                cursor.execute(sql, valores)
                conexao.commit()
                print(f"Livro '{self.titulo}' adicionado com sucesso!")
            else:
                print("Erro: Conexão com o banco não está ativa.")
        except Exception as e:
            print(f"Erro ao inserir livro: {e}")

    def deletar(self, titulo):
        try:
            if conexao.is_connected():
                sql = "UPDATE livros SET disponivel = FALSE WHERE titulo = %s"
                cursor.execute(sql, (titulo,))
                conexao.commit()
                print(f"Livro '{titulo}' marcado como fora do estoque.")
            else:
                print("Erro: conexão com o banco não está ativa.")
        except Exception as e:
            print(f"Erro ao atualizar disponibilidade: {e}")

  

    @staticmethod
    def atualizar(titulo, atualizar, autor, publicacao, tema, imagem):
        try:
            if conexao.is_connected():
                print("opa")
                sql = """UPDATE livros 
                         SET titulo = %s, autor = %s, publicacao = %s, tema = %s, imagem = %s 
                         WHERE titulo = %s"""
                cursor = conexao.cursor()
                cursor.execute(sql, (atualizar, autor, publicacao, tema, imagem, titulo))
                conexao.commit()
                print(f"Livro '{titulo}' atualizado com sucesso!")
            else:
                print("Erro: Conexão com o banco não está ativa.")
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")      

    @staticmethod
    def buscar_todos():
        try:
            conexao = conectar_bd()
            if conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT * FROM livros WHERE disponivel = TRUE")
                livros = cursor.fetchall()
                return [
                    {
                        'id': livro[0],
                        'titulo': livro[1],
                        'autor': livro[2],
                        'publicacao': livro[3],
                        'tema': livro[4],
                        'imagem': livro[5]
                    } for livro in livros
                ]
            else:
                print("Erro: conexão não foi estabelecida.")
                return []
        except Exception as e:
            print(f"Erro ao buscar livros: {e}")
            return []
    

    @staticmethod
    def buscar_livro(titulo):
        try:
            conexao = conectar_bd()
            if conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT * FROM livros WHERE titulo = %s", (titulo,))
                livro = cursor.fetchone()

                if not livro:
                    return None

                return {
                    "id": livro[0],
                    "titulo": livro[1],
                    "autor": livro[2],
                    "publicacao": livro[3],
                    "tema": livro[4],
                    "imagem": livro[5]
                }
            else:
                print("Erro: conexão não foi estabelecida.")
                return None
        except mysql.connector.Error as err:
            print(f"Erro ao buscar livro: {err}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar livro: {e}")
            return None
