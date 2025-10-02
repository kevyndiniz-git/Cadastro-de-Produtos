import pandas as pd

# Caminho da planilha
caminho = r"C:\Users\rosec\Downloads\desafio cadastro\atividade cadastro\estoque_loja_pecas.xlsx"
df = pd.read_excel(caminho)

# Loop de consulta
while True:
    codigo = input("Digite o código do item (ou 'sair' para encerrar): ")
    if codigo.lower() == "sair":
        print("Encerrando consulta...")
        break

    item = df[df["Código"] == codigo.upper()]
    if not item.empty:
        print("\nItem encontrado:")
        print(item)
    else:
        print("❌ Código não encontrado.")
