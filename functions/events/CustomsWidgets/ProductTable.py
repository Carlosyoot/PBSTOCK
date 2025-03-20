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
        ui.tabela_produto.setContextMenuPolicy(Qt.CustomContextMenu)
        ui.tabela_produto.customContextMenuRequested.connect(lambda pos: UiTabelaProduto.MostrarMenu(ui, pos))
        ui.tabela_produto.setFocusPolicy(Qt.NoFocus)
        
        selection_model = ui.tabela_produto.selectionModel()
        selection_model.selectionChanged.connect(lambda: UiTabelaProduto.block_column_selection(ui))
        
    @staticmethod
    def block_column_selection(ui):
        for index in ui.tabela_produto.selectedIndexes():
            if index.column() == 5:  
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

        if MenuEscolhido == "Renovar":
            UiTabelaProduto.AbrirJanelaRenovar(ui, ui.tabela_produto.currentRow())
        elif MenuEscolhido == "Pausar":
            UiTabelaProduto.AtualizarStatus(ui, ui.tabela_produto.currentRow(), "Pausado")
        elif MenuEscolhido == "Circular":
            UiTabelaProduto.AtualizarStatus(ui, ui.tabela_produto.currentRow(), "Ativo")

    @staticmethod
    def AbrirJanelaRenovar(ui, linha):
        dialog = QDialog(ui.tabela_produto)  
        ui_dialog = Ui_Dialog()  
        ui_dialog.setupUi(dialog)  

        ui_dialog.finalizar_renovar.clicked.connect(lambda: UiTabelaProduto.ConfirmarRenovação(ui, dialog, linha, ui_dialog.line_renovar_quantidade.text(), ui_dialog.renovar_checkbox))

        dialog.exec_()

    @staticmethod
    def ConfirmarRenovação(ui, dialog, linha, quantidade, renovar_padrao_checkbox):
        try:
            if renovar_padrao_checkbox.isChecked() and quantidade:
                QMessageBox.warning(ui.tabela_produto, "Erro", "Escolha apenas uma opção: insira a quantidade ou marque a opção de renovar com a mesma quantidade.")
                return

            if renovar_padrao_checkbox.isChecked():
                id_produto = ui.IDPRODUTOQUANTIDADE

                is_evento = VerificarSeProdutoEhEvento(id_produto)

                if is_evento:
                    quantidade = GetQuantidadeProdutoEvento(id_produto)  
                else:
                    quantidade = GetQuantidadeProduto(id_produto)

            try:
                quantidade = int(quantidade)  
                if quantidade <= 0:
                    raise ValueError  
            except ValueError:
                QMessageBox.warning(ui.tabela_produto, "Erro", "Por favor, insira uma quantidade válida.")
                return

            UiTabelaProduto.AtualizarStatus(ui, linha, "Ativo")

            id_produto = ui.IDPRODUTOQUANTIDADE

            is_evento = VerificarSeProdutoEhEvento(id_produto)

            if is_evento:
                UpdateStockEvento(id_produto, quantidade) 
            else:
                UpdateStock(id_produto, quantidade)  

            dialog.accept()

            QMessageBox.information(ui.tabela_produto, "Sucesso", f"Estoque renovado com {quantidade} unidades.")

        except Exception as e:
            QMessageBox.critical(ui.tabela_produto, "Erro", f"Ocorreu um erro: {str(e)}")

    @staticmethod
    def AtualizarStatus(ui, linha, texto):
        try:
            if linha < 0 or linha >= ui.tabela_produto.rowCount():
                print(f"Erro: Linha {linha} fora dos limites da tabela.")
                return
    
            item = ui.tabela_produto.item(linha, 5)
    
            if item is None:
                item = QTableWidgetItem()  
                ui.tabela_produto.setItem(linha, 5, item)  
    
            item.setText(texto)
    
            id_produto = ui.IDPRODUTOQUANTIDADE
    
            UpdateStatus(id_produto, texto)
    
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
        for linha in range(ui.tabela_produto.rowCount()):
            item = ui.tabela_produto.item(linha, 5)  
            if item:
                texto_status = item.text()
                UiTabelaProduto.EstilizarStatus(item, texto_status)