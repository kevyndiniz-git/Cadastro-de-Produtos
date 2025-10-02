estoque = []

while True:
    print("\n--- Menu do Estoque ---")
    print("1 - Cadastrar produto")
    print("2 - Excluir produto")
    print("3 - Dar baixa em produto")
    print("4 - Mostrar estoque")
    print("5 - Sair")

    opcao = int(input("Escolha a opção: "))

    if opcao == 1:
        nome = input("Nome: ")
        qtd = int(input("Qtd: "))
        valor = float(input("Valor unitário: "))
        estoque.append([nome, qtd, valor])  
        print("Produto cadastrado!")

    elif opcao == 2:
        nome = input("Nome do produto pra remover: ")
        for item in estoque:
            if item[0] == nome:
                estoque.remove(item)
                print("Removido!")
                break
        else:
            print("Produto não encontrado.")

    elif opcao == 3:
        nome = input("Nome do produto: ")
        for item in estoque:
            if item[0] == nome:
                baixa = int(input("Quantidade a dar baixa: "))
                if 0 < baixa <= item[1]:
                    item[1] -= baixa
                    print("Baixa feita!")
                    if item[1] == 0:
                        estoque.remove(item)
                        print("Produto zerou e foi removido.")
                else:
                    print("Quantidade inválida.")
                break
        else:
            print("Produto não encontrado.")

    elif opcao == 4:
        if not estoque:
            print("Estoque vazio.")
        else:
            for nome, qtd, valor in estoque:
                print(f"{nome} | Qtd: {qtd} | R$ {valor:.2f} un | Total: R$ {qtd*valor:.2f}")

    elif opcao == 5:
        print("Saindo...")
        break

    else:
        print("Opção inválida.")
