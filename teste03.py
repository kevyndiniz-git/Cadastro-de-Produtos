import pandas as pd
import os

ESTOQUE_FILE = r"C:\Users\rosec\Downloads\desafio cadastro\atividade cadastro\estoque_loja_pecas.xlsx"

# --- FUNÇÕES DE ARQUIVO E ESTOQUE PRINCIPAL ---

def atualizar_item(estoque):
    """Movimentar entrada e saida do estoque"""
    print("\n=== Movimentar Estoque (Entrada/Saída) ===")
    codigo = input("Digite o código do item: ".upper().strip())
    item = next((p for p in estoque if p ["Código"] == codigo),None)

    if not item:
        print("Item não encontrado.")
        return
    
    tipo = ""
    while tipo not in ("E","S"):
        tipo = input("Tipo (E = Entrada | S = Saída): ").strip().upper()

        try:
            qtd_mov = float(input('Quantidade da movimentção: '))
            if qtd_mov < 0:
                print ("Quantidade inválida. Operação cancelada.")
                return
        except ValueError:
            print("Entrada inválida. Operação cancelada.")

        qtd_atual = item["Quantidade"]
        valor_unit = item["Valor Unitário"]

        if tipo == "E":
            item["Quantidade"] = qtd_atual + qtd_mov
            print(f"Entrada registrada: +{qtd_mov}")
        else:
            if qtd_mov > qtd_atual:
                print(f"Erro: saída maior que estoque atual ({qtd_atual}). Opereção cancelada.")
                return
            item ["Quantidade"] = qtd_atual - qtd_mov
            print(f"Saída registrada: -{qtd_mov}")

        item ["Valor Total"] = item["Quantidade"] * valor_unit

        salvar_estoque(estoque)

        print("\nItem atualizado:")
        print(f"Código: {item['Código']} | Descrição: {item['Descrição do Item' ]} | Quantidade: {item['Quantidade']} | Valor Total: R$ {item['Valor Total']:.2f}")

def carregar_estoque():
    """Carrega os produtos do Excel para a lista em memória."""
    if os.path.exists(ESTOQUE_FILE):
        try:
            df = pd.read_excel(ESTOQUE_FILE)
            return df.to_dict(orient="records")
        except Exception as e:
            print(f"Erro ao carregar o arquivo '{ESTOQUE_FILE}': {e}")
    print(f"Aviso: Arquivo '{ESTOQUE_FILE}' não encontrado. Iniciando com estoque vazio.")
    return []

def salvar_estoque(estoque_lista):
    """Salva os produtos da lista em memória no Excel."""
    colunas = ["Código", "Descrição do Item", "Categoria", "Unidade", "Valor Unitário", "Quantidade", "Valor Total"]
    df = pd.DataFrame(estoque_lista, columns=colunas)
    try:
        df.to_excel(ESTOQUE_FILE, index=False)
        print("Estoque atualizado no Excel.")
    except PermissionError:
        print(f"Erro: Feche o arquivo '{ESTOQUE_FILE}' antes de salvar.")

def extract_quantity_from_unit(unit_str):
    """Extrai o primeiro número encontrado na string da unidade, padrão 1 se não achar."""
    num_str = ''.join(filter(str.isdigit, unit_str))
    try:
        return int(num_str) if num_str else 1
    except ValueError:
        return 1

def obter_dados_item():
    """Pede e retorna os dados do item."""
    print("-" * 30)
    codigo = input("Código do item: ").upper().strip()
    descricao = input("Descrição do Item: ").strip()
    categoria = input("Categoria (Matéria-Prima ou Produto Acabado): ").strip()
    unidade_str = input("Unidade (ex: 20un, kg, L): ").strip()

    try:
        valor_un = float(input("Valor Unitário (R$): "))
        quantidade = extract_quantity_from_unit(unidade_str)
        valor_total = valor_un * quantidade
    except ValueError:
        print("Entrada inválida. Usando 0 para valores.")
        valor_un = 0.0
        quantidade = 0
        valor_total = 0.0

    return {
        "Código": codigo,
        "Descrição do Item": descricao,
        "Categoria": categoria,
        "Unidade": unidade_str,
        "Valor Unitário": valor_un,
        "Quantidade": quantidade,
        "Valor Total": valor_total
    }

def adicionar_ao_estoque(estoque_lista, produto):
    """Adiciona ou atualiza produto e salva imediatamente."""
    indices = [i for i, item in enumerate(estoque_lista) if item["Código"] == produto["Código"]]
    if indices:
        estoque_lista[indices[0]] = produto
        print(f"\nProduto {produto['Código']} atualizado!")
    else:
        estoque_lista.append(produto)
        print(f"\nProduto {produto['Código']} adicionado!")
    salvar_estoque(estoque_lista)

def exibir_pilha(estoque_lista, titulo="Pilha de Produtos", limite=10):
    """Exibe itens em pilha (último no topo)."""
    if not estoque_lista:
        print("\nNenhum produto cadastrado.")
        return
    print(f"\n--- {titulo} (Mais Recente no Topo) ---")
    print(f"{'CÓDIGO':<10} | {'DESCRIÇÃO':<30} | {'UND':<8} | {'QTD':<5} | {'R$ UN':<10} | {'R$ TOTAL':<12}")
    print("-" * 90)
    for produto in reversed(estoque_lista[-limite:]):
        print(f"{produto['Código']:<10} | {produto['Descrição do Item']:<30} | {produto['Unidade']:<8} | "
              f"{produto['Quantidade']:<5} | R$ {produto['Valor Unitário']:<5.2f} | R$ {produto['Valor Total']:<7.2f}")
    print("-" * 90)

def excluir_item(estoque_lista):
    """Remove item pelo código e salva."""
    if not estoque_lista:
        print("\nNenhum produto para excluir.")
        return
    codigo = input("Digite o código do item para excluir: ").upper().strip()
    estoque_atualizado = [p for p in estoque_lista if p["Código"] != codigo]
    if len(estoque_atualizado) < len(estoque_lista):
        estoque_lista[:] = estoque_atualizado
        print(f"\nProduto {codigo} excluído com sucesso!")
        salvar_estoque(estoque_lista)
    else:
        print("Código não encontrado.")

def consultar_dados():
    """Consulta produtos direto no Excel."""
    if not os.path.exists(ESTOQUE_FILE):
        print("Arquivo não encontrado.")
        return
    try:
        df = pd.read_excel(ESTOQUE_FILE)
    except Exception as e:
        print(f"Erro ao abrir arquivo: {e}")
        return
    while True:
        codigo = input("Código do item (ou 'sair'): ").upper().strip()
        if codigo == "SAIR":
            break
        item = df[df["Código"] == codigo]
        if not item.empty:
            print(item.to_string(index=False))
        else:
            print("Código não encontrado.")

def cadastro_em_loop(estoque_lista):
    """Cadastro simplificado com atualização direta no estoque principal."""
    print("\n--- INICIANDO CADASTRO ---")
    while True:
        resposta = input("Cadastrar novo item? (s/n): ").lower().strip()
        if resposta == "s":
            novo_item = obter_dados_item()
            adicionar_ao_estoque(estoque_lista, novo_item)
            exibir_pilha(estoque_lista, titulo="Pilha Atual")
        elif resposta == "n":
            break
        else:
            print("Opção inválida. Digite 's' ou 'n'.")

# --- PROGRAMA PRINCIPAL ---
estoque = carregar_estoque()

while True:
    print("\n--- MENU PRINCIPAL ---")
    print("1. Cadastro Simplificado") 
    print("2. Consultar produtos")
    print("3. Visualizar pilha atual")
    print("4. Excluir produto")
    print("5- Movimentar Estoque")
    print("6. Sair")
    
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == "1":
        cadastro_em_loop(estoque)
    elif opcao == "2":
        consultar_dados()
    elif opcao == "3":
        exibir_pilha(estoque, titulo="Estoque Principal")
    elif opcao == "4":
        excluir_item(estoque)
    elif opcao == "5":
        atualizar_item(estoque)
    elif opcao == "6":
        print("Saindo do sistema.")
        break
    else:
        print("Opção inválida.")
