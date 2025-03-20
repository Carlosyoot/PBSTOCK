from PyQt5.QtWidgets import QCompleter, QMessageBox
from PyQt5.QtCore import Qt
from database.Datalogic import ExcluirEvento, getevento

def AtualizaCompleterSearchEventos(ui):

    try:
        eventos = getevento()

        CustomComptEvento = QCompleter(eventos, ui.line_search_Bar_evento)

        CustomComptEvento.setCaseSensitivity(False)
        CustomComptEvento.setFilterMode(Qt.MatchContains)

        ui.line_search_Bar_evento.setCompleter(CustomComptEvento)

        ui.line_search_Bar_evento.returnPressed.connect(
            lambda: filtrar_tabela_eventos(ui)
        )

        ui.line_search_Bar_evento.textChanged.connect(
            lambda: reexibir_tabela_eventos(ui) if ui.line_search_Bar_evento.text().strip() == "" else filtrar_tabela_eventos(ui)
        )

        ui.tabela_evento.cellClicked.connect(lambda row, col: capturar_id_evento(ui, row))


    except Exception as e:
        print(f"Erro ao configurar completer para eventos: {e}")

def capturar_id_evento(ui, row):

    try:
        item = ui.tabela_evento.item(row, 0)

        if item:
            id_evento = item.text()
            print(f"ID do evento clicado: {id_evento}")

          
            ui.id_evento_selecionado = id_evento

    except Exception as e:
        print(f"Erro ao capturar id_evento: {e}")

def excluir_evento_clicado(ui,parent):

    try:
        if hasattr(ui, 'id_evento_selecionado') and ui.id_evento_selecionado:
            id_evento = ui.id_evento_selecionado

            confirmacao = QMessageBox.question(
                parent, 
                "Confirmar Exclusão", 
                f"Tem certeza que deseja excluir o evento com ID {id_evento}?",  
                QMessageBox.Yes | QMessageBox.No  
            )

            if confirmacao == QMessageBox.Yes:
                if ExcluirEvento(id_evento):
                    print(f"Evento com ID {id_evento} excluído com sucesso.")
                    AtualizaCompleterSearchEventos(ui)
                    
                    
                else:
                    print(f"Erro ao excluir evento com ID {id_evento}.")
        else:
            QMessageBox.warning(parent, "Aviso", "Nenhum evento selecionado.")

    except Exception as e:
        print(f"Erro ao excluir evento: {e}")


def filtrar_tabela_eventos(ui):

    try:
        texto_busca = ui.line_search_Bar_evento.text().strip().lower()
        tabela = ui.tabela_evento

        if " - " in texto_busca:
            nome_busca, data_busca = texto_busca.rsplit(" - ", 1)
        else:
            nome_busca = texto_busca
            data_busca = ""

        row_count = tabela.rowCount()

        for row in range(row_count):
            data = tabela.item(row, 1).text().lower()

            match_data = data_busca in data if data_busca else True

            match = match_data
            tabela.setRowHidden(row, not match)

    except Exception as e:
        print(f"Erro ao filtrar tabela de eventos: {e}")

def reexibir_tabela_eventos(ui):

    try:
        row_count = ui.tabela_evento.rowCount()
        for row in range(row_count):
            ui.tabela_evento.setRowHidden(row, False)

    except Exception as e:
        print(f"Erro ao reexibir tabela de eventos: {e}")