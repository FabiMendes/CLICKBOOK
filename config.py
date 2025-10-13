import mysql.connector

def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="joao2504",
            database="teste"
        )
        if conexao.is_connected():
            print("Conectado ao banco de dados!")
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

conexao = conectar_bd()
cursor = conexao.cursor() if conexao else None