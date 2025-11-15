import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt


"""FUNÇÕES DO SISTEMA"""
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="estoque"
    )

def carregar_estoque():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    con.close()
    return dados

def salvar_item(item):
    con = conectar()
    cursor = con.cursor()
    sql = """UPDATE produtos 
             SET nome=%s, categoria=%s, unidade=%s, preco=%s, quantidade=%s 
             WHERE id=%s"""
    cursor.execute(sql, (
        item["nome"], item["categoria"], item["unidade"],
        item["preco"], item["quantidade"], item["id"]
    ))
    con.commit()
    con.close()

def adicionar_item(produto):
    con = conectar()
    cursor = con.cursor()
    sql = """INSERT INTO produtos (nome, categoria, unidade, preco, quantidade)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        produto["nome"], produto["categoria"],
        produto["unidade"], produto["preco"], produto["quantidade"]
    ))
    con.commit()
    con.close()

def registrar_movimentacao(id_produto, tipo, quantidade):
    con = conectar()
    cursor = con.cursor()
    sql = "INSERT INTO movimentacoes (id_produto, tipo, quantidade, data_mov) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (id_produto, tipo, quantidade, datetime.now()))
    con.commit()
    con.close()

def excluir_item_mysql(id_produto):
    con = conectar()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
    produto = cursor.fetchone()

    cursor.execute("DELETE FROM produtos WHERE id = %s", (id_produto,))
    con.commit()
    con.close()

    return produto

def mostrar_tabela_item(p):
    total = float(p['preco']) * int(p['quantidade'])
    print("\n--- Detalhes do Produto ---")
    print(f"{'ID':<5} | {'NOME':<25} | {'CAT':<15} | {'UND':<6} | {'QTD':<5} | {'R$ UN':<10} | {'R$ TOTAL':<12}")
    print("-" * 90)
    print(f"{p['id']:<5} | {p['nome']:<25} | {p['categoria']:<15} | {p['unidade']:<6} | "
          f"{p['quantidade']:<5} | R$ {p['preco']:<10.2f} | R$ {total:<12.2f}")
    print("-" * 90)

def atualizar_item():
    print("\nMovimentar Estoque (Entrada/Saída)")
    try:
        codigo = int(input("ID do produto: "))
    except:
        print("ID inválido.")
        return
    
    produtos = carregar_estoque()
    item = next((p for p in produtos if p["id"] == codigo), None)

    if not item:
        print("Item não encontrado.")
        return
    
    tipo = ""
    while tipo not in ("E", "S"):
        tipo = input("Tipo (E = Entrada | S = Saída): ").strip().upper()

    try:
        qtd_mov = float(input("Quantidade: "))
        if qtd_mov < 0:
            print("Inválido.")
            return
    except:
        print("Inválido.")
        return
    
    qtd_atual = item["quantidade"]

    if tipo == "E":
        item["quantidade"] = qtd_atual + qtd_mov
    else:
        if qtd_mov > qtd_atual:
            print("Saída maior que estoque.")
            return
        item["quantidade"] = qtd_atual - qtd_mov

    salvar_item(item)
    registrar_movimentacao(item["id"], tipo, qtd_mov)

    print("\nMovimentação registrada com sucesso!")
    mostrar_tabela_item(item)

    if item["quantidade"] < 5:
        print(f"⚠️ Atenção: Estoque baixo! Apenas {item['quantidade']} unidades restantes.")

def obter_dados_item():
    print("-" * 30)
    nome = input("Nome: ").strip()
    categoria = input("Categoria: ").strip()
    unidade = input("Unidade (ex: un, cx, kg, L): ").strip()

    try:
        preco_str = input("Preço: ").strip().replace(",", ".")
        preco = float(preco_str)
        quantidade = int(input("Quantidade: "))
    except:
        print("Valores inválidos.")
        preco = 0
        quantidade = 0

    return {
        "nome": nome,
        "categoria": categoria,
        "unidade": unidade,
        "preco": preco,
        "quantidade": quantidade
    }

def adicionar_ao_estoque():
    novo = obter_dados_item()
    adicionar_item(novo)

    produtos = carregar_estoque()
    item = produtos[-1]

    print("\nProduto adicionado!")
    mostrar_tabela_item(item)

def exibir_planilha():
    produtos = carregar_estoque()
    if not produtos:
        print("\nNenhum produto encontrado.")
        return
    
    print("\n--- Estoque Principal ---")
    print(f"{'CÓDIGO':<10} | {'DESCRIÇÃO':<30} | {'UND':<8} | {'QTD':<5} | {'R$ UN':<10} | {'R$ TOTAL':<12}")
    print("-" * 90)

    for p in produtos:
        total = float(p['preco']) * int(p['quantidade'])
        alerta = "!BAIXO!" if int(p['quantidade']) < 5 else ""
        print(f"{p['id']:<10} | {p['nome']:<30} | {p['unidade']:<8} | {p['quantidade']:<5} {alerta:<6} | "
              f"R$ {p['preco']:<10.2f} | R$ {total:<12.2f}")

    print("-" * 90)

def excluir_item():
    try:
        idp = int(input("ID do produto: "))
    except:
        print("ID inválido.")
        return

    produto = excluir_item_mysql(idp)

    if produto:
        print(f"\nProduto excluído: ID {produto['id']} - {produto['nome']}")
    else:
        print("Produto não encontrado.")

def consultar_dados():
    produtos = carregar_estoque()

    try:
        idp = int(input("ID do produto: "))
    except:
        print("ID inválido.")
        return

    item = next((p for p in produtos if p["id"] == idp), None)

    if item:
        mostrar_tabela_item(item)
    else:
        print("Não encontrado.")


"""RELATÓRIOS GERENCIAIS"""
def relatorio_giro_estoque():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nome,
               SUM(CASE WHEN m.tipo = 'S' THEN m.quantidade ELSE 0 END) AS saidas,
               AVG(p.quantidade) AS media_estoque
        FROM produtos p
        LEFT JOIN movimentacoes m ON m.id_produto = p.id
        GROUP BY p.id
    """)
    dados = cursor.fetchall()
    con.close()

    print("\n--- Giro de Estoque ---")
    for d in dados:
        media = d["media_estoque"] if d["media_estoque"] else 1
        giro = (d["saidas"] or 0) / media
        print(f"{d['nome']}: Giro = {giro:.2f}")

def relatorio_custo_manutencao():
    produtos = carregar_estoque()

    print("\n--- Custo de Manutenção do Estoque ---")
    for p in produtos:
        custo = float(p["quantidade"]) * float(p["preco"]) * 0.02
        print(f"{p['nome']}: R$ {custo:.2f}")

def relatorio_tempo_reposicao():
    print("\n--- Tempo Médio de Reposição ---")
    print("Assumindo 7 dias de reposição para todos os itens.")

def relatorio_estoque_seguranca():
    produtos = carregar_estoque()
    print("\n--- Estoque de Segurança ---")
    for p in produtos:
        seg = p["quantidade"] * 0.10
        print(f"{p['nome']}: {seg:.1f} unidades")


"""GRÁFICOS"""
def grafico_evolucao():
    con = conectar()
    cursor = con.cursor(dictionary=True)

    sql = """
    SELECT 
        p.nome,
        m.data_mov,
        CASE WHEN m.tipo = 'E' THEN m.quantidade ELSE -m.quantidade END AS mov
    FROM movimentacoes m
    JOIN produtos p ON m.id_produto = p.id
    ORDER BY p.nome, m.data_mov
    """

    cursor.execute(sql)
    dados = cursor.fetchall()
    con.close()

    if not dados:
        print("Sem movimentações.")
        return

    produtos = {}
    for d in dados:
        nome = d["nome"]
        if nome not in produtos:
            produtos[nome] = {"datas": [], "movs": []}

        produtos[nome]["datas"].append(d["data_mov"])
        produtos[nome]["movs"].append(d["mov"])

    plt.figure(figsize=(10,5))
    for nome, info in produtos.items():
        plt.plot(info["datas"], info["movs"], marker="o", label=nome)

    plt.title("Evolução de Movimentações do Estoque")
    plt.xlabel("Data")
    plt.ylabel("Movimento (+entrada / -saída)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def grafico_categorias():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute("""
        SELECT categoria, SUM(quantidade) AS total
        FROM produtos
        GROUP BY categoria
    """)
    dados = cursor.fetchall()
    con.close()

    if not dados:
        print("Sem dados.")
        return

    categorias = [d["categoria"] for d in dados]
    totais = [d["total"] for d in dados]

    plt.bar(categorias, totais)
    plt.title("Produtos por Categoria")
    plt.show()

def grafico_curva_abc():
    produtos = carregar_estoque()

    lista = []
    for p in produtos:
        custo = p["quantidade"] * p["preco"]
        lista.append((p["nome"], custo))

    lista.sort(key=lambda x: x[1], reverse=True)

    nomes = [x[0] for x in lista]
    custos = [x[1] for x in lista]

    plt.plot(nomes, custos)
    plt.title("Curva ABC")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


"""MENU DO SISTEMA"""
while True:
    print("\n--- MENU ---")
    print("1. Cadastrar Produto")
    print("2. Consultar Produto")
    print("3. Listar Produtos")
    print("4. Excluir Produto")
    print("5. Movimentar Estoque")
    print("6. Relatórios Gerenciais")
    print("7. Dashboard (Gráficos)")
    print("8. Sair")

    opcao = input("Opção: ")

    if opcao == "1":
        adicionar_ao_estoque()
    elif opcao == "2":
        consultar_dados()
    elif opcao == "3":
        exibir_planilha()
    elif opcao == "4":
        excluir_item()
    elif opcao == "5":
        atualizar_item()

    elif opcao == "6":
        relatorio_giro_estoque()
        relatorio_custo_manutencao()
        relatorio_tempo_reposicao()
        relatorio_estoque_seguranca()

    elif opcao == "7":
        print("\n1 - Evolução do estoque")
        print("2 - Categorias")
        print("3 - Curva ABC")
        sub = input("Escolha o tipo de gráfico: ")

        if sub == "1":
            grafico_evolucao()
        elif sub == "2":
            grafico_categorias()
        elif sub == "3":
            grafico_curva_abc()
        else:
            print("Inválido.")

    elif opcao == "8":
        print("Saindo...")
        break
    else:
        print("Inválido.")
