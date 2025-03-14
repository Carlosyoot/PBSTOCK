from PyQt5.QtWidgets import (
    QMenu, QDialog, QLineEdit, QMessageBox, QCheckBox, QLabel, QPushButton
)
from PyQt5.QtGui import QColor, QBrush, QIcon
from PyQt5.QtCore import Qt
from database.Datalogic import GetQuantidadeProduto, UpdateStatus



class UiTabelaProduto:
    
    @staticmethod
    def setup_table(ui):
        """Configurações iniciais da tabela."""

        ui.tabela_produto.setContextMenuPolicy(Qt.CustomContextMenu)
        ui.tabela_produto.customContextMenuRequested.connect(lambda pos: UiTabelaProduto.MostrarMenu(ui, pos))
        ui.tabela_produto.setFocusPolicy(Qt.NoFocus)
        
        selection_model = ui.tabela_produto.selectionModel()
        selection_model.selectionChanged.connect(lambda: UiTabelaProduto.block_column_selection(ui))
        
        
    @staticmethod
    def block_column_selection(ui):
        """Impede a seleção da coluna 5, mesmo em seleções múltiplas."""
        for index in ui.tabela_produto.selectedIndexes():
            if index.column() == 5:  # Coluna que não deve ser selecionável
                ui.tabela_produto.selectionModel().select(index, ui.tabela_produto.selectionModel().Deselect)

    @staticmethod
    def MostrarMenu(ui, posição):
        linha = ui.tabela_produto.rowAt(posição.y())

        if linha < 0 or linha >= ui.tabela_produto.rowCount():
            return

        # Seleciona a linha inteira ao clicar com o botão direito
        ui.tabela_produto.clearSelection()  
        for coluna in range(ui.tabela_produto.columnCount()):
            item = ui.tabela_produto.item(linha, coluna)
            if item:
                item.setSelected(True)

       
        id_produto = ui.tabela_produto.item(linha, 0).data(Qt.UserRole)  #
        ui.IDPRODUTOQUANTIDADE = id_produto  

        Menu = QMenu(ui.tabela_produto)

        Menu.setStyleSheet("""
            QMenu {
                background-color: #f9f9f9;  /* Cor de fundo do menu */
                border: 1px solid #ccc;    /* Borda do menu */
            }
            QMenu::item {
                background-color: #f9f9f9;  /* Cor de fundo do menu */
                padding: 5px 10px;
            }
            QMenu::item:selected {
                background-color: rgb(239, 239, 239);  /* Cor de fundo do item ao passar o mouse (hover) */
                color: black;  /* Cor do texto quando o mouse passa sobre o item */
            }
        """)

        # OPÇÕES GLOBAIS DENTRO DE MENU, INDEPENDENTE DO STATUS DO ITEM
        Renovar = Menu.addAction(QIcon("renovar.png"), "Renovar")
        Renovar.setData('Renovar')
        Pausar = Menu.addAction(QIcon("ausente.png"), "Pausar")
        Pausar.setData('Pausar')

        Show = Menu.exec_(ui.tabela_produto.viewport().mapToGlobal(posição))

        if Show:
            MenuEscolhido = Show.data()
            UiTabelaProduto.FecharMenu(ui, Menu, MenuEscolhido)



    @staticmethod
    def FecharMenu(ui, Menu, MenuEscolhido):

        Menu.close()

        # Agora verifica qual ação foi selecionada com base no identificador
        if MenuEscolhido == "Renovar":
            UiTabelaProduto.AbrirJanelaRenovar(ui, ui.tabela_produto.currentRow())
        elif MenuEscolhido == "Pausar":
            UiTabelaProduto.AtualizarStatus(ui, ui.tabela_produto.currentRow(), "Pausado")
        elif MenuEscolhido == "pausado":
            pass  # Nenhuma ação ou comportamento adicional
        
    @staticmethod
    def AbrirJanelaRenovar(ui, linha):
        # Criação do diálogo
        Box = QDialog(ui.tabela_produto)
        Box.setWindowTitle("Renovar Estoque")
        Box.resize(300, 150)

        # Adicionando o label
        label = QLabel("Digite a quantidade que deseja renovar:", Box)
        label.move(20, 10)

        # Campo para o usuário inserir a quantidade
        quantity_input = QLineEdit(Box)
        quantity_input.setFixedSize(180, 25)
        quantity_input.move(20, 40)

        # Checkbox para renovar com a mesma quantidade
        RenovarPadrão = QCheckBox("Renovar com mesma quantidade", Box)
        RenovarPadrão.move(20, 80)

        # Botão de confirmação
        confirm_button = QPushButton("OK", Box)
        confirm_button.setFixedSize(80, 25)
        confirm_button.move(205, 115)
        

        # Ação do botão confirm_button
        confirm_button.clicked.connect(lambda: UiTabelaProduto.ConfirmarRenovação(ui, Box, linha, quantity_input.text(), RenovarPadrão))

        # Exibe o diálogo
        Box.exec_()

    @staticmethod
    def ConfirmarRenovação(ui, box, linha, quantidade, RenovarPadrão):
        try:
            # Se o checkbox estiver marcado, usar a quantidade padrão (10)
            if RenovarPadrão.isChecked():
                quantidade = GetQuantidadeProduto(ui.IDPRODUTOQUANTIDADE)

            # Verificar se a quantidade é válida
            if not quantidade or int(quantidade) <= 0:
                QMessageBox.warning(ui.tabela_produto, "Erro", "Por favor, insira uma quantidade válida.")
                return

            # Atualizar o status do produto para 'Ativo'
            UiTabelaProduto.AtualizarStatus(ui, linha, "Ativo")

            # Fechar o box
            box.accept()

            # Exibir uma mensagem de sucesso
            QMessageBox.information(ui.tabela_produto, "Sucesso", f"Estoque renovado com {quantidade} unidades.")

        except Exception as e:
            # Tratar erros (como exceções de conversão de tipo)
            QMessageBox.critical(ui.tabela_produto, "Erro", f"Ocorreu um erro: {str(e)}")
            
            
    @staticmethod
    def AtualizarStatus(ui, linha, texto):
        
        if linha >= ui.tabela_produto.rowCount():
            return
        
        item = ui.tabela_produto.item(linha, 5)
        item.setText(texto)
        ID=ui.IDPRODUTOQUANTIDADE
        UpdateStatus(ID, texto)
        UiTabelaProduto.EstilizarStatus(item, texto)
        
    @staticmethod
    def EstilizarStatus(item, texto):
        if texto == "Ativo":
            item.setBackground(QColor("#90ee90"))
            item.setForeground(QBrush(QColor("#084f19")))
            item.setIcon(QIcon("ativo.png"))
        elif texto == "Esgotado":
            item.setBackground(QColor("#ffb6c1"))
            item.setForeground(QBrush(QColor("#8b0000")))
            item.setIcon(QIcon("esgotado.png"))
        elif texto == "Pausado":
            item.setBackground(QColor("#add8e6"))
            item.setForeground(QBrush(QColor("#00008b")))
            item.setIcon(QIcon("ausente.png"))
            
    @staticmethod
    def Estilizar(ui):
        """Percorre as linhas da tabela e aplica a estilização de status."""
        for linha in range(ui.tabela_produto.rowCount()):
            item = ui.tabela_produto.item(linha, 5)  # Coluna de status
            if item:
                texto_status = item.text()
                UiTabelaProduto.EstilizarStatus(item, texto_status)

            
    