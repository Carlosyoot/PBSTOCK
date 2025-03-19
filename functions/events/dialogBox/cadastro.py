from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from database.Datalogic import GetProdutosAll
from functions.events.dialogBox.dialog_produto import Ui_Dialog_produto  # Importe a classe gerada pelo pyuic5
from functions.events.dialogBox.interface import Ui_Dialog
from functions.events.searchs.CustomSugestion import DetailedCompleterEvent

class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, main_window=None):
        super(CustomLineEdit, self).__init__(parent)
        self.main_window = main_window  # Referência à janela principal

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Verifica se este é o último QLineEdit da linha
            if self == self.parent().layout().itemAt(self.parent().layout().count() - 2).widget():
                self.main_window.focus_next_line(self.parent())  # Chama o método da janela principal
            else:
                self.focusNextChild()  # Move o foco para o próximo widget na mesma linha
        else:
            super(CustomLineEdit, self).keyPressEvent(event)

class ProductDialog(QtWidgets.QDialog, Ui_Dialog_produto):
    def __init__(self, parent=None):
        super(ProductDialog, self).__init__(parent)
        self.setupUi(self)  # Configura a interface

        # Configura o autocompletar detalhado
        self.detailed_completer = DetailedCompleterEvent(
            GetProdutosAll,  # Função que busca os dados dos produtos
            self.line_buscar_produtos_evento  # Campo de "Produto"
        )
        self.line_buscar_produtos_evento.setCompleter(self.detailed_completer)

        # Conecta o botão "OK" ao método accept()
        self.finalizar_produto_evento.clicked.connect(self.accept)

    def accept(self):
        # Verifica se o texto digitado corresponde a um item válido no autocompletar
        current_text = self.line_buscar_produtos_evento.text().strip()
        if not self.detailed_completer.is_valid_selection(current_text):
            # Exibe um alerta se o texto não for válido
            QtWidgets.QMessageBox.warning(
                self,
                "Produto inválido",
                "Selecione um produto válido da lista de autocompletar."
            )
            return  # Impede o fechamento do diálogo

        # Se o texto for válido, chama o método accept() padrão
        super().accept()

    def get_selected_product(self):
        # Retorna os dados do produto selecionado
        return self.detailed_completer.get_selected_data()
    
    
class MyWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)  # Inicializa a interface gerada

        # Configura o layout do scrollAreaWidgetContents
        self.scrollAreaWidgetContents.setFocusPolicy(Qt.NoFocus)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.addStretch()

        # Conecta os botões
        self.Adicionar.clicked.connect(self.show_product_dialog)
        self.Finalizar.clicked.connect(self.finish)

        self.current_editing_line = None  # Armazena a linha atual que está sendo editada
        self.last_focused_widget = None  # Armazena o último QLineEdit com foco

        # Lista para armazenar os widgets das linhas
        self.linhas = []

    def show_product_dialog(self):
        # Abre o diálogo de seleção de produto
        dialog = ProductDialog(self)  # Use ProductDialog, não Ui_Dialog_produto
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            produto_data = dialog.get_selected_product()
            if produto_data:  # Se um produto foi selecionado
                self.add_item(produto_data)

    def add_item(self, produto_data):
        item_widget = QtWidgets.QWidget()
        item_layout = QtWidgets.QHBoxLayout(item_widget)

        # Campos da linha
        campos = []
        for i, (width, placeholder) in enumerate([
            (240, 'Produto'), (100, 'Quantidade'), (140, 'Valor unitário'), (320, 'Descrição')
        ]):
            line_edit = CustomLineEdit(item_widget, self)  # Passa a janela principal como main_window
            line_edit.setFixedSize(width, 41)
            line_edit.setPlaceholderText(placeholder)
            line_edit.setStyleSheet("""
            QLineEdit {
                font: 10pt "Montserrat";
            }
            QLineEdit:focus {
                border: 2px solid rgb(0, 120, 215);  /* Borda mais grossa e azul quando focado */
            }
            """)
            campos.append(line_edit)
            item_layout.addWidget(line_edit)

        # Preenche os campos com os dados do produto selecionado
        nome, codigo, quantidade, valor, descricao = produto_data
        campos[0].setText(nome)  # Produto
        campos[1].setText(str(quantidade))  # Quantidade
        campos[2].setText(str(valor))  # Valor unitário
        campos[3].setText(descricao)  # Descrição

        delete_button = QtWidgets.QPushButton(self)
        delete_button.setFixedSize(41, 41)
        delete_button.setIcon(QIcon(":/icones/delete.png"))
        delete_button.setIconSize(QSize(25, 25))
        delete_button.setStyleSheet("""
        QPushButton {
            border: 2px;
            background-color: rgb(255, 101, 70);
            color: white;
            border-radius: 5px;
            font: 10pt "Montserrat";
            outline: 0;
        }
        QPushButton:hover {
            background-color: rgb(255, 130, 100);
        }
        """)
        delete_button.clicked.connect(lambda _, widget=item_widget: self.remove_specific_item(widget))

        item_layout.addWidget(delete_button)

        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item_widget)
        self.scrollAreaWidgetContents.adjustSize()

        # Armazena a linha na lista de linhas
        self.linhas.append((item_widget, campos))

        # Restaura o foco para o último QLineEdit com foco ou para o primeiro campo da nova linha
        if self.last_focused_widget is not None:
            self.last_focused_widget.setFocus()
        else:
            item_layout.itemAt(0).widget().setFocus()

        # Força a atualização antes de rolar
        QtWidgets.QApplication.processEvents()
        self.scrollAreaWidgetContents.adjustSize()
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def get_collected_data(self):
        # Retorna os dados coletados dos produtos
        produtos = []
        for item_widget, campos in self.linhas:
            nome = campos[0].text()  # Produto
            quantidade = campos[1].text()  # Quantidade
            valor = campos[2].text()  # Valor unitário
            descricao = campos[3].text()  # Descrição
            produtos.append((nome, quantidade, valor, descricao))
        return produtos

    def finish(self):
        # Fecha o diálogo com o status Accepted
        self.accept()

    def focus_next_line(self, current_line):
        # Encontra o índice da linha atual
        index = self.scroll_layout.indexOf(current_line)
        if index < self.scroll_layout.count() - 2:  # Verifica se há uma próxima linha
            next_line = self.scroll_layout.itemAt(index + 1).widget()
            next_line.layout().itemAt(0).widget().setFocus()  # Foca no primeiro QLineEdit da próxima linha
        else:
            # Mantém o foco no último QLineEdit da linha atual
            current_line.layout().itemAt(current_line.layout().count() - 2).widget().setFocus()

    def remove_specific_item(self, widget):
        # Remove a linha da lista de linhas
        for linha in self.linhas:
            if linha[0] == widget:
                self.linhas.remove(linha)
                break

        if self.current_editing_line == widget:
            self.current_editing_line = None
        widget.deleteLater()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())