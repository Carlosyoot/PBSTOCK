from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt
from database.Datalogic import DataGetAllColaboradoresNomes

def AtualizaCompleterSearchColaboradores(ui):

    try:
        nomes_colaboradores = DataGetAllColaboradoresNomes()

        completer = QCompleter(nomes_colaboradores)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains) 

        ui.line_search_bar_buscar_colaboradores.setCompleter(completer)
        ui.line_search_bar_colaboradores.setCompleter(completer)
        ui.line_colaborador_vendedor.setCompleter(completer)


    
    except Exception as e:
        print(f"Erro ao configurar completer: {e}")


def filtrar_tabela_colaboradores(ui, alter):
 
    try:
        if alter == 1:
            texto_busca = ui.line_search_bar_colaboradores.text().strip().lower()
            row_count = ui.tabela_colaboradores.rowCount()
            col_count = ui.tabela_colaboradores.columnCount()
        elif alter == 2:
            texto_busca = ui.line_search_bar_buscar_colaboradores.text().strip().lower()
            row_count = ui.tabela_alterar_colaboradores.rowCount()
            col_count = ui.tabela_alterar_colaboradores.columnCount()
        else:
            return

        for row in range(row_count):
            match = False
            for col in range(col_count):
                item = ui.tabela_colaboradores.item(row, col) if alter == 1 else ui.tabela_alterar_colaboradores.item(row, col)
                if item and texto_busca in item.text().lower():
                    match = True
                    break

            if alter == 1:
                ui.tabela_colaboradores.setRowHidden(row, not match)
            else:
                ui.tabela_alterar_colaboradores.setRowHidden(row, not match)

    except Exception as e:
        print(f"Erro ao filtrar tabela de colaboradores: {e}")

def reexibir_tabela_colaboradores(ui, tabela):
   
    try:
        if tabela == 1:
            tabela_widget = ui.tabela_colaboradores
        elif tabela == 2:
            tabela_widget = ui.tabela_alterar_colaboradores
        else:
            return

        row_count = tabela_widget.rowCount()
        for row in range(row_count):
            tabela_widget.setRowHidden(row, False) 
    except Exception as e:
        print(f"Erro ao reexibir tabela de colaboradores: {e}")
