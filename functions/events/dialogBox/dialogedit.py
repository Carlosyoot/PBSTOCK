from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from database.Datalogic import GetUltimoCodigo
from functions.events.dialogBox.cadastro import MyWindow
from functions.events.dialogBox.frame import MyDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

def adicionar_produtos(ui, parent):
    """
    Abre o MyDialog para adicionar produtos e atualiza a linha de produtos com o total,
    além de adicionar os produtos na tabela_cadastro_eventos.
    """
    dialog = MyWindow()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        produtos = dialog.get_collected_data()  # Obtém os dados coletados
        
        total_produtos = len(produtos) if produtos else 0

        atualizar_linha_produtos(ui, total_produtos)
        adicionar_produtos_na_tabela(ui, produtos)

def atualizar_linha_produtos(ui, total_produtos):
    """
    Atualiza a linha de produtos com o número total de produtos.
    """
    ui.line_produtos_block.setText(f"Produtos ({total_produtos})")
    
def verificar_texto_apagado(ui):
    """
    Verifica se o texto do ui.line_produtos_block está vazio e, se estiver, limpa a tabela.
    """
    if not ui.line_produtos_block.text().strip():  # Verifica se o texto está vazio ou contém apenas espaços
        limpar_tabela(ui)

def limpar_tabela(ui):
    """
    Limpa a tabela_cadastro_eventos.
    """
    ui.tabela_cadastro_eventos.setRowCount(0)  # Remove todas as linhas da tabela

def GetUltimoCodigoDaTabela(tabela):
    """
    Obtém o último código presente na tabela.
    Retorna None se a tabela estiver vazia.
    """
    if tabela.rowCount() == 0:
        return None

    # Obtém o código da última linha da tabela
    ultima_linha = tabela.rowCount() - 1
    codigo = tabela.item(ultima_linha, 1).text()  # Coluna 1 é a coluna de código
    return codigo

def adicionar_produtos_na_tabela(ui, produtos):
    """
    Adiciona os produtos coletados na tabela_cadastro_eventos e na lista de produtos.
    """
    tabela = ui.tabela_cadastro_eventos

    # Obtém o último código da tabela
    ultimo_codigo = GetUltimoCodigoDaTabela(tabela)

    # Gera o próximo código
    proximo_codigo = GerarProximoCodigo(ultimo_codigo)

    row_count = tabela.rowCount()

    # Itera sobre os produtos e os adiciona na tabela e na lista
    for produto in produtos:
        # Gera o código para o produto atual
        codigo_produto = proximo_codigo

        # Adiciona o código ao produto (como primeiro elemento da tupla)
        produto_com_codigo = produto +  (codigo_produto,)

        # Adiciona o produto com código à lista de produtos
        if not hasattr(ui, 'lista_produtos'):
            ui.lista_produtos = []
        ui.lista_produtos.append(produto_com_codigo)

        # Insere o produto na tabela
        tabela.insertRow(row_count)

        # Cria os itens da tabela
        item_codigo = QTableWidgetItem(codigo_produto)
        item_codigo.setTextAlignment(Qt.AlignCenter)

        item_produto = QTableWidgetItem(produto[0])  # Nome do produto
        item_produto.setTextAlignment(Qt.AlignCenter)

        item_valor = QTableWidgetItem(str(produto[2]))  # Valor unitário
        item_valor.setTextAlignment(Qt.AlignCenter)

        item_quantidade = QTableWidgetItem(str(produto[1]))  # Quantidade
        item_quantidade.setTextAlignment(Qt.AlignCenter)

        item_descricao = QTableWidgetItem(produto[3])  # Descrição
        item_descricao.setTextAlignment(Qt.AlignCenter)

        # Insere os itens na tabela
        tabela.setItem(row_count, 0, item_produto)    
        tabela.setItem(row_count, 1, item_codigo)    
        tabela.setItem(row_count, 2, item_valor)     
        tabela.setItem(row_count, 3, item_quantidade)
        tabela.setItem(row_count, 4, item_descricao) 

        # Atualiza o próximo código para o próximo produto
        proximo_codigo = GerarProximoCodigo(codigo_produto)

        row_count += 1

    # Atualiza o ui.line_produtos_block com o número total de produtos na tabela
    total_produtos = tabela.rowCount()
    ui.line_produtos_block.setText(f"Produtos ({total_produtos})")

    # Exibe os produtos na lista (apenas para debug)
    for i in ui.lista_produtos:
        print("produto da lista", i)

def GerarProximoCodigo(ultimo_codigo):
    if ultimo_codigo:
        # Extrai o número do último código (por exemplo, "EVT00005" -> 5)
        numero = int(ultimo_codigo[3:])  # Remove "EVT" e converte o restante para inteiro
        proximo_numero = numero + 1
    else:
        # Se não houver último código, começa com 1
        proximo_numero = 1

    # Formata o próximo código (por exemplo, "EVT00006")
    return f"EVT{proximo_numero:05d}"