import mysql.connector
from tkinter import messagebox, simpledialog

from Connection import Conexao


class Itens:
    def __init__(self):
        self.db_connection = Conexao()
        self.c = self.db_connection.c
        self.conn = self.db_connection.conn
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS itens (
                        id_itens INT AUTO_INCREMENT PRIMARY KEY,
                        produto_id INT,
                        pedido_id INT,
                        quantidade_itens INTEGER,
                        preco_itens DECIMAL(10, 2),
                        CONSTRAINT fk_produto_constraint FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
                        CONSTRAINT fk_pedido_constraint FOREIGN KEY (pedido_id) REFERENCES pedidos(id_pedido) ON DELETE CASCADE
                        )''')

    def adicionar_produto_a_item(self, produto_id, pedido_id, quantidade, preco):
        self.c.execute("SELECT quantidade FROM produtos WHERE id = %s", (produto_id,))
        result = self.c.fetchone()

        if result[0] < int(quantidade):
            messagebox.showerror("Erro", "Quantidade insuficiente no estoque.")
            return

        self.c.callproc('AdicionarItemComDesconto', [produto_id, pedido_id, quantidade, preco,])
        messagebox.showinfo("Pedido", "Produto adicionado ao pedido com sucesso.")

    def remover_item_do_produto(self):
        id_item = simpledialog.askinteger("id_item", "Digite o id do item que deseja remover do pedido:")
        self.c.execute("DELETE FROM itens WHERE id_itens = %s", (id_item,))
        messagebox.showinfo("Pedido", "Produto removido do pedido com sucesso.")
