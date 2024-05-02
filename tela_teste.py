import database


produtos_totais = database.registro.visualizar_todos_produtos()

# Definindo o formato da saída
formato_produto = "ID: {}, Nome: {}, Quantidade: {}, Preço: R${}, Data de Validade: {}"

for produto in produtos_totais:
    # Desempacotando os dados do produto
    id_produto, nome, quantidade, preco, data_validade = produto

    # Formatando a saída usando o formato definido
    print(formato_produto.format(id_produto, nome, quantidade, preco, data_validade))

    comprar = True

    while comprar:
        print("Digite o ID produto que você irá adicionar ao carrinho: ")
        id_item = input()
        print("Digite a quantidade que você ira adicionar ao carrinho: ")
        quantidade_item = input()
        print("Digite 1 para adicionar outro produto ao carrinho, digite 2 para ir para o carrinho:")
        opcao = input()
        if opcao == 2:
            comprar = False

    