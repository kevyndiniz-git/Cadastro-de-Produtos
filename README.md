**Documentação do Sistema de Estoque de Peças de Carro**
1. Descrição do Sistema
Este sistema é um mini-ERP de estoque voltado para uma loja de peças de carro. Ele permite cadastrar peças, consultar e listar o estoque, registrar movimentações (entrada e saída), gerar relatórios gerenciais e gráficos para análise de estoque.
Ele utiliza Python, MySQL para armazenamento de dados e Matplotlib para gráficos.

3. Estrutura do Banco de Dados
O sistema utiliza duas tabelas:
2.1 Tabela produtos
id: Identificador único da peça (auto-incremento)
nome: Nome da peça
categoria: Categoria da peça (Ex: Motor, Freio, Suspensão)
unidade: Unidade de medida (un, cx, kit, L)
preco: Preço unitário
quantidade: Quantidade atual no estoque

2.2 Tabela movimentacoes
id: Identificador único da movimentação
id_produto: ID da peça movimentada
tipo: Tipo de movimentação (E = Entrada, S = Saída)
quantidade: Quantidade movimentada
data_mov: Data e hora da movimentação

3. Funcionalidades do Sistema
3.1 Cadastro de Peças
Permite adicionar novas peças ao estoque, informando:
Nome
Categoria
Unidade
Preço
Quantidade

3.2 Consulta de Peças
Permite visualizar detalhes de uma peça específica pelo ID, incluindo quantidade e preço total.

3.3 Listagem de Estoque
Exibe todas as peças cadastradas, mostrando:
ID, Nome, Unidade, Quantidade, Preço unitário e Preço total
Destaque de peças com estoque baixo (menos de 5 unidades)

3.4 Exclusão de Peças
Permite remover uma peça do estoque pelo ID.

3.5 Movimentação de Estoque
Registra entradas e saídas de peças:
Entrada: Aumenta a quantidade no estoque
Saída: Reduz a quantidade (não permite saída maior que o estoque disponível)
Alerta se a quantidade ficar abaixo de 5 unidades
Registra automaticamente a movimentação na tabela movimentacoes

3.6 Relatórios Gerenciais
Giro de Estoque: Calcula quantas vezes o estoque foi movimentado com base nas saídas.
Custo de Manutenção: Calcula 2% do valor do estoque de cada peça.
Tempo Médio de Reposição: Informativo (assume 7 dias).
Estoque de Segurança: Calcula 10% da quantidade de cada peça.

3.7 Dashboard / Gráficos
Evolução do Estoque: Linha mostrando entradas e saídas de cada peça ao longo do tempo.
Produtos por Categoria: Gráfico de barras mostrando a quantidade total de peças por categoria.
Curva ABC de Custos: Ordena peças pelo custo total (quantidade x preço) para análise de prioridade.

4. Como Usar
Execute o código no terminal em Python.

Será exibido o menu principal:

--- MENU LOJA DE PEÇAS ---
1. Cadastrar Produto
2. Consultar Produto
3. Listar Produtos
4. Excluir Produto
5. Movimentar Estoque
6. Relatórios Gerenciais
7. Dashboard (Gráficos)
8. Sair

Digite a opção desejada e siga as instruções.

Para gráficos, escolha a opção 7 e depois o tipo de gráfico.

5. Observações Importantes
A quantidade mínima para alerta de estoque baixo é 5 unidades.
Todos os dados são salvos no MySQL; garanta que o banco estoque esteja criado com as tabelas produtos e movimentacoes.
