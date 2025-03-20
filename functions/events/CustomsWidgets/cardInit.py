from datetime import datetime,timedelta
from PyQt5 import QtWidgets, QtCore, QtGui

from database.Datalogic import GetCardsInfo, GetEventosAtivos, GetItensForaEstoque, GetRecentSales, inserir_mudanca_card_init
from view.QRC import file_principal_rc

def init_custom_frame(ui):

    time_index = ui.update_time_combo.currentIndex()
    intervalo_minutos = {0: 0, 1: 5, 2: 15, 3: 30}.get(time_index, 0)

    if intervalo_minutos == 0:
        create_frames(ui)
    
    UpdateFrames(ui)


def init_custom_frame(ui):

    create_frames(ui)


def UpdateFrames(ui):

    intervalo_map = {
        0: 0,  
        1: 5,  
        2: 15,  
        3: 30   
    }

    time_index = ui.update_time_combo.currentIndex()
    intervalo_minutos = intervalo_map.get(time_index, 0)
    

    if not hasattr(UpdateFrames, "ultima_atualizacao"):
        UpdateFrames.ultima_atualizacao = None 

    if intervalo_minutos == 0:
        create_frames(ui)

        pass
    else:
        if UpdateFrames.ultima_atualizacao is None:
            UpdateFrames.ultima_atualizacao = datetime.now()

        agora = datetime.now()

        if agora - UpdateFrames.ultima_atualizacao >= timedelta(minutes=intervalo_minutos):
            create_frames(ui)
            inserir_mudanca_card_init() 

            UpdateFrames.ultima_atualizacao = agora
            
            print("TEMPO ATINGIDO")
        else:
            
            print("TEMPO NAO ATINGIDO")
            pass

def create_frames(ui):
    intervalo_map = {
        0: 'dia',
        1: 'semana',
        2: 'mes',
        3: 'total'
    }

    index = ui.ordenar_item_combo.currentIndex()

    intervalo = intervalo_map.get(index)  

    dados = GetCardsInfo(intervalo)
    dados_eventos = GetEventosAtivos()
    dados_estoque = GetItensForaEstoque()
    dados_venda = GetRecentSales()

    if dados_eventos:
        fill_scroll_area(ui.ScrollEventAtive, create_event_card, dados=dados_eventos)
    else:
        fill_scroll_area(
            ui.ScrollEventAtive,
            create_event_card,
            empty_message_text="Nenhum evento \nativo no momento.",
            empty_icon_path=":/icones/cancel-event.png"
        )

    if dados_venda:
        fill_scroll_area(ui.ScrollMostSellerItem, create_sales_card, dados=dados_venda)
    else:
        fill_scroll_area(
            ui.ScrollMostSellerItem,
            create_sales_card,
            empty_message_text="Nenhum item de \nvendas foi encontrado.",
            empty_icon_path=":/icones/nodata.png"
        )

    if dados:
        fill_scroll_area(ui.ScrollRecentSell, create_top_selling_card, dados=dados)
    else:
        fill_scroll_area(
            ui.ScrollRecentSell,
            lambda i: create_top_selling_card(i, dados),
            empty_message_text="Nenhuma venda \nrecente registrada.",
            empty_icon_path=":/icones/price.png"
        )

    if dados_estoque:
        fill_scroll_area(ui.ScrollOutstock, create_out_of_stock_card, dados=dados_estoque)
    else:
        fill_scroll_area(
            ui.ScrollOutstock,
            create_out_of_stock_card,
            empty_message_text="Ótimo! Nenhum \nproduto esgotado.",
            empty_icon_path=":/icones/happy-face.png"
        )

def toggle_data_mode(ui):
    ui.data_mode = not ui.data_mode

    create_frames(ui) 

def fill_scroll_area(scroll_area, card_creation_function, dados=None, empty_message_text="Nenhum dado disponível", empty_icon_path="nodata.png"):
    if scroll_area.widget():
        scroll_area.widget().setParent(None)

    scroll_content = QtWidgets.QWidget()
    scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
    scroll_layout.setSpacing(5)
    scroll_layout.setContentsMargins(5, 5, 5, 5)

    if not dados:
        create_card(scroll_layout, "", "", "", empty_message=True, empty_message_text=empty_message_text, empty_icon_path=empty_icon_path)
    else:
        for i in range(len(dados)):
            card = card_creation_function(i, dados)  
            if card is not None:  
                scroll_layout.addWidget(card)

    scroll_area.setWidget(scroll_content)

    scroll_area.setStyleSheet("""
        QScrollBar:vertical {
            background-color: #f1f1f1;  /* Cor do trilho */
            width: 8px;                /* Largura da barra vertical */
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #FFD700;  /* Cor do handle (amarelo) */
            min-height: 20px;          /* Altura mínima do handle */
            border-radius: 4px;        /* Bordas arredondadas */
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            background: none;          /* Remove as setas */
        }
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;          /* Remove o fundo ao redor do handle */
        }
        QScrollBar:horizontal {
            background-color: #f1f1f1; /* Cor do trilho */
            height: 8px;               /* Altura da barra horizontal */
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background-color: #FFD700; /* Cor do handle (amarelo) */
            min-width: 20px;           /* Largura mínima do handle */
            border-radius: 4px;        /* Bordas arredondadas */
        }
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            background: none;          /* Remove as setas */
        }
        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {
            background: none;          /* Remove o fundo ao redor do handle */
        }
    """)

def create_card(layout, title, description, image_path, empty_message=False, empty_message_text="Nenhum dado disponível", empty_icon_path="nodata.png"):

    card = NewsCard(title, description, image_path, empty_message=empty_message, empty_message_text=empty_message_text, empty_icon_path=empty_icon_path)
    layout.addWidget(card)

def create_event_card(index, dados):
    if dados and index < len(dados):
        nome_evento, data_inicio = dados[index]
        return NewsCard(
            title=f"{nome_evento}",
            description=f"Início: {data_inicio}",
            image_path=":/icones/planner.png"
        )
    else:
        return None

def create_sales_card(index, dados):
    if dados and index < len(dados):
        produto, quantidade, vendedor = dados[index]
        
        return NewsCard(
            title=f"{produto}",
            description=f"{vendedor}",
            image_path=":/icones/vendidoIcon.png"
        )
    else:
        return None

def create_top_selling_card(index, dados):
    if dados and index < len(dados):
        produto, quantidade = dados[index]
        return NewsCard(
            title=f"{produto}",
            description=f"Vendas: {quantidade}",
            image_path=":/icones/quality.png"
        )
    else:
        return None

def create_out_of_stock_card(index, dados):
    if dados and index < len(dados):
        produto, quantidade = dados[index]
        return NewsCard(
            title=f"{produto}",
            description=f"Data: {quantidade}",
            image_path=":/icones/out-of-stock.png"
        )
    else:
        return None

class NewsCard(QtWidgets.QWidget):
    def __init__(self, title, description, image_path, parent=None, empty_message=False, empty_message_text="Nenhum dado disponível", empty_icon_path="nodata.png"):
        super().__init__(parent)
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(10)  
        
        if empty_message:
            self.empty_layout = QtWidgets.QHBoxLayout()
            
            self.empty = QtWidgets.QLabel(self)
            self.empty.setFixedWidth(20)
            self.empty_layout.addWidget(self.empty)

            self.empty_icon = QtWidgets.QLabel(self)
            self.empty_icon.setPixmap(QtGui.QPixmap(empty_icon_path).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
            self.empty_icon.setAlignment(QtCore.Qt.AlignCenter)
            self.empty_icon.setFixedWidth(65)
            self.empty_layout.addWidget(self.empty_icon)

            self.empty_label = QtWidgets.QLabel(empty_message_text)
            self.empty_label.setStyleSheet(""" 
                font: 10pt 'Arial';
                color: gray;
            """)
            self.empty_label.setAlignment(QtCore.Qt.AlignCenter)
            self.empty_label.setFixedWidth(150)

            self.empty_layout.addWidget(self.empty_label)

            self.layout.addLayout(self.empty_layout)

            self.layout.setAlignment(QtCore.Qt.AlignVCenter) 
        else:
            self.image_label = QtWidgets.QLabel(self)
            self.image_label.setPixmap(QtGui.QPixmap(image_path).scaled(30, 30, QtCore.Qt.KeepAspectRatio))
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.image_label.setFixedWidth(30)
            self.layout.addWidget(self.image_label)
            
            self.title_label = QtWidgets.QLabel(title)
            self.title_label.setStyleSheet(""" 
                font: 9pt 'Arial';
                color: black;
                padding-left: 10px;
            """)
            self.title_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.title_label.setFixedWidth(140)
            self.layout.addWidget(self.title_label)
            
            self.description_label = QtWidgets.QLabel(description)
            self.description_label.setStyleSheet("font: 8pt 'Arial'; color: gray; padding-right: 10px;")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.description_label)
