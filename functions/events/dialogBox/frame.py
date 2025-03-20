from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QScrollArea, QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from functions.events.searchs.CustomSugestion import DetailedCompleter
from database.Datalogic import GetProdutosAll
from PyQt5.QtCore import QSize, Qt
import sys


class CustomLineEdit(QLineEdit):
    def __init__(ui, parent=None):
        super().__init__(parent)

    def keyPressEvent(ui, event):
       
        if event.key() == Qt.Key_Right:
            ui.parent().focusNextChild()
        elif event.key() == Qt.Key_Left:
            ui.parent().focusPreviousChild()
        else:
            super().keyPressEvent(event)


class CustomDialog(QDialog):
    def __init__(ui, parent=None):
        super().__init__(parent)

    def keyPressEvent(ui, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            focused_widget = ui.focusWidget()
            if isinstance(focused_widget, QLineEdit):
                ui.focusNextChild()
                
                next_widget = ui.focusWidget()
                if isinstance(next_widget, QPushButton) and next_widget.text() == "":
                    ui.focusNextChild()
            elif isinstance(focused_widget, QPushButton):
                focused_widget.click()
            else:
                event.ignore()
        else:
            super().keyPressEvent(event)


class MyDialog(CustomDialog):
    def __init__(ui, parent=None):
        super().__init__(parent)
        
        ui.setWindowTitle("Adicionar Linhas Editáveis")
        ui.setGeometry(100, 100, 1140, 510)
        ui.collected_data = None 
        ui.setFocusPolicy(Qt.NoFocus)
        
        if parent:
            ui.move(parent.geometry().center() - ui.rect().center())

        ui.scroll_area = QScrollArea(ui)
        ui.scroll_widget = QWidget()
        ui.scroll_area.setWidget(ui.scroll_widget)
        ui.scroll_area.setWidgetResizable(True)
        ui.scroll_area.setGeometry(20, 90, 940, 401)

        ui.scroll_area.setFocusPolicy(Qt.NoFocus)
        ui.scroll_widget.setFocusPolicy(Qt.NoFocus)

        ui.scroll_layout = QVBoxLayout(ui.scroll_widget)
        ui.scroll_layout.setSpacing(20)
        ui.scroll_layout.setContentsMargins(10, 10, 10, 10)
        ui.scroll_layout.addStretch()

      
        ui.add_button = QPushButton(ui)
        ui.add_button.setGeometry(1070, 100, 50, 41)
        ui.add_button.setIcon(QIcon(":/icones/addicon.png"))
        ui.add_button.setIconSize(QSize(25, 25))
        ui.add_button.setStyleSheet("""
        QPushButton {
            border: 2px;
            background-color: rgb(116, 170, 74);
            color: white;
            border-radius: 5px;
            font: 10pt "Montserrat";
            outline: 0;
        }
        QPushButton:hover {
            background-color: rgb(140, 200, 90);
        }
        """)
        ui.add_button.clicked.connect(ui.add_item)
        ui.add_button.focusInEvent = lambda event, button=ui.add_button: ui.highlight_button(button)
        ui.add_button.focusOutEvent = lambda event, button=ui.add_button: ui.unhighlight_button(button)

       
        ui.add_button.setAutoDefault(False)
        ui.add_button.setDefault(False)

        ui.finish_button = QPushButton("Finalizar", ui)
        ui.finish_button.setGeometry(980, 450, 141, 41)
        ui.finish_button.setStyleSheet('''
        QPushButton {
            border: 2px;
            background-color: rgb(159, 63, 250);
            color: white;
            border-radius: 5px;
            font: 10pt "Montserrat";
            outline: 0;
        }
        QPushButton:hover {
            background-color: rgb(197, 62, 255);
        }
        ''')
        ui.finish_button.clicked.connect(ui.collect_data)
        ui.finish_button.focusInEvent = lambda event, button=ui.finish_button: ui.highlight_button(button)
        ui.finish_button.focusOutEvent = lambda event, button=ui.finish_button: ui.unhighlight_button(button)

        ui.finish_button.setAutoDefault(False)
        ui.finish_button.setDefault(False)

        ui.add_item()
        ui.personalizar_scrollbar()
        ui.setup_tab_order()
        
    def personalizar_scrollbar(ui):
        ui.scroll_area.verticalScrollBar().setStyleSheet("""
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #3498db;
            border-radius: 5px;
            min-height: 20px;
        }
        """)
        
    def focused_style(ui):
        return """
        border: 2px solid black;  /* Borda preta quando focado */
        color: #004d40;
        font: 10pt "Montserrat";
        """

    def unfocused_style(ui):
        return """
        background-color: rgba(0, 0, 0, 0);
        border: 1px solid rgb(66, 66, 66);
        color: rgb(0, 0, 0);
        border-radius: 0px;
        font: 10pt "Montserrat";
        """

    def highlight_button(ui, button):
        if not hasattr(button, 'original_style'):
            button.original_style = button.styleSheet()
        button.setStyleSheet(button.original_style + """
        QPushButton {
            border: 2px solid black;  /* Borda preta quando focado */
        }
        """)

    def unhighlight_button(ui, button):
        if hasattr(button, 'original_style'):
            button.setStyleSheet(button.original_style)

    def setup_tab_order(ui):
        last_widget = None

        for i in range(ui.scroll_layout.count() - 1):
            item_layout = ui.scroll_layout.itemAt(i).layout()
            if item_layout:
                for j in range(item_layout.count()):
                    widget = item_layout.itemAt(j).widget()
                    if isinstance(widget, (QLineEdit, QPushButton)):
                        if last_widget:
                            ui.setTabOrder(last_widget, widget)
                        last_widget = widget

        if last_widget:
            ui.setTabOrder(last_widget, ui.finish_button)

        ui.setTabOrder(ui.finish_button, ui.add_button)

        if ui.scroll_layout.count() > 1:
            ui.scroll_layout.itemAt(0).layout().itemAt(0).widget().setFocus()

    def add_item(ui):
        item_layout = QHBoxLayout()

        # Cria os campos de entrada
        campos = []
        for i in range(4):
            line_edit = CustomLineEdit(ui)  
            line_edit.setFixedHeight(41)
            line_edit.setStyleSheet(ui.unfocused_style())
            line_edit.focusInEvent = lambda event, line_edit=line_edit: ui.highlight_widget(line_edit)
            line_edit.focusOutEvent = lambda event, line_edit=line_edit: ui.unhighlight_widget(line_edit)

            if i == 0:
                line_edit.setFixedWidth(200)
                line_edit.setPlaceholderText('Produto')
                campo_produto = line_edit 
            elif i == 3:
                line_edit.setFixedWidth(320)
                line_edit.setPlaceholderText('Descrição')
                campo_descricao = line_edit  
            elif i == 1:
                line_edit.setFixedWidth(100)
                line_edit.setPlaceholderText('Quantidade')
                campo_quantidade = line_edit 
            elif i == 2:
                line_edit.setFixedWidth(140)
                line_edit.setPlaceholderText('Valor unitário')
                campo_valor = line_edit 

            campos.append(line_edit)
            item_layout.addWidget(line_edit)

       
        detailed_completer = DetailedCompleter(
            GetProdutosAll,  
            campo_produto,  
            campo_quantidade,   
            campo_descricao     
        )
        campo_produto.setCompleter(detailed_completer)

        delete_button = QPushButton(ui)
        delete_button.setFixedSize(60, 41)
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
        delete_button.clicked.connect(lambda _, layout=item_layout: ui.remove_specific_item(layout))
        delete_button.focusInEvent = lambda event, button=delete_button: ui.highlight_button(button)
        delete_button.focusOutEvent = lambda event, button=delete_button: ui.unhighlight_button(button)

        delete_button.setAutoDefault(False)
        delete_button.setDefault(False)

        item_layout.addWidget(delete_button)

        ui.scroll_layout.insertLayout(ui.scroll_layout.count() - 1, item_layout)
        ui.scroll_widget.adjustSize()

        ui.setup_tab_order()

        item_layout.itemAt(0).widget().setFocus()
    
    def highlight_widget(ui, widget):
        widget.setStyleSheet(ui.focused_style())

    def unhighlight_widget(ui, widget):
        widget.setStyleSheet(ui.unfocused_style())

    def remove_specific_item(ui, item_layout):
        for i in reversed(range(item_layout.count())):
            widget = item_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        item_layout.deleteLater()
        ui.scroll_widget.adjustSize()
        ui.setup_tab_order()

    def collect_data(ui):
        data = []
        empty_fields = False
        total_produtos = 0

        for i in range(ui.scroll_layout.count() - 1):
            item_layout = ui.scroll_layout.itemAt(i).layout()
            if item_layout:
                item_data = []
                for j in range(item_layout.count()):
                    widget = item_layout.itemAt(j).widget()
                    if isinstance(widget, QLineEdit):
                        text = widget.text()
                        if not text:
                            empty_fields = True
                        item_data.append(text)
                data.append(item_data)
                total_produtos += 1

        if empty_fields:
            QMessageBox.warning(ui, "Campos Vazios", "Existem campos vazios! Preencha todos antes de finalizar.")
            return None  
        print(f"Total de produtos feitos: {total_produtos}")
        print("Dados coletados:")
        for idx, item in enumerate(data):
            print(f"Item {idx + 1}: {item}")

        ui.collected_data = data  
        ui.accept()  

        return data  


from view.QRC import file_principal_rc

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.exec_()