from PyQt5.QtWidgets import QCompleter, QTableWidgetItem
from database.Datalogic import DataGetAllColaboradoresNomes
from PyQt5.QtCore import Qt

def AtualizaCompleterSearchMonitoramento(ui):
    """
    Configura o QCompleter para o campo de busca de monitoramento.
    """
    try:
        # Obtém a lista de nomes de colaboradores
        nomes_colaboradores = DataGetAllColaboradoresNomes()

        # Verifica se é uma lista simples
        if not all(isinstance(nome, str) for nome in nomes_colaboradores):
            nomes_colaboradores = [str(nome) for nome in nomes_colaboradores]  # Converte para string se necessário

        # Cria o autocompleter com a lista corrigida
        CustomComptMonitoramento = QCompleter(nomes_colaboradores)
        CustomComptMonitoramento.setCaseSensitivity(False)  # Ignora maiúsculas/minúsculas
        CustomComptMonitoramento.setFilterMode(Qt.MatchContains)  # Permite pesquisa parcial

        # Define o autocompleter para o campo de busca
        ui.line_search_bar_monitoramentoto.setCompleter(CustomComptMonitoramento)

    except Exception as e:
        print(f"Erro ao configurar completer para monitoramento: {e}")


def filtrar_tabela_monitoramento(ui):
    """
    Filtra a tabela de monitoramento com base no nome do vendedor digitado no campo de busca.
    """
    try:
        texto_busca = ui.line_search_bar_monitoramento.text().strip().lower()
        tabela = ui.tabela_monitoramento

        print(f"Texto de busca: {texto_busca}")

        # Percorre as linhas da tabela e verifica se o texto de busca está presente na coluna do vendedor
        row_count = tabela.rowCount()

        for row in range(row_count):
            # Obtém o nome do vendedor da linha atual
            vendedor = tabela.item(row, 0).text().lower()  # Coluna 0: Vendedor

            # Verifica se o texto de busca está presente no nome do vendedor
            match = texto_busca in vendedor if texto_busca else True

            # Mostra ou oculta a linha com base no resultado da busca
            tabela.setRowHidden(row, not match)
            print(f"Linha {row}: {'Mostrar' if match else 'Ocultar'} - Vendedor: {vendedor}")

    except Exception as e:
        print(f"Erro ao filtrar tabela de monitoramento: {e}")


def reexibir_tabela_monitoramento(ui):
    """
    Reexibe todas as linhas da tabela de monitoramento quando o campo de busca está vazio.
    """
    try:
        # Reexibe todas as linhas da tabela de monitoramento
        row_count = ui.tabela_monitoramento.rowCount()
        for row in range(row_count):
            ui.tabela_monitoramento.setRowHidden(row, False)  # Mostra todas as linhas

    except Exception as e:
        print(f"Erro ao reexibir tabela de monitoramento: {e}")