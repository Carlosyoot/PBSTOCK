from PyQt5.QtCore import Qt  



def setTextAlterarColaboradores(ui):
    # Conecta o sinal de clique da tabela à função que preenche os QLineEdit
    ui.tabela_alterar_colaboradores.cellClicked.connect(lambda row, column: preencherCampos(ui, row))

def preencherCampos(ui, row):
    # Obtém os dados da linha clicada
    dados_linha = []
    for col in range(ui.tabela_alterar_colaboradores.columnCount()):
        item = ui.tabela_alterar_colaboradores.item(row, col)
        if item is not None:
            dados_linha.append(item.text())
        else:
            dados_linha.append('')

    # Preenche os QLineEdit com os dados da linha clicada
    ui.line_nome_alterar_colaboradores.setText(dados_linha[0])
    ui.line_datanasc_alterar_colaboradores.setText(dados_linha[3])
    ui.line_login_alterar_colaboradores.setText(dados_linha[1])
    ui.line_senha_alterar_colaboradores.setText(dados_linha[2])
    ui.line_cpf_alterar_colaboradores.setText(dados_linha[4])
    

    id_colaborador = ui.tabela_alterar_colaboradores.item(row, 0).data(Qt.UserRole)
    ui.IDUSERNAME = id_colaborador  

    # Exibe o ID (opcional)
    print(f"ID do colaborador selecionado: {ui.IDUSERNAME}")