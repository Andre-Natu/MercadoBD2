import mysql.connector
from tkinter import messagebox

from datetime import datetime
from Connection import Conexao


class Pedidos:
    def __init__(self):
        self.db_connection = Conexao()
        self.c = self.db_connection.c
        self.conn = self.db_connection.conn
        self.create_table()
        self.view_detalhes_pedido()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
                    cliente_id INT,
                    data_pedido DATE,
                    forma_pagamento TEXT,
                    CONSTRAINT fk_cliente_constraint FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente) ON DELETE CASCADE
                )''')

    def mostrar(self):
        self.c.execute("SHOW TABLES LIKE 'pedidos';")
        dados = self.c.fetchall()

        return dados

    # uso da view
    def view_detalhes_pedido(self):
        # Verificar se a view existe
        self.c.execute("SHOW TABLES LIKE 'detalhes_pedido_cliente';")
        result = self.c.fetchone()

        # se ela não existir, cria ela
        if not result:
            self.c.execute("""
                CREATE VIEW detalhes_pedido_cliente AS
                SELECT 
                    pedidos.id_pedido, 
                    clientes.nome AS nome_cliente, 
                    pedidos.forma_pagamento, 
                    produtos.nome AS nome_produto, 
                    itens.quantidade_itens, 
                    itens.preco_itens, 
                    pedidos.data_pedido 
                FROM 
                    pedidos 
                INNER JOIN 
                    clientes ON pedidos.cliente_id = clientes.id_cliente 
                INNER JOIN 
                    itens ON pedidos.id_pedido = itens.pedido_id
                INNER JOIN 
                    produtos ON itens.produto_id = produtos.id
            """)
            self.conn.commit()

    def adicionar_pedido(self, cliente_id, forma_pagamento):
        self.c.execute("INSERT INTO pedidos (cliente_id, forma_pagamento, data_pedido) VALUES (%s, %s, %s)",
                       (cliente_id, forma_pagamento, datetime.now(),))
        self.conn.commit()
        return self.c.lastrowid

    def alterar_view(self):
        self.c.execute("""
                ALTER VIEW detalhes_pedido_cliente AS
                SELECT 
                    pedidos.id_pedido, 
                    clientes.nome AS nome_cliente, 
                    pedidos.forma_pagamento, 
                    produtos.nome AS nome_produto, 
                    itens.quantidade_itens, 
                    itens.preco_itens, 
                    pedidos.data_pedido,
                    itens.id_itens
                FROM 
                    pedidos 
                INNER JOIN 
                    clientes ON pedidos.cliente_id = clientes.id_cliente 
                INNER JOIN 
                    itens ON pedidos.id_pedido = itens.pedido_id
                INNER JOIN 
                    produtos ON itens.produto_id = produtos.id
            """)
        self.conn.commit()
