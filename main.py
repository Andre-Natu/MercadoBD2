from tkinter.ttk import *
from tkinter import *
# noinspection PyUnresolvedReferences
from tkinter import messagebox, ttk
from datetime import datetime

from PIL import ImageTk, Image

from tkcalendar import Calendar, DateEntry

import database


def procurar():
    nome_produto = e_procurar.get()
    dados = database.registro.pesquisar_produto(nome_produto)

    # apaga os dados anteriores nos campos
    e_nome.delete(0, END)
    e_quantidade.delete(0, END)
    preco.delete(0, END)
    data_validade.delete(0, END)

    # coloca os dados pesquisados nos campos
    e_nome.insert(END, dados[1])
    e_quantidade.insert(END, dados[2])
    preco.insert(END, dados[3])
    data_validade.insert(END, dados[4])


def registrar():
    # guarda os dados colocados nos campos
    nome = e_nome.get()
    quantidade = e_quantidade.get()
    valor = preco.get()
    data_antiga = data_validade.get()
    validade = data_validade.get_date().strftime('%Y-%m-%d')

    database.registro.registrar_produto(nome, quantidade, valor, validade)
    mostrar_produtos()


def atualizar():
    nome_anterior = e_procurar.get()
    nome = e_nome.get()
    quantidade = e_quantidade.get()
    valor = preco.get()
    data_antiga = data_validade.get()
    validade = data_validade.get_date().strftime('%Y-%m-%d')
    rowid = database.registro.obter_id(nome_anterior)

    database.registro.alterar_produto((rowid, nome, quantidade, valor, validade))
    mostrar_produtos()


def remover():
    nome_anterior = e_procurar.get()
    rowid = database.registro.obter_id(nome_anterior)

    database.registro.remover_produto(rowid)
    mostrar_produtos()


def relatorio():
    estoque = database.registro.relatorio()

    messagebox.showinfo('Relatório de Estoque',
                        f'Quantidade de Produtos no estoque: {estoque[0]}\n'
                        f' Valor total do preço dos produtos: R$ {estoque[1]}\n')


# cores
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # Branca
co2 = "#e5e5e5"
co3 = "#00a095"
co4 = "#403d3d"
co6 = "#003452"

# criando janela
janela = Tk()
janela.title("")
janela.geometry('470x535')
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

# Criando os campos de entrada ----------------------------------

l_nome = Label(frame_detalhes, text="Nome do Produto", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_nome.place(x=4, y=13)
e_nome = Entry(frame_detalhes, width=30, justify='left', relief='solid')
e_nome.place(x=7, y=43)

l_quantidade = Label(frame_detalhes, text="Quantidade", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_quantidade.place(x=4, y=65)
e_quantidade = Entry(frame_detalhes, width=10, justify='left', relief='solid')
e_quantidade.place(x=7, y=90)

l_preco = Label(frame_detalhes, text="Preço", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_preco.place(x=120, y=65)
preco = Entry(frame_detalhes, width=10, justify='left', relief='solid')
preco.place(x=124, y=90)

l_data_validade = Label(frame_detalhes, text="Data de Validade", anchor=NW, font='Ivy 10', bg=co1, fg=co4)
l_data_validade.place(x=4, y=115)
data_validade = DateEntry(frame_detalhes, width=18, justify='center', background='darkblue', foreground='white',
                          borderwidth=2, year=2023)
data_validade.place(x=4, y=135)

app_img_report = Image.open('report.png')
app_img_report = app_img_report.resize((25, 25))
app_img_report = ImageTk.PhotoImage(app_img_report)
app_relatorio = Button(frame_detalhes, command=relatorio, image=app_img_report, text="Relatório", width=200, height=25,
                       compound=LEFT,
                       relief=GROOVE,
                       overrelief=RIDGE, font='Ivy 11', bg=co1, fg=co0)
app_relatorio.place(x=0, y=173)


# Tabela Alunos
def mostrar_produtos():
    dados_produtos = database.registro.visualizar_todos_produtos()

    # creating a treeview with dual scrollbars
    list_header = ['id', 'Nome', 'Quantidade', 'Preço', 'Validade']

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

    hd = ["center", "center", "center", "center", "center"]
    h = [40, 150, 100, 70, 70]
    n = 0

    for col in list_header:
        lista_produto.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        lista_produto.column(col, width=h[n], anchor=hd[n])

        n += 1

    for item in dados_produtos:
        lista_produto.insert('', 'end', values=item)


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

# linha separatória ---------------------------------------------------

l_linha = Label(frame_botoes, relief=GROOVE, text='h', width=1, height=123, anchor=NW, font='Ivy 1', bg=co1, fg=co0)
l_linha.place(x=240, y=15)

# chamar a tabela
mostrar_produtos()

janela.mainloop()
