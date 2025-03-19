from PyQt5.QtWidgets import QCompleter
from database.Datalogic import getVendas
from functions.events.searchs.CustomSugestion import CustomCompleterCód, CustomCompleterNome

def AtualizaCompleterSearchVendas(ui):
    """
    Configura o QCompleter para o campo de busca de vendas.
    """
    try:
        # Passa a função getVendas como callable para o CustomCompleterNome
        CustomComptNome = CustomCompleterNome(getVendas)

        # Define o autocompleter para o campo de busca de vendas
        ui.line_search_bar_vendas.setCompleter(CustomComptNome)

        # Conecta os sinais para filtrar a tabela de vendas
        ui.line_search_bar_vendas.returnPressed.connect(
            lambda: filtrar_tabela_vendas(ui)
        )

        ui.line_search_bar_vendas.textChanged.connect(
            lambda: reexibir_tabela_vendas(ui) if ui.line_search_bar_vendas.text().strip() == "" else None
        )

    except Exception as e:
        print(f"Erro ao configurar completer para vendas: {e}")


def filtrar_tabela_vendas(ui):
    """
    Filtra a tabela de vendas com base no texto digitado no campo de busca.
    """
    try:
        texto_busca = ui.line_search_bar_vendas.text().strip().lower()
        tabela = ui.tabela_vendas

        print(f"Texto de busca: {texto_busca}")

        # Percorre as linhas da tabela e verifica se o texto de busca está presente
        row_count = tabela.rowCount()

        for row in range(row_count):
            # Obtém o nome do produto da linha atual
            nome = tabela.item(row, 0).text().lower()  # Coluna 0: Nome do Produto

            # Verifica se o texto de busca está presente no nome do produto
            match = texto_busca in nome if texto_busca else True

            # Mostra ou oculta a linha com base no resultado da busca
            tabela.setRowHidden(row, not match)
            print(f"Linha {row}: {'Mostrar' if match else 'Ocultar'} - Nome: {nome}")

    except Exception as e:
        print(f"Erro ao filtrar tabela de vendas: {e}")


def reexibir_tabela_vendas(ui):
    """
    Reexibe todas as linhas da tabela de vendas quando o campo de busca está vazio.
    """
    try:
        # Reexibe todas as linhas da tabela de vendas
        row_count = ui.tabela_vendas.rowCount()
        for row in range(row_count):
            ui.tabela_vendas.setRowHidden(row, False)  # Mostra todas as linhas

    except Exception as e:
        print(f"Erro ao reexibir tabela de vendas: {e}")