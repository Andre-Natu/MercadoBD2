from tkinter.ttk import *
from tkinter import *
# noinspection PyUnresolvedReferences
from tkinter import messagebox, ttk
from datetime import datetime

from PIL import ImageTk, Image

from tkcalendar import Calendar, DateEntry

import database
import datacliente
import datafuncionario
import dataitens
import datapedidos
import search


# datacliente.Clientes().adicionar_cliente('Andre', 'andre@fazoL.gmail', '(83)1234-5678')
# datapedidos.Pedidos().adicionar_pedido(2, 'boleto')
# dataitens.Itens().adicionar_produto_a_item(1, 2, 3, 7.66)
# dataitens.Itens().adicionar_produto_a_item(2, 2, 7, 3.54)
# dataitens.Itens().adicionar_produto_a_item(3, 2, 2, 9.54)

# datapedidos.Pedidos().alterar_view()

# datafuncionario.Funcionarios().create_table()

print("Clientes:")
for i in search.Busca().mostrar_todos_os_clientes():
    print(i)

print("itens:")
for row in search.Busca().mostrar_todos_os_itens():
    id_item, produto_id, pedido_id, quantidade, preco = row
    print(f"ID: {id_item}, Produto ID: {produto_id}, Pedido ID: {pedido_id}, Quantidade: {quantidade}, Preço: {preco}")


print("Pedidos:")
for i in search.Busca().mostrar_todos_os_pedidos():
    print(i)
