from view.pages.FRMadmin import Ui_FrmAdmin
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from functions.events.adminevents import *
from functions.events.timeevents import *



class FrmAdmin(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        # Configuração inicial da interface
        self.ui.lbl_seja_bem_vindo.setText(f'{user_name}')
        self.ui.lbl_titulo_vendas.setText(f'Vendedor(a) - {user_name}')
        self.ui.lbl_seja_bem_vindo.setFixedWidth(500)

        # Conectar eventos
        conectar_eventos(self.ui)

        # Iniciar o tempo corretamente
        self.iniciar_tempo()  # Agora o método é reconhecido

    def iniciar_tempo(self):
        """Inicia o timer para atualizar hora/data e verificar saída"""
        self.tempo = QTimer(self)
        self.tempo.timeout.connect(lambda: HoraData(self.ui))  
        self.tempo.timeout.connect(lambda: Sair(self.ui, "23:59:59")) 
        self.tempo.start(1000)  # Atualiza a cada segundo

class WindowManager:
    SecondWindow = None  # Armazena referência global para evitar fechamento automático

    @classmethod
    def open_admin(cls, user_name):
        if cls.SecondWindow is None or not cls.SecondWindow.isVisible():
            cls.SecondWindow = FrmAdmin(user_name)
            cls.SecondWindow.show()

