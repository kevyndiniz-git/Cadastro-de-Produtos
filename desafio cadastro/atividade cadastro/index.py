estoque = []
opcao = 0

while opcao != 5:
    print("\n--- Menu do Estoque ---")
    print("1 - Cadastrar novo produto")
    print("2 - Excluir produto")
    print("3 - Dar baixa em um produto")
    print("4 - Visualizar estoque completo")
    print("5 - Sair")

    opcao = int(input("Escolha a opção: "))

    if opcao == 1:
        nome_item = input("Nome do produto: ")
        qtd = int(input("Quantidade: "))
        valor = float(input("Valor por unidade: "))
        total_valor = qtd * valor

        novo_produto = {
            "nome": nome_item,
            "quantidade": qtd,
            "valor_un": valor,
            "valor_total": total_valor
        }
        estoque.append(novo_produto)
        print("Produto cadastrado! Vamos pro próximo.")

    else:
        if opcao == 2:
            remover_nome = input("Qual produto você quer remover? ")
            encontrado = False

            for item in list(estoque):
                if item["nome"] == remover_nome:
                    estoque.remove(item)
                    print("Produto removido com sucesso!")
                    encontrado = True
                    break

            if not encontrado:
                print("Esse produto não foi encontrado.")

        else:
            if opcao == 3:
                nome_baixa = input("Nome do produto para dar baixa: ")
                encontrado = False

                for item in estoque:
                    if item["nome"] == nome_baixa:
                        encontrado = True
                        
                        quantidade_baixa = int(input(f"Quantas unidades de '{item['nome']}' você quer dar baixa? "))
                        if quantidade_baixa <= 0:
                            print("A baixa deve ser maior que zero.")
                        else:
                            if quantidade_baixa > item["quantidade"]:
                                print("Quantidade maior que o estoque atual!")
                            else:
                                item["quantidade"] -= quantidade_baixa
                                item["valor_total"] = item["quantidade"] * item["valor_un"]
                                print("Baixa feita!")

                                if item["quantidade"] == 0:
                                    estoque.remove(item)
                                    print(f"Produto '{item['nome']}' zerou o estoque e foi removido.")
                        
                        break
                if not encontrado:
                    print("Produto não encontrado.")
            else:
                if opcao == 4:
                    print("\n--- Itens em Estoque ---")
                    if not estoque:
                        print("Estoque vazio.")
                    else:
                        for item in estoque:
                            print(f"Nome: {item['nome']}")
                            print(f"Quantidade: {item['quantidade']}")
                            print(f"Valor Unitário: R$ {item['valor_un']:.2f}")
                            print(f"Valor Total: R$ {item['valor_total']:.2f}")
                            print("-" * 20)
                else:
                    if opcao == 5:
                        print("Saindo do sistema!!")
                    else:
                        print("Opção inválida, tente novamente apenas de 1 a 5.")