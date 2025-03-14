from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt
from database.Datalogic import DataGetAllColaboradoresNomes

def AtualizaCompleterSearchColaboradores(ui):
    """
    Configura o QCompleter com base nos nomes dos colaboradores.
    """
    try:
        # Obtém os nomes dos colaboradores
        nomes_colaboradores = DataGetAllColaboradoresNomes()

        # Configura o QCompleter com os nomes
        completer = QCompleter(nomes_colaboradores)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)  # Permite buscar por qualquer parte do texto

        # Aplica o QCompleter aos campos de busca
        ui.line_search_bar_buscar_colaboradores.setCompleter(completer)
        ui.line_search_bar_colaboradores.setCompleter(completer)
        ui.line_colaborador_vendedor.setCompleter(completer)

        # Conecta a mudança de texto para verificar quando o campo de busca está vazio
        ui.line_search_bar_colaboradores.textChanged.connect(lambda text: mostrar_todos_os_colaboradores(text, completer, ui))
        ui.line_search_bar_buscar_colaboradores.textChanged.connect(lambda text: mostrar_todos_os_colaboradores(text, completer, ui))
    
    except Exception as e:
        print(f"Erro ao configurar completer: {e}")

def mostrar_todos_os_colaboradores(text, completer, ui):
    """
    Função que mostra todos os colaboradores quando o texto da busca está vazio ou apenas com espaços.
    """
    try:
        # Se o texto estiver vazio ou apenas com espaços, recarrega todos os colaboradores
        if not text.strip():  # Se o texto estiver vazio ou contiver apenas espaços
            nomes_colaboradores = DataGetAllColaboradoresNomes()
            completer.model().setStringList(nomes_colaboradores)
            completer.complete()  # Força o completer a atualizar as sugestões
        else:
            # Caso contrário, o QCompleter continua funcionando normalmente com o filtro
            completer.setFilterMode(Qt.MatchContains)
    except Exception as e:
        print(f"Erro ao atualizar lista de colaboradores no completer: {e}")

def filtrar_tabela_colaboradores(ui, alter):
    """
    Filtra a tabela de colaboradores com base no texto digitado no campo de busca.
    """
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

        # Percorre as linhas da tabela e verifica se o texto de busca está presente
        for row in range(row_count):
            match = False
            for col in range(col_count):
                # Acessa o item da célula no contexto correto
                item = ui.tabela_colaboradores.item(row, col) if alter == 1 else ui.tabela_alterar_colaboradores.item(row, col)
                if item and texto_busca in item.text().lower():
                    match = True
                    break

            # Mostra ou oculta a linha com base no resultado da busca
            if alter == 1:
                ui.tabela_colaboradores.setRowHidden(row, not match)
            else:
                ui.tabela_alterar_colaboradores.setRowHidden(row, not match)

    except Exception as e:
        print(f"Erro ao filtrar tabela de colaboradores: {e}")

def reexibir_tabela_colaboradores(ui, tabela):
    """
    Reexibe todas as linhas da tabela de colaboradores.

    :param ui: Interface do usuário.
    :param tabela: Número da tabela (1 para tabela_colaboradores, 2 para tabela_alterar_colaboradores).
    """
    try:
        if tabela == 1:
            tabela_widget = ui.tabela_colaboradores
        elif tabela == 2:
            tabela_widget = ui.tabela_alterar_colaboradores
        else:
            return

        row_count = tabela_widget.rowCount()
        for row in range(row_count):
            tabela_widget.setRowHidden(row, False)  # Mostra todas as linhas
    except Exception as e:
        print(f"Erro ao reexibir tabela de colaboradores: {e}")
