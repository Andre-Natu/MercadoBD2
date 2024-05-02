import mysql.connector


# Cria uma conexão com o banco de dados
class Conexao:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="79801320natu;;",
                database="mercadoBomDemais3"
            )
            cls._instance.c = cls._instance.conn.cursor()
        return cls._instance
