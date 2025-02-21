from PyQt5.QtWidgets import QListView, QDialog, QVBoxLayout, QLabel, QPushButton, QStyledItemDelegate
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPainter


class ListViewDelegate(QStyledItemDelegate):
    """Delegate personalizado para deslocar os itens do QListView para baixo."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """Renderiza o item com um deslocamento vertical."""
        # Ajusta a posição vertical (y) para deslocar o texto para baixo
        option.rect.adjust(0, 12, 0, 0)  # Desloca o retângulo do item em 12 pixels para baixo

        # Renderiza o item normalmente
        super().paint(painter, option, index)


class DetalhesAvisoDialog(QDialog):
    """Janela personalizada para exibir detalhes do aviso."""
    def __init__(self, aviso, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalhes do Aviso")
        self.setFixedSize(300, 150)  # Tamanho fixo da janela
        
        self.setStyleSheet("background-color: white; color: black;")

        # Layout principal
        layout = QVBoxLayout()

        # Label para exibir o texto do aviso
        self.label_aviso = QLabel(aviso)
        self.label_aviso.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_aviso)

        # Botão "OK" para fechar a janela
        self.botao_ok = QPushButton("OK")
        self.botao_ok.clicked.connect(self.accept)  # Fecha a janela ao clicar
        layout.addWidget(self.botao_ok)

        # Define o layout da janela
        self.setLayout(layout)


class AlertManager:
    def __init__(self, ui):
        self.ui = ui

        # Criar modelo para o QListView
        self.model = QStringListModel()
        self.ui.listView.setModel(self.model)
        self.ui.listView.setSelectionMode(QListView.SingleSelection)

        # Desativar o foco no QListView para remover a borda pontilhada
        self.ui.listView.setFocusPolicy(Qt.NoFocus)

        # Aplicar o delegate personalizado
        self.delegate = ListViewDelegate(self.ui.listView)
        self.ui.listView.setItemDelegate(self.delegate)

        # Desativar a rolagem horizontal
        self.ui.listView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listView.setEnabled(True)

        # Lista de avisos com um título inicial
        self.avisos = [
            "⚠️ Aviso 1: Sistema atualizado",
            "✨ Aviso 2: Nova funcionalidade disponível",
            "🔧 Aviso 3: Ação necessária para atualização",
            "🚨 Aviso 4: Falha no servidor, verificando",
            "🛠️ Aviso 5: Manutenção programada para amanhã",
            "⚙️ Aviso 6: Por favor, revise suas configurações",
            "✅ Aviso 7: Backup completo realizado",
            "🔒 Aviso 8: Lembrete de segurança"
        ]

        # Paginação
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
        lista_exibida = self.avisos[inicio:fim]

        self.model.setStringList(lista_exibida)
        self.ui.listView.setTextElideMode(Qt.ElideNone)  # Evita corte de texto

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
        """Exibe um QDialog personalizado com o aviso selecionado."""
        item_text = self.model.data(index, Qt.DisplayRole)

        if item_text:
            # Cria e exibe o QDialog personalizado
            dialog = DetalhesAvisoDialog(item_text, self.ui.listView)
            dialog.exec_()  # Exibe o diálogo de forma modal

            # Limpa a seleção após fechar o QDialog
            self.ui.listView.clearSelection()
            self.ui.listView.clearFocus()  # Evita foco no item selecionado