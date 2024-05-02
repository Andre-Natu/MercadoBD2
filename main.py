from tkinter.ttk import *
from tkinter import *
# noinspection PyUnresolvedReferences
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime

from PIL import ImageTk, Image

from tkcalendar import Calendar, DateEntry

import database
import datafuncionario
import search


def procurar():
    nome_produto = e_procurar.get()
    dados = search.Busca().pesquisar_produto_nome(nome_produto)

    # apaga os dados anteriores nos campos
    e_nome.delete(0, END)
    e_quantidade.delete(0, END)
    preco.delete(0, END)
    data_validade.delete(0, END)

    # coloca os dados pesquisados nos campos
    e_nome.insert(END, dados[1])
    e_quantidade.insert(END, dados[2])
    preco.insert(END, dados[3])
    var_categoria.set(dados[4])
    var_opcao.set(dados[5])
    data_validade.insert(END, dados[6])


def registrar():
    # guarda os dados colocados nos campos
    nome = e_nome.get()
    quantidade = e_quantidade.get()
    valor = preco.get()
    data_antiga = data_validade.get()
    validade = data_validade.get_date().strftime('%Y-%m-%d')
    categoria = var_categoria.get()
    fabricado_mari = var_opcao.get()

    database.registro.registrar_produto(nome, quantidade, valor, categoria, fabricado_mari, validade)
    mostrar_produtos("Todos os Produtos", 0, 0, 0)


def atualizar():
    nome_anterior = e_procurar.get()
    nome = e_nome.get()
    quantidade = e_quantidade.get()
    valor = preco.get()
    data_antiga = data_validade.get()
    validade = data_validade.get_date().strftime('%Y-%m-%d')
    rowid = search.Busca().obter_id(nome_anterior)
    categoria = var_categoria.get()
    fabricado_mari = var_opcao.get()

    database.registro.alterar_produto((rowid, nome, quantidade, valor, categoria, fabricado_mari, validade))
    mostrar_produtos("Todos os Produtos", 0, 0, 0)


def remover():
    nome_anterior = e_procurar.get()
    rowid = search.Busca().obter_id(nome_anterior)

    database.registro.remover_produto(rowid)
    mostrar_produtos("Todos os Produtos", 0, 0, 0)


def relatorio():
    resposta = messagebox.askyesno('Relatorio', 'Aperte Sim para verificar o relatório de estoque, aperte Nao para '
                                                'verificar o relatório de vendas')
    if resposta:
        estoque = database.registro.relatorio()
        messagebox.showinfo('Relatório de Estoque',
                            f'Quantidade de Produtos no estoque: {estoque[0]}\n'
                            f' Valor total do preço dos produtos: R$ {estoque[1]}\n')
    else:
        nome_funcionario = e_nome_funcionario.get()

        if nome_funcionario == '':
            messagebox.showerror('Erro', 'Por favor, logue como funcionário')
        else:
            vendas = datafuncionario.Funcionarios().relatorio_vendas(nome_funcionario)
            messagebox.showinfo('Relatório de Vendas',
                                f'O Funcionário {vendas[0]}\n'
                                f' Conseguiu nesse mês um total das vendas igual a: R$ {vendas[1]}\n')


def efetuar_venda():
    nome_funcionario = e_nome_funcionario.get()
    id_pedido = simpledialog.askinteger("Confirmar Venda", "Digite o id do pedido que deseja marcar como vendido:")
    datafuncionario.Funcionarios().subtrair_estoque(id_pedido, nome_funcionario)

    var_filtro.set("Todos os Produtos")
    filtrar_produtos()


def logar():
    nome_funcionario = e_nome_funcionario.get()

    datafuncionario.Funcionarios().inserir_funcionarios(nome_funcionario)


def filtrar_produtos():
    categoria = var_categoria_filtro.get()
    price_min = preco_min.get()
    price_max = preco_max.get()
    mostrar_produtos(var_filtro.get(), categoria, price_min, price_max)


def menu_invisivel(opcao):
    if opcao == "Por Preço":
        tornar_visivel()
    else:
        tornar_invisivel()
    if opcao == "Por Categoria":
        tornar_visivel_categoria()
    else:
        tornar_invisivel_categoria()


def tornar_invisivel(event=None):
    l_preco_min.place(anchor="nw", x=0, y=0, width=0, height=0)
    l_preco_max.place(anchor="nw", x=0, y=0, width=0, height=0)
    preco_min.place(anchor="nw", x=0, y=0, width=0, height=0)
    preco_max.place(anchor="nw", x=0, y=0, width=0, height=0)


def tornar_visivel(event=None):
    l_preco_min.place(anchor="nw", x=0, y=70, width=85, height=20)
    l_preco_max.place(anchor="nw", x=0, y=95, width=90, height=20)
    preco_min.place(anchor="nw", x=100, y=70, width=75, height=20)
    preco_max.place(anchor="nw", x=100, y=95, width=75, height=20)


def tornar_invisivel_categoria():
    l_categoria_filtro.place(x=0, y=0, width=0, height=0)
    e_categoria_filtro.place(x=0, y=0, width=0, height=0)


def tornar_visivel_categoria():
    l_categoria_filtro.place(x=0, y=70, width=175, height=30)
    e_categoria_filtro.place(x=0, y=95, width=180, height=20)


# cores
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # Branca
co2 = "#e5e5e5"
co3 = "#00a095"
co4 = "#403d3d"
co6 = "#003452"

# Categorias de Produtos
categorias = ['Alimento', 'Bebidas', 'Higiene Pessoal', 'Limpeza', 'Padaria', 'Frios']

filtros = ['Todos os Produtos', 'Fabricados em Mari', 'Por Categoria', 'Por Preço', 'Menos de 5 unidades',
           'Histórico de pedidos']

# criando janela
janela = Tk()
janela.title("")
janela.geometry('808x535')
janela.configure(background=co1)
janela.resizable(width=FALSE, height=FALSE)

style = Style(janela)
style.theme_use("clam")

# Criando Frames
frame_logo = Frame(janela, width=850, height=52, bg=co6)
frame_logo.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW, columnspan=5)

frame_botoes = Frame(janela, width=100, height=200, bg=co1, relief=RAISED)
frame_botoes.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frame_detalhes = Frame(janela, width=600, height=100, bg=co1, relief=SOLID)
frame_detalhes.grid(row=1, column=1, pady=1, padx=10, sticky=NSEW)

frame_tabela = Frame(janela, width=600, height=100, bg=co1, relief=SOLID)
frame_tabela.grid(row=3, column=0, pady=0, padx=10, sticky=NSEW, columnspan=5)

# Trabalhando no frame logo ------------------------------------
global imagem, imagem_string, l_imagem

app_lg = Image.open('logo.png')
app_lg = app_lg.resize((45, 45))
app_lg = ImageTk.PhotoImage(app_lg)
app_logo = Label(frame_logo, image=app_lg, text=" Supermercado Bom Demais", width=850, compound=LEFT, anchor=NW,
                 font='Verdana 15', bg=co6, fg=co1)
app_logo.place(x=5, y=0)

# Campo de informações dos produtos ----------------------------------

l_nome = Label(frame_detalhes, text="Nome do Produto", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_nome.place(x=204, y=13)
e_nome = Entry(frame_detalhes, width=30, justify='left', relief='solid')
e_nome.place(x=207, y=43)

var_categoria = StringVar()
l_categoria = Label(frame_detalhes, text="Categoria do Produto", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_categoria.place(x=204, y=110)
e_categoria = Combobox(frame_detalhes, textvariable=var_categoria, values=categorias, state="readonly")
e_categoria.place(x=207, y=130)

l_quantidade = Label(frame_detalhes, text="Quantidade", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_quantidade.place(x=204, y=65)
e_quantidade = Entry(frame_detalhes, width=10, justify='left', relief='solid')
e_quantidade.place(x=207, y=90)

l_preco = Label(frame_detalhes, text="Preço", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_preco.place(x=320, y=65)
preco = Entry(frame_detalhes, width=10, justify='left', relief='solid')
preco.place(x=324, y=90)

var_opcao = StringVar()
var_opcao.set("Sim")
l_fabricado = Label(frame_detalhes, text="De Mari?", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_fabricado.place(x=204, y=155)
e_fabricado = Combobox(frame_detalhes, textvariable=var_opcao, values=["Sim", "Não"], width=7, state="readonly")
e_fabricado.place(x=206, y=180)

l_data_validade = Label(frame_detalhes, text="Data de Validade", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_data_validade.place(x=284, y=155)
data_validade = DateEntry(frame_detalhes, width=14, justify='center', background='darkblue', foreground='white',
                          borderwidth=2, year=2023)
data_validade.place(x=284, y=180)

# Aba de vendas funcionário -----------------------------------------------

l_nome_funcionario = Label(frame_detalhes, text="Seu nome de funcionário", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_nome_funcionario.place(x=395, y=13)
e_nome_funcionario = Entry(frame_detalhes, width=23, justify='left', relief='solid')
e_nome_funcionario.place(x=400, y=43)

app_img_venda = Image.open('cart.png')
app_img_venda = app_img_venda.resize((25, 25))
app_img_venda = ImageTk.PhotoImage(app_img_venda)
app_venda = Button(frame_detalhes, command=efetuar_venda, image=app_img_venda, text="Confirmar Venda", width=137,
                   compound=LEFT,
                   relief=GROOVE,
                   overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_venda.place(x=400, y=172)

app_img_logar = Image.open('employee.png')
app_img_logar = app_img_logar.resize((25, 25))
app_img_logar = ImageTk.PhotoImage(app_img_logar)
app_logar = Button(frame_detalhes, command=logar, image=app_img_logar, text="Logar", width=137, compound=LEFT,
                   relief=GROOVE,
                   overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_logar.place(x=400, y=132)


# Lista dos produtos --------------------------------------------
def mostrar_produtos(filtro, categoria, price_min, price_max, nome_cliente="", id_pedido=0):
    dados_produtos = search.Busca().opcoes_filtro(filtro, categoria, price_min, price_max, nome_cliente, id_pedido)

    # creating a treeview with dual scrollbars
    if filtro == 'Histórico de pedidos':
        list_header = ['Pedido', 'Cliente', 'Pagamento', 'Nome Produto', 'Quantidade', 'Preço', 'Data de '
                                                                                                'Compra', 'id_item', ]
    else:
        list_header = ['id', 'Nome', 'Quantidade', 'Preço', 'Categoria', 'Fabricado em Mari', 'Validade', '']

    lista_produto = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")

    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=lista_produto.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=lista_produto.xview)

    lista_produto.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    lista_produto.grid(column=0, row=1, sticky='nsew')
    vsb.grid(column=1, row=1, sticky='ns')
    hsb.grid(column=0, row=2, sticky='ew')
    frame_tabela.grid_rowconfigure(0, weight=12)

    hd = ["center", "center", "center", "center", "center", "center", "center", "center"]
    h = [50, 110, 100, 100, 120, 120, 120, 50]
    n = 0

    for col in list_header:
        lista_produto.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        lista_produto.column(col, width=h[n], anchor=hd[n])

        n += 1

    for item in dados_produtos:
        lista_produto.insert('', 'end', values=item)


# Frame Opções ------------------------------------

var_filtro = StringVar()
var_filtro.set(filtros[0])

l_filtro = Label(frame_detalhes, text="Filtrar Produtos", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_filtro.place(x=4, y=10)
e_filtro = Combobox(frame_detalhes, textvariable=var_filtro, values=filtros, width=27, state="readonly")
e_filtro.place(x=0, y=40)

var_filtro.trace('w', lambda *args: menu_invisivel(var_filtro.get()))

l_preco_min = Label(frame_detalhes, text="Preço Mínimo", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_preco_min.place(x=0, y=70)
preco_min = Entry(frame_detalhes, width=10, justify='left', relief='solid')
preco_min.place(x=4, y=95)
l_preco_max = Label(frame_detalhes, text="Preço Máximo", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_preco_max.place(x=100, y=70)
preco_max = Entry(frame_detalhes, width=10, justify='left', relief='solid')
preco_max.place(x=104, y=95)
tornar_invisivel()

var_categoria_filtro = StringVar()
l_categoria_filtro = Label(frame_detalhes, text="Categoria do Produto", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_categoria_filtro.place(x=0, y=70)
e_categoria_filtro = Combobox(frame_detalhes, textvariable=var_categoria_filtro, values=categorias, width=27,
                              state="readonly")
e_categoria_filtro.place(x=0, y=95)
tornar_invisivel_categoria()

app_img_filter = Image.open('filter.png')
app_img_filter = app_img_filter.resize((25, 25))
app_img_filter = ImageTk.PhotoImage(app_img_filter)
app_relatorio = Button(frame_detalhes, command=filtrar_produtos, image=app_img_filter, text="Filtrar", width=175,
                       compound=LEFT,
                       relief=GROOVE,
                       overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_relatorio.place(x=0, y=133)

app_img_report = Image.open('report.png')
app_img_report = app_img_report.resize((25, 25))
app_img_report = ImageTk.PhotoImage(app_img_report)
app_relatorio = Button(frame_detalhes, command=relatorio, image=app_img_report, text="Relatório Estoque", width=175,
                       compound=LEFT,
                       relief=GROOVE,
                       overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_relatorio.place(x=0, y=173)

# Procurar produto -----------

frame_procurar = Frame(frame_botoes, width=20, height=100, bg=co1, relief=RAISED)
frame_procurar.grid(row=0, column=0, pady=10, padx=10, sticky=NSEW)

l_nome = Label(frame_procurar, text="Procurar produto por nome", height=1, anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_nome.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)
e_procurar = Entry(frame_procurar, width=5, justify='center', relief="solid", font='Ivy 10')
e_procurar.grid(row=1, column=0, pady=10, padx=0, sticky=NSEW)

botao_procurar = Button(frame_procurar, command=procurar, anchor=CENTER, text="Procurar", width=9, overrelief=RIDGE,
                        font='ivy 7 bold',
                        bg=co1, fg=co0)
botao_procurar.grid(row=1, column=1, pady=10, padx=0, sticky=NSEW)

# Botoes --------------------

app_img_adicionar = Image.open('add.png')
app_img_adicionar = app_img_adicionar.resize((25, 25))
app_img_adicionar = ImageTk.PhotoImage(app_img_adicionar)

app_adicionar = Button(frame_botoes,
                       command=registrar,
                       image=app_img_adicionar, text=" Adicionar", width=100, compound=LEFT,
                       relief=GROOVE, overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_adicionar.grid(row=1, column=0, pady=5, padx=10, sticky=NSEW)

app_img_atualizar = Image.open('update.png')
app_img_atualizar = app_img_atualizar.resize((25, 25))
app_img_atualizar = ImageTk.PhotoImage(app_img_atualizar)
app_atualizar = Button(frame_botoes, command=atualizar, image=app_img_atualizar, text=" Atualizar", width=100,
                       compound=LEFT,
                       relief=GROOVE, overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_atualizar.grid(row=2, column=0, pady=5, padx=10, sticky=NSEW)

app_img_deletar = Image.open('delete.png')
app_img_deletar = app_img_deletar.resize((25, 25))
app_img_deletar = ImageTk.PhotoImage(app_img_deletar)
app_deletar = Button(frame_botoes, command=remover, image=app_img_deletar, text=" Deletar", width=100, compound=LEFT,
                     relief=GROOVE,
                     overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_deletar.grid(row=3, column=0, pady=5, padx=10, sticky=NSEW)

# linhas separatórias ---------------------------------------------------

l_linha = Label(frame_botoes, relief=GROOVE, text='h', width=1, height=123, anchor=NW, font='Ivy 1', bg=co1, fg=co0)
l_linha.place(x=240, y=15)

l_linha2 = Label(frame_detalhes, relief=GROOVE, text='h', width=1, height=100, anchor=NW, font='Ivy 1', bg=co1, fg=co0)
l_linha2.place(x=190, y=15)

# chamar a tabela
mostrar_produtos(filtros[0], 0, 0, 0, )

janela.mainloop()
