from PyQt5.QtWidgets import (
    QMenu, QDialog, QLineEdit, QMessageBox, QCheckBox, QLabel, QPushButton, QTableWidgetItem
)
from PyQt5.QtGui import QColor, QBrush, QIcon
from PyQt5.QtCore import Qt
from database.Datalogic import GetQuantidadeProduto, GetQuantidadeProdutoEvento, UpdateStatus, UpdateStock, UpdateStockEvento, VerificarSeProdutoEhEvento
from functions.events.CustomsWidgets.renovar import Ui_Dialog

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

        ui.tabela_produto.clearSelection()  
        for coluna in range(ui.tabela_produto.columnCount()):
            item = ui.tabela_produto.item(linha, coluna)
            if item:
                item.setSelected(True)

        status_item = ui.tabela_produto.item(linha, 5) 
        if status_item:
            status = status_item.text() 
        else:
            status = ""  

        # Recupera o ID do produto
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

        # OPÇÕES GLOBAIS DENTRO DO MENU, INDEPENDENTE DO STATUS DO ITEM
        Renovar = Menu.addAction(QIcon(":/icones/redefinir.png"), "Renovar")
        Renovar.setData('Renovar')

        if status == "Ativo":
            Pausar = Menu.addAction(QIcon(":/icones/ausente.png"), "Pausar")
            Pausar.setData('Pausar')
            
        if status == "Pausado":
            Ativar = Menu.addAction(QIcon(":/icones/ativo.png"), "Circular")
            Ativar.setData("Circular")

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
        elif MenuEscolhido == "Circular":
            UiTabelaProduto.AtualizarStatus(ui, ui.tabela_produto.currentRow(), "Ativo")

    @staticmethod
    def AbrirJanelaRenovar(ui, linha):
        # Criação do diálogo utilizando a classe Ui_Dialog gerada pelo pyuic
        dialog = QDialog(ui.tabela_produto)  # Criação do QDialog
        ui_dialog = Ui_Dialog()  # Instancia a classe Ui_Dialog gerada
        ui_dialog.setupUi(dialog)  # Configura a interface do diálogo

        # Conectar a ação do botão de confirmação
        ui_dialog.finalizar_renovar.clicked.connect(lambda: UiTabelaProduto.ConfirmarRenovação(ui, dialog, linha, ui_dialog.line_renovar_quantidade.text(), ui_dialog.renovar_checkbox))

        # Exibe o diálogo
        dialog.exec_()

    @staticmethod
    def ConfirmarRenovação(ui, dialog, linha, quantidade, renovar_padrao_checkbox):
        try:
            # Verifica se ambos os campos foram preenchidos: a quantidade manual e o checkbox
            if renovar_padrao_checkbox.isChecked() and quantidade:
                # Se ambos forem preenchidos, exibe uma mensagem de erro
                QMessageBox.warning(ui.tabela_produto, "Erro", "Escolha apenas uma opção: insira a quantidade ou marque a opção de renovar com a mesma quantidade.")
                return

            # Se o checkbox estiver marcado, usar a quantidade padrão (10)
            if renovar_padrao_checkbox.isChecked():
                # Obtém o ID do produto
                id_produto = ui.IDPRODUTOQUANTIDADE

                # Verifica se o produto é de um evento
                is_evento = VerificarSeProdutoEhEvento(id_produto)

                # Obtém a quantidade atual do produto
                if is_evento:
                    quantidade = GetQuantidadeProdutoEvento(id_produto)  # Função para produtos de eventos
                else:
                    quantidade = GetQuantidadeProduto(id_produto)  # Função para produtos normais

            # Validar se a quantidade inserida é um número válido
            try:
                quantidade = int(quantidade)  # Tenta converter para inteiro
                if quantidade <= 0:
                    raise ValueError  # Se a quantidade for 0 ou negativa, gera um erro
            except ValueError:
                QMessageBox.warning(ui.tabela_produto, "Erro", "Por favor, insira uma quantidade válida.")
                return

            # Atualizar o status do produto para 'Ativo'
            UiTabelaProduto.AtualizarStatus(ui, linha, "Ativo")

            # Obtém o ID do produto
            id_produto = ui.IDPRODUTOQUANTIDADE

            # Verifica se o produto é de um evento
            is_evento = VerificarSeProdutoEhEvento(id_produto)

            # Chamar a função para atualizar o estoque no banco de dados
            if is_evento:
                UpdateStockEvento(id_produto, quantidade)  # Função para atualizar estoque de produtos de eventos
            else:
                UpdateStock(id_produto, quantidade)  # Função para atualizar estoque de produtos normais

            # Fechar o box
            dialog.accept()

            # Exibir uma mensagem de sucesso
            QMessageBox.information(ui.tabela_produto, "Sucesso", f"Estoque renovado com {quantidade} unidades.")

        except Exception as e:
        # Tratar erros (como exceções de conversão de tipo)
            QMessageBox.critical(ui.tabela_produto, "Erro", f"Ocorreu um erro: {str(e)}")

    @staticmethod
    def AtualizarStatus(ui, linha, texto):
        try:
            # Verifica se a linha é válida
            if linha < 0 or linha >= ui.tabela_produto.rowCount():
                print(f"Erro: Linha {linha} fora dos limites da tabela.")
                return
    
            # Obtém o item da coluna de status (coluna 5)
            item = ui.tabela_produto.item(linha, 5)
    
            # Se o item não existir, cria um novo
            if item is None:
                item = QTableWidgetItem()  # Cria um novo QTableWidgetItem
                ui.tabela_produto.setItem(linha, 5, item)  # Define o item na tabela
    
            # Atualiza o texto do item
            item.setText(texto)
    
            # Obtém o ID do produto
            id_produto = ui.IDPRODUTOQUANTIDADE
    
            # Atualiza o status no banco de dados
            UpdateStatus(id_produto, texto)
    
            # Aplica a estilização ao item
            UiTabelaProduto.EstilizarStatus(item, texto)
    
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")

    @staticmethod
    def EstilizarStatus(item, texto):
        if texto == "Ativo":
            item.setBackground(QColor("#90ee90"))
            item.setForeground(QBrush(QColor("#084f19")))
            item.setIcon(QIcon(":/icones/ativo.png"))
        elif texto == "Esgotado":
            item.setBackground(QColor("#ffb6c1"))
            item.setForeground(QBrush(QColor("#8b0000")))
            item.setIcon(QIcon(":/icones/esgotado.png"))
        elif texto == "Pausado":
            item.setBackground(QColor("#add8e6"))
            item.setForeground(QBrush(QColor("#00008b")))
            item.setIcon(QIcon(":/icones/ausente.png"))

    @staticmethod
    def Estilizar(ui):
        """Percorre as linhas da tabela e aplica a estilização de status."""
        for linha in range(ui.tabela_produto.rowCount()):
            item = ui.tabela_produto.item(linha, 5)  # Coluna de status
            if item:
                texto_status = item.text()
                UiTabelaProduto.EstilizarStatus(item, texto_status)