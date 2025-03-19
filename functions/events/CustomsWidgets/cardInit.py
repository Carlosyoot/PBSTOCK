from datetime import datetime,timedelta
from PyQt5 import QtWidgets, QtCore, QtGui

from database.Datalogic import GetCardsInfo, GetEventosAtivos, GetItensForaEstoque, GetRecentSales, inserir_mudanca_card_init
from view.QRC import file_principal_rc

def init_custom_frame(ui):
    """
    Inicializa os frames personalizados.
    Se o intervalo for 0 (sempre), cria os frames imediatamente.
    Caso contrário, não cria os frames inicialmente.
    """
    # Obtém o índice selecionado no combo box
    time_index = ui.update_time_combo.currentIndex()
    intervalo_minutos = {0: 0, 1: 5, 2: 15, 3: 30}.get(time_index, 0)

    if intervalo_minutos == 0:
        # Se o intervalo for 0 (sempre), cria os frames imediatamente
        create_frames(ui)
    
    # Inicializa a função de atualização
    UpdateFrames(ui)


def init_custom_frame(ui):
    """
    Inicializa os frames personalizados e configura o timer para atualização automática.
    """
   


    create_frames(ui)


def UpdateFrames(ui):
    """
    Atualiza os frames com base no intervalo de tempo selecionado.
    
    """
    # Mapeamento do índice do combo box para minutos
    
    
    intervalo_map = {
        0: 0,   # Sempre
        1: 5,   # 5 minutos
        2: 15,  # 15 minutos
        3: 30   # 30 minutos
    }

    # Obtém o índice selecionado no combo box
    time_index = ui.update_time_combo.currentIndex()
    intervalo_minutos = intervalo_map.get(time_index, 0)  # Padrão: 0 (sempre)

    # Verifica se a função já tem uma variável estática para armazenar a última atualização
    if not hasattr(UpdateFrames, "ultima_atualizacao"):
        UpdateFrames.ultima_atualizacao = None  # Inicializa como None na primeira execução

    if intervalo_minutos == 0:
        # Se o intervalo for 0 (sempre), não faz nada (os frames já foram criados no init_custom_frame)
        pass
    else:
        # Verifica se há uma data/hora de atualização armazenada
        if UpdateFrames.ultima_atualizacao is None:
            # Se não houver data armazenada, cria uma nova referência
            UpdateFrames.ultima_atualizacao = datetime.now()

        # Calcula o tempo atual
        agora = datetime.now()

        # Verifica se o tempo desde a última atualização é maior ou igual ao intervalo
        if agora - UpdateFrames.ultima_atualizacao >= timedelta(minutes=intervalo_minutos):
            # Chama a função create_frames
            create_frames(ui)
            inserir_mudanca_card_init()  # Insere o registro no banco de dados

            # Atualiza a data/hora da última atualização
            UpdateFrames.ultima_atualizacao = agora
            
            print("TEMPO ATINGIDO")
        else:
            
            print("TEMPO NAO ATINGIDO")
            # Se o tempo ainda não passou, apenas dá um pass (não faz nada)
            pass

def create_frames(ui):
    intervalo_map = {
        0: 'dia',
        1: 'semana',
        2: 'mes',
        3: 'total'
    }

    index = ui.ordenar_item_combo.currentIndex()

    # Obtém o valor correspondente ao índice
    intervalo = intervalo_map.get(index)  # Padrão: 'total'

    # Obtém os dados das funções
    dados = GetCardsInfo(intervalo)
    dados_eventos = GetEventosAtivos()
    dados_estoque = GetItensForaEstoque()
    dados_venda = GetRecentSales()

    # Verificando e exibindo os dados ou a mensagem vazia conforme necessário
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
    """
    Alterna entre os modos "Com dados" e "Sem dados".
    
    Args:
        ui: A interface gerada pelo pyuic5.
    """
    ui.data_mode = not ui.data_mode

    create_frames(ui)  # Recria os frames com o novo modo

def fill_scroll_area(scroll_area, card_creation_function, dados=None, empty_message_text="Nenhum dado disponível", empty_icon_path="nodata.png"):
    """
    Preenche um QScrollArea com cards ou uma mensagem de "Nenhum dado disponível".
    
    Args:
        scroll_area: O QScrollArea a ser preenchido.
        card_creation_function: Função que cria um card (deve retornar um QWidget).
        dados: Lista de dados para criar os cards.
        empty_message_text: Mensagem personalizada para exibição quando não houver dados.
        empty_icon_path: Caminho do ícone para a mensagem vazia.
    """
    # Limpa o conteúdo existente do QScrollArea
    if scroll_area.widget():
        scroll_area.widget().setParent(None)

    # Cria um widget para o conteúdo rolável
    scroll_content = QtWidgets.QWidget()
    scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
    scroll_layout.setSpacing(5)
    scroll_layout.setContentsMargins(5, 5, 5, 5)

    if not dados:
        # Se não houver dados, exibe a mensagem de "Nenhum dado disponível"
        create_card(scroll_layout, "", "", "", empty_message=True, empty_message_text=empty_message_text, empty_icon_path=empty_icon_path)
    else:
        # Cria os cards com base nos dados disponíveis
        for i in range(len(dados)):
            card = card_creation_function(i, dados)  # Passa o índice e os dados
            if card is not None:  # Verifica se o card foi criado com sucesso
                scroll_layout.addWidget(card)

    # Configura o widget de conteúdo no QScrollArea
    scroll_area.setWidget(scroll_content)

    # Aplica a estilização da barra de rolagem
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
    """
    Cria um card e o adiciona ao layout fornecido.
    
    Args:
        layout: O layout onde o card será adicionado.
        title: Título do card.
        description: Descrição do card.
        image_path: Caminho da imagem do card.
        empty_message: Se True, cria um card de "Nenhum dado disponível".
    """
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
        # Extrair as três colunas retornadas: Produto, Quantidade e Vendedor
        produto, quantidade, vendedor = dados[index]
        
        # Retorna o card com as informações de produto, quantidade e vendedor
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
        
        # Layout principal do card (horizontal)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(10)  # Espaçamento menor entre os elementos
        
        if empty_message:
            # Se for um card vazio, cria o layout correspondente
            self.empty_layout = QtWidgets.QHBoxLayout()
            
            self.empty = QtWidgets.QLabel(self)
            self.empty.setFixedWidth(20)
            self.empty_layout.addWidget(self.empty)

            # Ícone personalizado para o card vazio
            self.empty_icon = QtWidgets.QLabel(self)
            self.empty_icon.setPixmap(QtGui.QPixmap(empty_icon_path).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
            self.empty_icon.setAlignment(QtCore.Qt.AlignCenter)
            self.empty_icon.setFixedWidth(65)
            self.empty_layout.addWidget(self.empty_icon)

            # Texto personalizado para o card vazio
            self.empty_label = QtWidgets.QLabel(empty_message_text)
            self.empty_label.setStyleSheet(""" 
                font: 10pt 'Arial';
                color: gray;
            """)
            self.empty_label.setAlignment(QtCore.Qt.AlignCenter)
            self.empty_label.setFixedWidth(150)

            self.empty_layout.addWidget(self.empty_label)

            # Adicionando o layout do ícone e do label ao layout principal
            self.layout.addLayout(self.empty_layout)

            # Alinha o conteúdo do layout ao centro
            self.layout.setAlignment(QtCore.Qt.AlignVCenter)  # Alinhamento vertical ao centro
        else:
            # Adicionando uma imagem (ou ícone)
            self.image_label = QtWidgets.QLabel(self)
            self.image_label.setPixmap(QtGui.QPixmap(image_path).scaled(30, 30, QtCore.Qt.KeepAspectRatio))
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.image_label.setFixedWidth(30)
            self.layout.addWidget(self.image_label)
            
            # Adicionando o título
            self.title_label = QtWidgets.QLabel(title)
            self.title_label.setStyleSheet(""" 
                font: 9pt 'Arial';
                color: black;
                padding-left: 10px;
            """)
            self.title_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.title_label.setFixedWidth(140)
            self.layout.addWidget(self.title_label)
            
            # Adicionando a descrição (informação adicional)
            self.description_label = QtWidgets.QLabel(description)
            self.description_label.setStyleSheet("font: 8pt 'Arial'; color: gray; padding-right: 10px;")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.description_label)
