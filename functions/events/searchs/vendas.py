from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt
from database.Datalogic import getVendas  


def AtualizaCompleterSearchVendas(ui):

    try:
       
        vendas_lista = getVendas() 

        completer = QCompleter(vendas_lista)
        completer.setCaseSensitivity(Qt.CaseInsensitive) 
        completer.setFilterMode(Qt.MatchContains)  

    
        ui.line_search_bar_vendas.setCompleter(completer)

      
        ui.line_search_bar_vendas.editingFinished.connect(lambda: filtrar_tabela_vendas(ui))

        ui.line_search_bar_vendas.textChanged.connect(
            lambda: reexibir_tabela_vendas(ui) if ui.line_search_bar_vendas.text().strip() == "" else None
        )

    except Exception as e:
        print(f"Erro ao configurar completer para vendas: {e}")


def filtrar_tabela_vendas(ui):
    try:
        texto_busca = ui.line_search_bar_vendas.text().strip().lower()
        tabela = ui.tabela_vendas

        print(f"Texto de busca: {texto_busca}")

        row_count = tabela.rowCount()

        for row in range(row_count):
            nome = tabela.item(row, 0).text().strip().lower()

            match = texto_busca in nome if texto_busca else True

            tabela.setRowHidden(row, not match)

    except Exception as e:
        print(f"Erro ao filtrar tabela de vendas: {e}")


def reexibir_tabela_vendas(ui):

    try:
        row_count = ui.tabela_vendas.rowCount()
        for row in range(row_count):
            ui.tabela_vendas.setRowHidden(row, False)  

    except Exception as e:
        print(f"Erro ao reexibir tabela de vendas: {e}")
