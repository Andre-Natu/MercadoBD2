import mysql.connector
from tkinter import messagebox

from Connection import Conexao


class Clientes:
    def __init__(self):
        self.db_connection = Conexao()
        self.c = self.db_connection.c
        self.conn = self.db_connection.conn
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                        nome TEXT,
                        email TEXT,
                        telefone TEXT,
                        desconto TEXT)''')

    def adicionar_cliente(self, nome, email, telefone, desconto=None):
        self.c.execute("SELECT * FROM clientes WHERE nome = %s", (nome,))
        rows = self.c.fetchall()
        if len(rows) > 0:
            messagebox.showinfo("Logado", "Você já possui um cadastro no sistema, login feito com sucesso.")
        else:
            self.c.execute("INSERT INTO clientes (nome, email, telefone, desconto) VALUES (%s, %s, %s, %s)",
                           (nome, email, telefone, desconto))
            self.conn.commit()
            messagebox.showinfo("Registro", "Cliente cadastrado com sucesso.")

