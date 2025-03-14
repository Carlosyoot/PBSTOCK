from functions.events.NavEvents.navConection import conectar_eventos
from functions.events.NavEvents.buttonConection import conect_button
from functions.events.TimeEvents.Timer import HoraData, Sair
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit


class EventManager:
    @staticmethod
    def configurar_eventos(ui, parent):
        """Conecta todos os eventos da interface."""
        conectar_eventos(ui)
        conect_button(ui, parent)

        # Lista de tabelas que devem ser deselecionadas
        tabelas = [
            ui.tabela_alterar_colaboradores, ui.tabela_monitoramento,
            ui.tabela_evento, ui.tabela_vendas,ui.tabela_colaboradores,
            ui.tabela_cadastro_eventos,ui.tabela_produto, ui.tabela_cadastro,
            ui.tabela_alterar_produto, ui.tabela_evento
        ]

        # Sobrescreve o evento de clique do mouse na janela principal
        parent.mousePressEvent = lambda event: EventManager.mousePressEvent(ui, event, tabelas)
        EventManager.configurar_clique_widgets(parent, tabelas)

    @staticmethod
    def iniciar_tempo(ui, parent):
        """Inicia o timer para atualizar hora/data e verificar saída."""
        parent.tempo = QTimer(parent)
        parent.tempo.timeout.connect(lambda: HoraData(ui))
        parent.tempo.timeout.connect(lambda: Sair(ui, "23:59:59"))
        parent.tempo.start(1000)

    @staticmethod
    def mousePressEvent(ui, event, tabelas):
        """Sobrescreve o evento de clique do mouse para limpar a seleção das tabelas."""
        # Verifica se o clique foi fora das tabelas
        for tabela in tabelas:
            if not tabela.geometry().contains(event.pos()):
                tabela.clearSelection()  # Limpa a seleção da tabela

    @staticmethod
    def limpar_selecao_tabelas(tabelas):
        """Limpa a seleção de todas as tabelas."""
        for tabela in tabelas:
            tabela.clearSelection()
            
    @staticmethod
    def configurar_clique_widgets(ui, tabelas):
        """Sobrescreve o evento de clique para QLineEdit e outros widgets."""
        for widget in ui.findChildren(QLineEdit): 
            widget.mousePressEvent = lambda event, tabelas=tabelas: EventManager.limpar_selecao_tabelas(tabelas)