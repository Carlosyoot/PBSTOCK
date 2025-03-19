from PyQt5.QtWidgets import QCompleter
from database.Datalogic import getevento
from functions.events.searchs.CustomSugestion import CustomCompleterNome

def AtualizaCompleterSearchEventos(ui):
    """
    Configura o QCompleter para o campo de busca de eventos.
    """
    try:
        # Define uma função que retorna a lista de eventos formatados
        def get_eventos_formatados():
            eventos = getevento()
            return eventos

        # Cria o autocompleter com a função que retorna a lista de eventos formatados
        CustomComptEvento = CustomCompleterNome(get_eventos_formatados)

        # Define o autocompleter para o campo de busca de eventos
        ui.line_search_Bar_evento.setCompleter(CustomComptEvento)

        # Conecta os sinais para filtrar a tabela de eventos
        ui.line_search_Bar_evento.returnPressed.connect(
            lambda: filtrar_tabela_eventos(ui)
        )

        ui.line_search_Bar_evento.textChanged.connect(
            lambda: reexibir_tabela_eventos(ui) if ui.line_search_Bar_evento.text().strip() == "" else filtrar_tabela_eventos(ui)
        )

    except Exception as e:
        print(f"Erro ao configurar completer para eventos: {e}")


def filtrar_tabela_eventos(ui):
    """
    Filtra a tabela de eventos com base no texto digitado no campo de busca.
    """
    try:
        texto_busca = ui.line_search_Bar_evento.text().strip().lower()
        tabela = ui.tabela_evento

        print(f"Texto de busca: {texto_busca}")

        # Verifica se o texto de busca está no formato "nome - data"
        if " - " in texto_busca:
            nome_busca, data_busca = texto_busca.rsplit(" - ", 1)
        else:
            # Se não estiver no formato "nome - data", assume que é apenas o nome
            nome_busca = texto_busca
            data_busca = ""

        # Percorre as linhas da tabela e verifica se o texto de busca está presente
        row_count = tabela.rowCount()

        for row in range(row_count):
            # Obtém o nome e a data do evento da linha atual
            data = tabela.item(row, 1).text().lower()  # Coluna 1: Data do Evento

            # Verifica se o nome e a data correspondem ao texto de busca
            match_data = data_busca in data if data_busca else True

            # Mostra ou oculta a linha com base no resultado da busca
            match =  match_data
            tabela.setRowHidden(row, not match)
            print(f"Linha {row}: {'Mostrar' if match else 'Ocultar'} - Nome: {data}")

    except Exception as e:
        print(f"Erro ao filtrar tabela de eventos: {e}")


def reexibir_tabela_eventos(ui):
    """
    Reexibe todas as linhas da tabela de eventos quando o campo de busca está vazio.
    """
    try:
        # Reexibe todas as linhas da tabela de eventos
        row_count = ui.tabela_evento.rowCount()
        for row in range(row_count):
            ui.tabela_evento.setRowHidden(row, False)  # Mostra todas as linhas

    except Exception as e:
        print(f"Erro ao reexibir tabela de eventos: {e}")