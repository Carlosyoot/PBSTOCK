from view.pages.FRMadmin import Ui_FrmAdmin
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from functions.events.adminevents import *
from functions.events.timeevents import *
from functions.events.alertsevents import *


class FrmAdmin(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        # Configuração inicial da interface
        self.ui.lbl_seja_bem_vindo_primary.setText(f'Olá, {user_name}')
        self.ui.lbl_seja_bem_vindo.setText('Seja Bem-Vindo')
        self.ui.lbl_seja_bem_vindo.setFixedWidth(500)

        # Deixa os botões como "checkable" para funcionarem como toggle
        self.ui.admin_button.setCheckable(True)
        self.ui.colaborador_button.setCheckable(True)

        # Conecta os botões à função de alternância
        self.ui.admin_button.clicked.connect(self.selecionar_admin)
        self.ui.colaborador_button.clicked.connect(self.selecionar_colaborador)

        # Conectar eventos adicionais
        conectar_eventos(self.ui)
        self.iniciar_tempo()
        self.alert_manager = AlertManager(self.ui)

        # Define estado inicial (opcional)
        self.ui.admin_button.setChecked(True)  # Por exemplo, Admin como padrão

    def selecionar_admin(self):
        """Marca Admin e desmarca Colaborador"""
        print('entrou funcao admin')
        self.ui.admin_button.setChecked(True)
        self.ui.colaborador_button.setChecked(False)

    def selecionar_colaborador(self):
        """Marca Colaborador e desmarca Admin"""
        print('entrou funcao colaborador')
        self.ui.admin_button.setChecked(False)
        self.ui.colaborador_button.setChecked(True)

    def iniciar_tempo(self):
        """Inicia o timer para atualizar hora/data e verificar saída"""
        self.tempo = QTimer(self)
        self.tempo.timeout.connect(lambda: HoraData(self.ui))
        self.tempo.timeout.connect(lambda: Sair(self.ui, "23:59:59"))
        self.tempo.start(1000)

    def obter_perfil_selecionado(self):
        """Retorna o perfil atualmente selecionado"""
        if self.ui.admin_button.isChecked():
            return "admin"
        elif self.ui.colaborador_button.isChecked():
            return "colaborador"
        return "nenhum"


class WindowManager:
    SecondWindow = None

    @classmethod
    def open_admin(cls, user_name):
        if cls.SecondWindow is None or not cls.SecondWindow.isVisible():
            cls.SecondWindow = FrmAdmin(user_name)
            cls.SecondWindow.show()
