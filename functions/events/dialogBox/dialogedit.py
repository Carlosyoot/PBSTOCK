from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from database.Datalogic import GetUltimoCodigo
from functions.events.dialogBox.cadastro import MyWindow
from functions.events.dialogBox.frame import MyDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

def adicionar_produtos(ui, parent):

    dialog = MyWindow()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        produtos = dialog.get_collected_data() 
        
        total_produtos = len(produtos) if produtos else 0

        atualizar_linha_produtos(ui, total_produtos)
        adicionar_produtos_na_tabela(ui, produtos)

def atualizar_linha_produtos(ui, total_produtos):

    ui.line_produtos_block.setText(f"Produtos ({total_produtos})")
    
def verificar_texto_apagado(ui):

    if not ui.line_produtos_block.text().strip(): 
        limpar_tabela(ui)

def limpar_tabela(ui):

    ui.tabela_cadastro_eventos.setRowCount(0)  

def GetUltimoCodigoDaTabela(tabela):

    if tabela.rowCount() == 0:
        return None

    ultima_linha = tabela.rowCount() - 1
    codigo = tabela.item(ultima_linha, 1).text()  
    return codigo

def adicionar_produtos_na_tabela(ui, produtos):

    tabela = ui.tabela_cadastro_eventos

    ultimo_codigo = GetUltimoCodigoDaTabela(tabela)

    proximo_codigo = GerarProximoCodigo(ultimo_codigo)

    row_count = tabela.rowCount()

    for produto in produtos:
        codigo_produto = proximo_codigo

        produto_com_codigo = produto +  (codigo_produto,)

        if not hasattr(ui, 'lista_produtos'):
            ui.lista_produtos = []
        ui.lista_produtos.append(produto_com_codigo)

        tabela.insertRow(row_count)

        item_codigo = QTableWidgetItem(codigo_produto)
        item_codigo.setTextAlignment(Qt.AlignCenter)

        item_produto = QTableWidgetItem(produto[0])  
        item_produto.setTextAlignment(Qt.AlignCenter)

        item_valor = QTableWidgetItem(str(produto[2]))  
        item_valor.setTextAlignment(Qt.AlignCenter)

        item_quantidade = QTableWidgetItem(str(produto[1]))  
        item_quantidade.setTextAlignment(Qt.AlignCenter)

        item_descricao = QTableWidgetItem(produto[3]) 
        item_descricao.setTextAlignment(Qt.AlignCenter)

        tabela.setItem(row_count, 0, item_produto)    
        tabela.setItem(row_count, 1, item_codigo)    
        tabela.setItem(row_count, 2, item_valor)     
        tabela.setItem(row_count, 3, item_quantidade)
        tabela.setItem(row_count, 4, item_descricao) 

        proximo_codigo = GerarProximoCodigo(codigo_produto)

        row_count += 1

    total_produtos = tabela.rowCount()
    ui.line_produtos_block.setText(f"Produtos ({total_produtos})")

    for i in ui.lista_produtos:
        print("produto da lista", i)

def GerarProximoCodigo(ultimo_codigo):
    if ultimo_codigo:
        numero = int(ultimo_codigo[3:])  
        proximo_numero = numero + 1
    else:
        proximo_numero = 1

    return f"EVT{proximo_numero:05d}"