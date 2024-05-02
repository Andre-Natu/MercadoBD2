import mysql.connector
from tkinter import messagebox

import search
from Connection import Conexao


class Funcionarios:
    def __init__(self):
        self.db_connection = Conexao()
        self.c = self.db_connection.c
        self.conn = self.db_connection.conn
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
                        id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
                        nome TEXT,
                        total_vendas_mes DECIMAL(10, 2) DEFAULT 0)''')

    def inserir_funcionarios(self, nome_funcionario):
        self.c.execute("SELECT * FROM funcionarios WHERE nome = %s", (nome_funcionario,))
        rows = self.c.fetchall()
        if len(rows) > 0:
            messagebox.showinfo("Logado", "Você já possui um cadastro no sistema, login feito com sucesso.")
        else:
            self.c.execute("INSERT INTO funcionarios (nome) VALUES (%s)",
                           (nome_funcionario,))
            self.conn.commit()
            messagebox.showinfo("Registro", "Funcionário cadastrado com sucesso.")

    def subtrair_estoque(self, id_pedido, nome_funcionario):
        # Seleciona todos os itens associados ao pedido
        self.c.execute("SELECT produto_id, quantidade_itens FROM itens WHERE pedido_id = %s", (id_pedido,))
        itens_pedido = self.c.fetchall()

        # Itera sobre os itens do pedido
        for item in itens_pedido:
            produto_id = item[0]
            quantidade_itens = item[1]

            # Subtrai a quantidade de itens do estoque do produto
            self.c.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s",
                           (quantidade_itens, produto_id))
            self.conn.commit()

        # Atualiza o campo 'forma_pagamento' para informar que o pedido foi pago
        self.c.execute("UPDATE pedidos SET forma_pagamento = CONCAT(forma_pagamento, ' -Pago ') WHERE id_pedido = %s",
                       (id_pedido,))
        self.conn.commit()

        valor_venda = search.Busca().valor_total_pedido(id_pedido)

        self.c.execute("UPDATE funcionarios SET total_vendas_mes = total_vendas_mes + %s WHERE nome = %s",
                       (valor_venda, nome_funcionario))
        self.conn.commit()

        messagebox.showinfo('Alteração de Estoque', f'O estoque dos itens do ID: {id_pedido} foram atualizado com '
                                                    f'sucesso!')

    def relatorio_vendas(self, nome_funcionario):
        self.c.execute("SELECT nome, total_vendas_mes FROM funcionarios WHERE nome = %s",
                       (nome_funcionario,))
        rows = self.c.fetchall()
        nome = 0
        total_vendas = 0
        for row in rows:
            nome = row[0]
            total_vendas = row[1]
        return [nome, total_vendas]
