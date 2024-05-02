# **Mercado Bom Demais**

Um sistema de mercado para o projeto da disciplina 
de banco de dados com Marcelo Iuri
Alunos:
- Andre Lopes
- Antônio Rocha
- Elias Victor

![Logo](logo.png)

# **Sobre o código**:

1. O aplicativo utiliza uma storage procedure que foi criada fora do código. Seu detalhe é o segunte abaixo:

CREATE DEFINER=`root`@`localhost` PROCEDURE `AdicionarItemComDesconto`(
 IN produto_id INT,
 IN pedido_id INT,
 IN quantidade INT,
 IN preco DECIMAL(10, 2))
BEGIN
	DECLARE cliente_desconto TEXT;
	DECLARE novo_preco DECIMAL(10, 2);
    
    SELECT clientes.desconto INTO cliente_desconto
    FROM pedidos
    JOIN clientes ON pedidos.cliente_id = clientes.id_cliente
    WHERE pedidos.id_pedido = pedido_id;

    IF cliente_desconto IN ('mengão', 'one piece', 'sousa') THEN
        SET novo_preco = preco * 0.8;
    ELSE
        SET novo_preco = preco;
    END IF;

    INSERT INTO itens (produto_id, pedido_id, quantidade_itens, preco_itens)
    VALUES (produto_id, pedido_id, quantidade, novo_preco);
END



