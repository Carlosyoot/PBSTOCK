from PyQt5.QtWidgets import QCompleter, QListView, QStyledItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

def displayText(value, locale):
    if len(value) > 50:
        return value[:50] + "..."
    return value

def create_popup():
    popup = QListView()
    popup.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    return popup

def populate(model, data):
    model.clear()
    for item in data:
        parts = item.split(' - ')
        
        if len(parts) == 3:
            nome, nome_evento, codigo = parts
            display_text = f"{nome} - {nome_evento} - {codigo}"
        elif len(parts) == 2:
            nome, codigo = parts
            display_text = f"{nome} - {codigo}"
        else:
            continue
        
        product_item = QStandardItem(display_text)
        code_item = QStandardItem(codigo)
        model.appendRow([product_item, code_item])
        
def DetailPopulate(model, data):
    for produto in data:
        nome, codigo, quantidade, valor, descricao = produto
        display_text = f"{nome} - {codigo}"
        item = QStandardItem(display_text)
        
        item.setData((nome, str(quantidade), str(valor), descricao), Qt.UserRole)
        
        model.appendRow(item)

def pathFromIndex(index, column):
    return index.sibling(index.row(), column).data()

class ProductDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        return displayText(value, locale)  

class CustomCompleterCód(QCompleter):
    def __init__(self, data_fetcher, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup()) 
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        populate(self.model, data_fetcher())  

    def pathFromIndex(self, index):
        full_text = index.data()
        
        parts = full_text.split(' - ')
        if len(parts) >= 2:
            return parts[-1]  
        return full_text  

class CustomCompleterNome(QCompleter):
    def __init__(self, data_fetcher, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup())  
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        populate(self.model, data_fetcher())  

    def pathFromIndex(self, index):
        return pathFromIndex(index, 0) 
    
class CustomCompleterNomeEvento(QCompleter):
    def __init__(self, data_fetcher, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup()) 
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        populate(self.model, data_fetcher())    
    

    
class DetailedCompleter(QCompleter):
    def __init__(self, data_fetcher, produto_edit, quantity_edit, value_edit, description_edit, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup()) 
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        DetailPopulate(self.model, data_fetcher())  

        self.produto_edit = produto_edit
        self.quantity_edit = quantity_edit
        self.value_edit = value_edit
        self.description_edit = description_edit

        self.activated.connect(self.fill_detailed_fields)

    def pathFromIndex(self, index):
        full_text = index.data(Qt.DisplayRole)
        return full_text.split(' - ')[0]

    def splitPath(self, path):
        return [path]

    def fill_detailed_fields(self, text):
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item and item.text().split(' - ')[0] == text:
                nome, quantidade, valor, descricao = item.data(Qt.UserRole)
                
                self.produto_edit.setText(nome)
                
                self.quantity_edit.setText(quantidade)
                self.value_edit.setText(valor)
                self.description_edit.setText(descricao)
                break
            
            

class DetailedCompleterEvent(QCompleter):
    def __init__(self, data_fetcher, produto_edit, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)

        self.produto_edit = produto_edit

        self.activated.connect(self.fill_detailed_fields)

        self.populate_model(data_fetcher())

    def populate_model(self, produtos):
        self.model.clear()

        for produto in produtos:
            nome, codigo, quantidade, valor, descricao = produto
            item = QStandardItem(nome)
            item.setData((nome, codigo, quantidade, valor, descricao), Qt.UserRole) 
            self.model.appendRow(item)

    def fill_detailed_fields(self, text):
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item and item.text() == text:
                self.selected_data = item.data(Qt.UserRole)
                break

    def get_selected_data(self):
        return self.selected_data

    def is_valid_selection(self, text):
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item and item.text() == text:
                return True
        return False