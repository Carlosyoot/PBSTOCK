from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from functions.events.dialogBox.frame import MyDialog
from PyQt5.QtCore import Qt


def adicionar_produtos(ui, parent):
    """
    Abre o MyDialog para adicionar produtos e atualiza a linha de produtos com o total,
    além de adicionar os produtos na tabela_cadastro_eventos.
    """
    dialog = MyDialog(parent)
    if dialog.exec_() == QDialog.Accepted:
        produtos = dialog.collected_data  
        total_produtos = len(produtos) if produtos else 0


        atualizar_linha_produtos(ui, total_produtos)

        adicionar_produtos_na_tabela(ui, produtos)

def atualizar_linha_produtos(ui, total_produtos):
    """
    Atualiza a linha de produtos com o número total de produtos.
    """
    ui.line_produtos_block.setText(f"Produtos ({total_produtos})")

def adicionar_produtos_na_tabela(ui, produtos):
    """
    Adiciona os produtos coletados na tabela_cadastro_eventos.
    """
    tabela = ui.tabela_cadastro_eventos

    row_count = tabela.rowCount()

    for index, produto in enumerate(produtos, start=1):
        tabela.insertRow(row_count)

        item_index = QTableWidgetItem(str(index))
        item_index.setTextAlignment(Qt.AlignCenter)

        item_codigo = QTableWidgetItem("")
        item_codigo.setTextAlignment(Qt.AlignCenter)

        item_produto = QTableWidgetItem(produto[0])
        item_produto.setTextAlignment(Qt.AlignCenter)

        item_valor = QTableWidgetItem(produto[2])
        item_valor.setTextAlignment(Qt.AlignCenter)

        item_quantidade = QTableWidgetItem(produto[1])
        item_quantidade.setTextAlignment(Qt.AlignCenter)

        item_descricao = QTableWidgetItem(produto[3])
        item_descricao.setTextAlignment(Qt.AlignCenter)

        tabela.setItem(row_count, 0, item_index)     
        tabela.setItem(row_count, 1, item_codigo)    
        tabela.setItem(row_count, 2, item_produto)   
        tabela.setItem(row_count, 3, item_valor)     
        tabela.setItem(row_count, 4, item_quantidade)
        tabela.setItem(row_count, 5, item_descricao) 

        row_count += 1
