import sqlite3
from tkinter import messagebox


class Registro:
    def __init__(self):
        self.conn = sqlite3.connect('produtos.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute(''' CREATE TABLE IF NOT EXISTS produtos (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       nome TEXT NOT NULL, 
                       quantidade INTEGER,
                       preco FLOAT,
                       imagem TEXT NOT NULL) ''')

    def registrar_produto(self, produtos):
        self.c.execute("INSERT INTO produtos (nome, quantidade, preco, imagem) VALUES (?,?,?,?)",
                       produtos)
        self.conn.commit()

        messagebox.showinfo('Registro', 'Produto registrado com sucesso!')

    def visualizar_todos_produtos(self):
        self.c.execute("SELECT * FROM produtos")
        dados = self.c.fetchall()

        for i in dados:
            print(f'ID:{i[0]} / Nome: {i[1]} / Quantidade: {i[2]}, Preço: {i[3]}')

    def pesquisar_produto(self, nome):
        self.c.execute("SELECT * FROM produtos WHERE nome = ?", nome)
        dados = self.c.fetchone()

        print(f'ID:{dados[0]} / Nome: {dados[1]} / Quantidade: {dados[2]}, Preço: {dados[3]}')

    def alterar_produto(self, novos_dados):
        query = "UPDATE produtos SET nome = ?, quantidade = ?, preco = ?, imagem = ? WHERE id = ? "
        self.c.execute(query, novos_dados)
        self.conn.commit()

        messagebox.showinfo('Alteração', f'Produto do ID: {novos_dados[1]} atualizado com sucesso!')

    def remover_produto(self, codigo_produto):
        self.c.execute("DELETE FROM produtos WHERE id = ?", (codigo_produto,))
        self.conn.commit()

        messagebox.showinfo('Exclusão', f'Produto do ID: {codigo_produto} foi deletado com sucesso!')


registro = Registro()
