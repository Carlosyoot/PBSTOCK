from PyQt5.QtWidgets import QCompleter, QListView, QStyledItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

# Função auxiliar para mostrar o texto (fora da classe)
def displayText(value, locale):
    if len(value) > 50:
        return value[:50] + "..."
    return value

# Função para criar o popup (fora da classe)
def create_popup():
    popup = QListView()
    popup.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    return popup

# Função para popular os dados (fora da classe)
def populate(model, data):
    model.clear()
    for item in data:
        parts = item.rsplit(' - ', 1)  # Divide apenas no último ' - '
        if len(parts) == 2:
            name, code = parts
        else:
            name, code = item, ""
        product_item = QStandardItem(item)
        code_item = QStandardItem(code)
        model.appendRow([product_item, code_item])
        
def DetailPopulate(model, data):
    for produto in data:
        nome, codigo, quantidade, valor, descricao = produto
        # Cria o texto que será exibido no QCompleter
        display_text = f"{nome} - {codigo}"
        item = QStandardItem(display_text)
        
        # Armazena os dados adicionais no Qt.UserRole
        item.setData((nome, str(quantidade), str(valor), descricao), Qt.UserRole)
        
        # Adiciona o item ao modelo
        model.appendRow(item)

# Função para pegar o caminho do índice (fora da classe)
def pathFromIndex(index, column):
    return index.sibling(index.row(), column).data()

# Classe ProductDelegate
class ProductDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        return displayText(value, locale)  # Usando a função externa

# Classe itCompleterCód
class CustomCompleterCód(QCompleter):
    def __init__(self, data_fetcher, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup())  # Usando a função externa
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        populate(self.model, data_fetcher())  # Usando a função externa

    def pathFromIndex(self, index):
        return pathFromIndex(index, 1)  # Usando a função externa para pegar o código (coluna 1)

# Classe CustomCompleterNome
class CustomCompleterNome(QCompleter):
    def __init__(self, data_fetcher, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup())  # Usando a função externa
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        populate(self.model, data_fetcher())  # Usando a função externa

    def pathFromIndex(self, index):
        return pathFromIndex(index, 0)  # Usando a função externa para pegar o nome (coluna 0)
    
    
class DetailedCompleter(QCompleter):
    def __init__(self, data_fetcher, produto_edit, quantity_edit, value_edit, description_edit, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setPopup(create_popup())  # Usando a função externa
        self.popup().setItemDelegate(ProductDelegate())
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(5)
        DetailPopulate(self.model, data_fetcher())  # Usando a função externa

        # Armazena os campos que serão preenchidos
        self.produto_edit = produto_edit
        self.quantity_edit = quantity_edit
        self.value_edit = value_edit
        self.description_edit = description_edit

        # Conecta o sinal activated ao método fill_detailed_fields
        self.activated.connect(self.fill_detailed_fields)

    def pathFromIndex(self, index):
        # Retorna apenas o nome do produto (primeira parte da string)
        full_text = index.data(Qt.DisplayRole)
        return full_text.split(' - ')[0]

    def splitPath(self, path):
        return [path]

    def fill_detailed_fields(self, text):
    # Preenche os campos com base no item selecionado
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item and item.text().split(' - ')[0] == text:
                # Recupera os dados armazenados no Qt.UserRole
                nome, quantidade, valor, descricao = item.data(Qt.UserRole)
                
                # Preenche o campo de "Produto" com o nome do produto
                self.produto_edit.setText(nome)
                
                # Preenche os outros campos
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

        # Armazena o campo de "Produto"
        self.produto_edit = produto_edit

        # Conecta o sinal activated ao método fill_detailed_fields
        self.activated.connect(self.fill_detailed_fields)

        # Preenche o modelo com os dados dos produtos
        self.populate_model(data_fetcher())

    def populate_model(self, produtos):
        # Limpa o modelo
        self.model.clear()

        # Adiciona os produtos ao modelo
        for produto in produtos:
            # Suponha que produto seja uma tupla: (nome, codigo, quantidade, valor, descricao)
            nome, codigo, quantidade, valor, descricao = produto
            item = QStandardItem(nome)
            item.setData((nome, codigo, quantidade, valor, descricao), Qt.UserRole)  # Armazena todos os dados do produto
            self.model.appendRow(item)

    def fill_detailed_fields(self, text):
        # Preenche os campos com base no item selecionado
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item and item.text() == text:
                # Recupera os dados armazenados no Qt.UserRole
                self.selected_data = item.data(Qt.UserRole)
                break

    def get_selected_data(self):
        # Retorna os dados do produto selecionado
        return self.selected_data

    def is_valid_selection(self, text):
        # Verifica se o texto corresponde a um item no modelo
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item and item.text() == text:
                return True
        return False