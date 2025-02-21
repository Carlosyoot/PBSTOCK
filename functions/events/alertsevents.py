from PyQt5.QtWidgets import QMessageBox, QListView
from PyQt5.QtCore import Qt, QStringListModel


class AlertManager:
    def __init__(self, ui):
        self.ui = ui

        # Criar modelo para o QListView
        self.model = QStringListModel()
        self.ui.listView.setModel(self.model)
        self.ui.listView.setSelectionMode(QListView.SingleSelection)

        # Desativar a rolagem horizontal
        self.ui.listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listView.setEnabled(True)

        # Lista de avisos com um título inicial
        self.avisos = [
            "Aviso 1: Sistema atualizado",
            "Aviso 2: Nova funcionalidade disponível",
            "Aviso 3: Ação necessária para atualização",
            "Aviso 4: Falha no servidor, verificando",
            "Aviso 5: Manutenção programada para amanhã",
            "Aviso 6: Por favor, revise suas configurações",
            "Aviso 7: Backup completo realizado",
            "Aviso 8: Lembrete de segurança"
        ]

        # Páginação
        self.itens_por_pagina = 5
        self.pagina_atual = 0
        self.atualizar_lista()

        # Conectar botões e eventos
        self.ui.antes_btn.clicked.connect(self.anterior)
        self.ui.depois_btn.clicked.connect(self.proximo)
        self.ui.listView.clicked.connect(self.item_clicado)

    def atualizar_lista(self):
        """Atualiza os itens visíveis no QListView com base na página atual"""
        inicio = self.pagina_atual * self.itens_por_pagina
        fim = min(inicio + self.itens_por_pagina, len(self.avisos))

        # Mantém o título fixo na primeira posição
        lista_exibida = self.avisos[inicio : fim]

        self.model.setStringList(lista_exibida)
        self.ui.lbl_pagina.setText(f"{self.pagina_atual + 1}")

    def anterior(self):
        """Mudar para a página anterior"""
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.atualizar_lista()

    def proximo(self):
        """Mudar para a próxima página"""
        if (self.pagina_atual + 1) * self.itens_por_pagina < len(self.avisos):
            self.pagina_atual += 1
            self.atualizar_lista()

    def add_aviso(self, mensagem):
        """Adiciona um aviso à lista no QListView"""
        self.avisos.append(mensagem)
        self.atualizar_lista()

    def item_clicado(self, index):
        """Exibe um QMessageBox com o aviso selecionado, exceto para o título"""
        item_text = self.model.data(index, Qt.DisplayRole)

        if item_text:
            QMessageBox.information(self.ui.listView, "Detalhes do Aviso", item_text)

        self.ui.listView.clearFocus()  # Evita foco no item selecionado
