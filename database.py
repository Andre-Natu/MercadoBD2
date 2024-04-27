import mysql.connector
from tkinter import messagebox


class Registro:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="79801320natu;;",
            database="mercadoBomDemais"
        )
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       nome TEXT,
                       quantidade INTEGER,
                       preco DECIMAL(10, 2),
                       validade DATE)''')

    def registrar_produto(self, nome, quantidade, preco, validade):
        dados_produto = (nome, quantidade, preco, validade)
        self.c.execute("INSERT INTO produtos (nome, quantidade, preco, validade) VALUES (%s, %s, %s, %s)",
                       dados_produto)
        self.conn.commit()
        messagebox.showinfo("Registro", "Produto registrado com sucesso.")

    def visualizar_todos_produtos(self):
        self.c.execute("SELECT * FROM produtos")
        dados = self.c.fetchall()

        return dados

    def pesquisar_produto(self, nome):
        self.c.execute("SELECT * FROM produtos WHERE nome = %s", (nome,))
        dados = self.c.fetchone()

        return dados

    def obter_id(self, nome):
        self.c.execute("SELECT id FROM produtos WHERE nome = %s", (nome,))

        rowid = self.c.fetchone()
        if rowid:
            return rowid[0]
        else:
            messagebox.showinfo("Erro", "Erro, o produto não foi encontrado")
            return None

    def alterar_produto(self, novos_dados):

        query = "UPDATE produtos SET nome = %s, quantidade = %s, preco = %s, validade = %s WHERE id = %s"
        self.c.execute(query, (novos_dados[1], novos_dados[2], novos_dados[3], novos_dados[4], novos_dados[0]))
        self.conn.commit()

        messagebox.showinfo('Alteração', f'Produto do ID: {novos_dados[0]} atualizado com sucesso!')

    def remover_produto(self, codigo_produto):
        self.c.execute("DELETE FROM produtos WHERE id = %s", (codigo_produto,))
        self.conn.commit()

        messagebox.showinfo('Exclusão', f'Produto do ID: {codigo_produto} foi deletado com sucesso!')

    def relatorio(self):
        self.c.execute("SELECT * FROM produtos")
        dados = self.c.fetchall()

        total_produtos = 0
        preco_total = 0.0
        for i in dados:
            total_produtos += i[2]
            preco_total += float(i[2] * i[3])

        preco_total = round(preco_total, 2)
        estoque = [total_produtos, preco_total]

        return estoque


registro = Registro()
