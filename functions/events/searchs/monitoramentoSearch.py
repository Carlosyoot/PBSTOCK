from PyQt5.QtWidgets import QCompleter, QTableWidgetItem
from database.Datalogic import DataGetAllColaboradoresNomes
from PyQt5.QtCore import Qt

def AtualizaCompleterSearchMonitoramento(ui):

    try:
        nomes_colaboradores = DataGetAllColaboradoresNomes()

        if not all(isinstance(nome, str) for nome in nomes_colaboradores):
            nomes_colaboradores = [str(nome) for nome in nomes_colaboradores]

        CustomComptMonitoramento = QCompleter(nomes_colaboradores)
        CustomComptMonitoramento.setCaseSensitivity(False) 
        CustomComptMonitoramento.setFilterMode(Qt.MatchContains) 

        ui.line_search_bar_monitoramentoto.setCompleter(CustomComptMonitoramento)

        ui.line_search_bar_monitoramentoto.textChanged.connect(lambda: filtrar_tabela_monitoramento(ui))

    except Exception as e:
        print(f"Erro ao configurar completer para monitoramento: {e}")

def filtrar_tabela_monitoramento(ui):
    try:
        texto_busca = ui.line_search_bar_monitoramentoto.text().strip().lower()
        tabela = ui.tabela_monitoramento

        if not texto_busca:
            reexibir_tabela_monitoramento(ui)
            return

        row_count = tabela.rowCount()

        for row in range(row_count):
            vendedor_item = tabela.item(row, 0) 

            if vendedor_item:
                vendedor = vendedor_item.text().lower()
                match = texto_busca in vendedor
            else:
                match = False  

            tabela.setRowHidden(row, not match)

    except Exception as e:
        print(f"Erro ao filtrar tabela de monitoramento: {e}")

def reexibir_tabela_monitoramento(ui):
 
    try:
        tabela = ui.tabela_monitoramento
        row_count = tabela.rowCount()

        for row in range(row_count):
            tabela.setRowHidden(row, False)  

    except Exception as e:
        print(f"Erro ao reexibir tabela de monitoramento: {e}")