from PyQt5.QtCore import Qt  

def setTextAlterarProdutos(ui):
    # Conecta o sinal de clique da tabela à função que preenche os QLineEdit
    ui.tabela_alterar_produto.cellClicked.connect(lambda row, column: preencherCampos(ui, row))

def preencherCampos(ui, row):
    dados_linha = []
    for col in range(ui.tabela_alterar_produto.columnCount()):
        item = ui.tabela_alterar_produto.item(row, col)
        if item is not None:
            dados_linha.append(item.text())
        else:
            dados_linha.append('')

    # Preenche os campos
    ui.line_nome_alterar_produto.setText(dados_linha[0])  # Nome do produto
    ui.line_qtde_alterar_produto.setText(dados_linha[2])  # Quantidade
    ui.line_valor_alterar_produto.setText(dados_linha[3])  # Valor
    ui.line_decricao_alterar_produto.setText(dados_linha[4])  # Descrição

    id_produto = ui.tabela_alterar_produto.item(row, 0).data(Qt.UserRole)
    ui.IDPRODUTO = id_produto  

    print(f"Produto selecionado: Nome: {dados_linha[0]}, ID: {ui.IDPRODUTO}")