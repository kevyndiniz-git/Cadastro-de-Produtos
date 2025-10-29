import pandas as pd
import os

ESTOQUE_FILE = r"C:\Users\rosec\Downloads\desafio cadastro\atividade cadastro\estoque_loja_pecas.xlsx"

# --- FUNÇÕES DE ARQUIVO E ESTOQUE PRINCIPAL ---

def carregar_estoque():
    """Carrega os produtos do Excel para a lista em memória."""
    if os.path.exists(ESTOQUE_FILE):
        try:
            df = pd.read_excel(ESTOQUE_FILE)
            return df.to_dict(orient="records")
        except Exception as e:
            print(f"Erro ao carregar o arquivo '{ESTOQUE_FILE}': {e}")
            print("Verifique se o arquivo está fechado e no formato correto.")
    print(f"Aviso: Arquivo '{ESTOQUE_FILE}' não encontrado. Iniciando com estoque vazio.")
    return []

def salvar_estoque(estoque_lista):
    """Salva os produtos da lista em memória no Excel."""
    # Garante que todas as colunas necessárias estão presentes
    colunas = ["Código", "Descrição do Item", "Categoria", "Unidade", "Valor Unitário", "Quantidade", "Valor Total"]
    df = pd.DataFrame(estoque_lista, columns=colunas)
    df.to_excel(ESTOQUE_FILE, index=False)
    print("Estoque atualizado no Excel.")

def extract_quantity_from_unit(unit_str):
    """Tenta extrair um número inteiro do início da string de unidade. Ex: '20un' -> 20"""
    num_str = ''
    for char in unit_str:
        if char.isdigit():
            num_str += char
        elif num_str:
            # Pára quando encontra um não-dígito após dígitos
            break
    try:
        # Retorna o número extraído ou 1 (padrão para 'un', 'kg', 'L', etc.)
        return int(num_str) if num_str else 1
    except ValueError:
        return 1

def obter_dados_item():
    """Pede e retorna os dados do item na ordem solicitada, usando o campo Unidade para Quantidade."""
    print("-" * 30)
    codigo = input("Código do item: ").upper().strip()
    descricao = input("Descrição do Item: ").strip()
    categoria = input("Categoria (Matéria-Prima ou Produto Acabado): ").strip()
    unidade_str = input("Unidade (ex: kg, L, un): ").strip() # Armazena a string completa

    # ORDEM EXATA SOLICITADA
    try:
        valor_un = float(input("Valor Unitário (R$): "))
        
        # LOGICA NOVA: Extrai a quantidade da string de unidade
        quantidade = extract_quantity_from_unit(unidade_str) 
        
        # CÁLCULO OBRIGATÓRIO: Valor Total = Valor Unitário x Quantidade extraída
        valor_total = valor_un * quantidade
        
    except ValueError:
        print("Entrada inválida para Valor. Usando 0.")
        valor_un = 0.0
        quantidade = 0
        valor_total = 0.0
        
    return {
        "Código": codigo, 
        "Descrição do Item": descricao, 
        "Categoria": categoria, 
        "Unidade": unidade_str, # Guarda a string original (ex: "20un")
        "Valor Unitário": valor_un,
        "Quantidade": quantidade, # Guarda o número extraído (ex: 20)
        "Valor Total": valor_total
    }

def adicionar_ao_estoque(estoque_lista, produto):
    """Adiciona um produto ou atualiza se o código já existir."""
    indices = [i for i, item in enumerate(estoque_lista) if item["Código"] == produto["Código"]]

    if indices:
        estoque_lista[indices[0]] = produto
        print(f"\nProduto {produto['Código']} atualizado!")
    else:
        estoque_lista.append(produto)
        print(f"\nProduto {produto['Código']} adicionado!")
        
    salvar_estoque(estoque_lista)


def exibir_pilha(estoque_lista, titulo="Pilha de Produtos"):
    """Exibe os itens em formato de pilha (último no topo), mostrando Valor Unitário e Valor Total."""
    if not estoque_lista:
        print("\nNenhum produto cadastrado.")
        return
        
    print(f"\n--- {titulo} (Mais Recente no Topo) ---")
    
    # Colunas de exibição
    print(f"{'CÓDIGO':<10} | {'DESCRIÇÃO DO ITEM':<30} | {'UND':<8} | {'QTD':<5} | {'R$ UN':<10} | {'R$ TOTAL':<12}")
    print("-" * 90)
    
    for produto in reversed(estoque_lista):
        valor_un = produto.get("Valor Unitário", 0.0)
        quantidade = produto.get("Quantidade", 0)
        valor_total_exibicao = produto.get("Valor Total", valor_un * quantidade)
        
        print(
            f"{produto['Código']:<10} | "
            f"{produto['Descrição do Item']:<30} | "
            f"{produto['Unidade']:<8} | "
            f"{quantidade:<5} | "
            f"R$ {valor_un:<5.2f} | "
            f"R$ {valor_total_exibicao:<7.2f}"
        )
    print("-" * 90)

def excluir_item(estoque_lista):
    """Remove um item do estoque pelo código e salva a alteração."""
    if not estoque_lista:
        print("\nNenhum produto para excluir.")
        return
        
    codigo = input("Digite o código do item para excluir: ").upper().strip()
    
    estoque_atualizado = [produto for produto in estoque_lista if produto["Código"] != codigo]
    
    if len(estoque_atualizado) < len(estoque_lista):
        estoque_lista[:] = estoque_atualizado
        print(f"\nProduto {codigo} excluído com sucesso!")
        salvar_estoque(estoque_lista)
    else:
        print("Código não encontrado na pilha atual.")

def consultar_dados():
    """Consulta dados diretamente no arquivo Excel."""
    if not os.path.exists(ESTOQUE_FILE):
        print("Arquivo Excel não encontrado. Por favor, cadastre um item primeiro.")
        return
        
    try:
        df = pd.read_excel(ESTOQUE_FILE)
    except Exception as e:
        print(f"Erro ao abrir arquivo: {e}")
        return
    
    while True:
        codigo = input("Digite o código do item (ou 'sair' para encerrar a consulta): ").upper().strip()
        if codigo == "SAIR":
            print("Encerrando consulta...")
            break

        item = df[df["Código"] == codigo]
        if not item.empty:
            print("\nItem encontrado (do Excel):")
            print(item.to_string(index=False))
        else:
            print("Código não encontrado.")

# --- FUNÇÃO DE EXPORTAÇÃO ---

def exportar_para_excel(dados, arquivo):
    """Exporta para Excel usando Pandas."""
    if not dados:
        print("\nNão há dados para exportar.")
        return
    try:
        df = pd.DataFrame(dados)
        df.to_excel(arquivo, index=False)
        print(f"\n[SUCESSO] Dados exportados para o Excel: {arquivo}")
    except Exception as e:
        print(f"\n[ERRO] Falha ao exportar para Excel: {e}")

def menu_exportacao_final(dados):
    """Pergunta sobre a exportação, agora apenas para Excel."""
    if not dados:
        print("Nenhum item cadastrado para exportação.")
        return
        
    while True:
        formato = input("Deseja exportar os dados para o Excel? (s/n): ").lower().strip()
        
        if formato == "s":
            exportar_para_excel(dados, ESTOQUE_FILE) 
            break
        elif formato == "n":
            print("Exportação cancelada.")
            break
        else:
            print("Opção inválida. Digite s ou n.")
            
# --- FLUXO DE CADASTRO OBRIGATÓRIO (Opção 1) ---

def cadastro_em_loop():
    """Implementa o fluxo de cadastro em loop, pilha por item e exportação final."""
    produtos_loop = []
    print("\n--- INICIANDO CADASTRO SIMPLIFICADO ---")
    
    while True:
        resposta = input("Deseja cadastrar um novo item? (s/n): ").lower().strip()
        
        if resposta == "s":
            novo_item = obter_dados_item()
            
            produtos_loop.append(novo_item)
            
            print("\n-- Produto cadastrado! --")
            
            exibir_pilha(produtos_loop, titulo="Pilha Atual")
            
        elif resposta == "n":
            break
            
        else:
            print("Opção inválida. Por favor, digite 's' para cadastrar ou 'n' para sair.")
            
    if produtos_loop:
        print("\n--- RESUMO FINAL DA LISTA CADASTRADA ---")
        exibir_pilha(produtos_loop, titulo="Lista Completa")
        
        menu_exportacao_final(produtos_loop)

# --- PROGRAMA PRINCIPAL ---

estoque = carregar_estoque()

while True:
    print("\n--- MENU PRINCIPAL ---")
    print("1. Cadastro Simplificado (Pilha e Exportação Final)") 
    print("2. Consultar produtos (direto do arquivo)")
    print("3. Visualizar pilha atual (do arquivo principal)")
    print("4. Excluir produto da pilha")
    print("5. Sair")
    
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        cadastro_em_loop()

    elif opcao == "2":
        consultar_dados()

    elif opcao == "3":
        exibir_pilha(estoque, titulo="Estoque Principal")

    elif opcao == "4":
        excluir_item(estoque)

    elif opcao == "5":
        print("Saindo do sistema. Até mais!")
        break

    else:
        print("Opção inválida. Escolha um número de 1 a 5.")