import mysql.connector
from tkinter import messagebox
from tkinter.simpledialog import askstring
from Connection import Conexao


class Busca:

    def __init__(self):
        # Carregando a conexão com o Banco de dados
        self.db_connection = Conexao()
        self.c = self.db_connection.c
        self.conn = self.db_connection.conn

    def obter_id(self, nome):
        self.c.execute("SELECT id FROM produtos WHERE nome = %s", (nome,))

        rowid = self.c.fetchone()
        if rowid:
            return rowid[0]
        else:
            messagebox.showinfo("Erro", "Erro, o produto não foi encontrado")
            return None

    def obter_id_cliente(self, nome):
        self.c.execute("SELECT id_cliente FROM clientes WHERE nome = %s", (nome,))

        rowid = self.c.fetchone()
        if rowid:
            return rowid[0]
        else:
            messagebox.showinfo("Erro", "Erro, o cliente não foi encontrado")
            return None

    def pesquisar_produto_nome(self, nome):
        self.c.execute("SELECT * FROM produtos WHERE nome = %s", (nome,))
        dados = self.c.fetchone()

        return dados

    def pesquisar_produtos_total(self):
        self.c.execute("SELECT * FROM produtos")
        dados = self.c.fetchall()

        return dados

    def pesquisar_produtos_fabricados_por_mari(self):
        self.c.execute("SELECT * FROM produtos WHERE fabricado_mari = 'Sim'")
        dados = self.c.fetchall()

        return dados

    def pesquisar_produtos_por_preco(self, preco_min, preco_max):
        self.c.execute("SELECT * FROM produtos WHERE preco BETWEEN %s AND %s", (preco_min, preco_max))
        dados = self.c.fetchall()

        return dados

    def pesquisar_produtos_por_categoria(self, categoria):

        self.c.execute("SELECT * FROM produtos WHERE categoria = %s", (categoria,))
        dados = self.c.fetchall()

        return dados

    def pesquisar_produtos_baixa_quantidade(self):
        self.c.execute("SELECT * FROM produtos WHERE quantidade <= 5")
        dados = self.c.fetchall()

        return dados

    def opcoes_filtro(self, filtro, categoria, preco_min, preco_max, nome_cliente, id_pedido):
        opcoes = {
            'Todos os Produtos': self.pesquisar_produtos_total,
            'Fabricados em Mari': self.pesquisar_produtos_fabricados_por_mari,
            'Por Categoria': lambda: self.pesquisar_produtos_por_categoria(categoria),
            'Por Preço': lambda: self.pesquisar_produtos_por_preco(preco_min, preco_max),
            'Menos de 5 unidades': self.pesquisar_produtos_baixa_quantidade,
            'Histórico de pedidos': self.mostrar_todos_os_pedidos,
            'Seu Histórico de pedidos': lambda: self.mostrar_pedidos_cliente(nome_cliente),
            'Pedido Atual': lambda: self.mostrar_pedido_atual(id_pedido)
        }

        # Executa a função correspondente ao filtro ou mostra uma mensagem de erro se o filtro não existir
        if filtro in opcoes:
            return opcoes[filtro]()
        else:
            messagebox.showinfo("Erro", "Opção de filtro inválida.")

    def mostrar_todos_os_clientes(self):
        self.c.execute("SELECT * FROM clientes")
        dados = self.c.fetchall()

        return dados

    # Mostra todos os pedidos na view
    def mostrar_todos_os_pedidos(self):
        self.c.execute("SELECT * FROM detalhes_pedido_cliente;")
        dados = self.c.fetchall()

        return dados

    def mostrar_pedidos_cliente(self, nome_cliente):
        self.c.execute("SELECT * FROM detalhes_pedido_cliente WHERE nome_cliente = %s", (nome_cliente,))
        dados = self.c.fetchall()

        return dados

    def mostrar_pedido_atual(self, id_pedido):
        if id_pedido == 0:
            messagebox.showinfo("Erro", "Você não possui nenhum pedido atual.")
        self.c.execute("SELECT * FROM detalhes_pedido_cliente WHERE id_pedido = %s", (id_pedido,))
        dados = self.c.fetchall()

        return dados

    def mostrar_todos_os_itens(self):
        self.c.execute("SELECT * FROM itens")
        dados = self.c.fetchall()

        return dados

    def valor_total_pedido(self, id_pedido):
        self.c.execute("SELECT * FROM itens WHERE pedido_id = %s", (id_pedido,))
        dados = self.c.fetchall()

        total_itens = 0
        preco_total = 0.0

        for i in dados:
            preco_total += float(i[3] * i[4])

        preco_total = round(preco_total, 2)

        return preco_total
