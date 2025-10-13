from config import conexao, cursor
from datetime import datetime, timedelta


class Alugueis:
    def __init__(self, usuario_id, livro_id):
        self.usuario_id = usuario_id
        self.livro_id = livro_id

    def alugar(self):
        try:
            if conexao.is_connected():
                sql = """
                    INSERT INTO alugueis (usuario_id, livro_id, data_aluguel, devolvido)
                    VALUES (%s, %s, %s, %s)
                """
                valores = (self.usuario_id, self.livro_id, datetime.now(), False)
                cursor.execute(sql, valores)
                conexao.commit()
                return {"sucesso": "Livro alugado com sucesso!"}, 201
            else:
                return {"erro": "Sem conexão com o banco"}, 500
        except Exception as e:
            return {"erro": f"Erro ao alugar livro: {e}"}, 400

    @staticmethod
    def devolver(aluguel_id):
        try:
            if conexao.is_connected():
                sql = """
                    UPDATE alugueis
                    SET devolvido = TRUE, data_devolucao = %s
                    WHERE id = %s AND devolvido = FALSE
                """
                valores = (datetime.now(), aluguel_id)
                cursor.execute(sql, valores)
                conexao.commit()
                if cursor.rowcount > 0:
                    return {"sucesso": "Livro devolvido com sucesso!"}, 200
                else:
                    return {"erro": "Aluguel não encontrado ou já devolvido."}, 404
            else:
                return {"erro": "Sem conexão com o banco"}, 500
        except Exception as e:
            return {"erro": f"Erro ao devolver livro: {e}"}, 400

    @staticmethod
    def listar():
        try:
            if conexao.is_connected():
                sql = """
                    SELECT a.id, u.nome, l.titulo, a.data_aluguel, a.data_devolucao, a.devolvido
                    FROM alugueis a
                    JOIN usuarios u ON a.usuario_id = u.id
                    JOIN livros l ON a.livro_id = l.id
                """
                cursor.execute(sql)
                registros = cursor.fetchall()
                alugueis = [{
                    "id": r[0],
                    "usuario": r[1],
                    "livro": r[2],
                    "data_aluguel": r[3],
                    "data_devolucao": r[4],
                    "devolvido": r[5]
                } for r in registros]
                return alugueis
            else:
                return []
        except Exception as e:
            print(f"Erro ao listar aluguéis: {e}")
            return []


    @staticmethod
    def listar_por_usuario(usuario_id):
        try:
            if conexao.is_connected():
                sql = """
                    SELECT a.id, l.titulo, l.imagem, 
                        a.data_aluguel, a.data_devolucao, a.devolvido, a.multa,
                        a.livro_id
                    FROM alugueis a
                    JOIN livros l ON a.livro_id = l.id
                    WHERE a.usuario_id = %s
                    ORDER BY a.data_aluguel DESC
                """
                cursor.execute(sql, (usuario_id,))
                registros = cursor.fetchall()

                alugueis = []
                agora = datetime.now()

                for r in registros:
                    aluguel_id = r[0]
                    titulo = r[1]
                    imagem = r[2]
                    data_aluguel = r[3]
                    data_devolucao = r[4]
                    devolvido = bool(r[5])
                    multa_atual = bool(r[6])
                    livro_id = r[7]

                    multa = multa_atual  # mantém o valor atual por padrão

                    if data_aluguel:
                        if (agora - data_aluguel) > timedelta(days=30):
                            multa = True
                            if multa != multa_atual:
                                update_sql = "UPDATE alugueis SET multa = %s WHERE id = %s"
                                cursor.execute(update_sql, (True, aluguel_id))
                                conexao.commit()

                    alugueis.append({
                        "id": aluguel_id,
                        "titulo": titulo,
                        "imagem": imagem,
                        "data_aluguel": data_aluguel,
                        "data_devolucao": data_devolucao,
                        "devolvido": devolvido,
                        "multa": multa,
                        "livro_id": livro_id
                    })

                return alugueis
            return []
        except Exception as e:
            print(f"Erro ao listar aluguéis do usuário: {e}")
            return []
