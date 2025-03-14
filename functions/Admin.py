from view.pages.FRMadmin import Ui_FrmAdmin
from PyQt5.QtWidgets import QMainWindow
from functions.events.eventManager import EventManager



class FrmAdmin(QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        # Configuração inicial da interface
        self.ui.lbl_seja_bem_vindo_primary.setText(f'Olá, {user_name}')
        self.ui.lbl_seja_bem_vindo.setText('Seja Bem-Vindo')
        self.ui.lbl_seja_bem_vindo.setFixedWidth(500)
        
        self.ui.admin_button.setChecked(True)  # Por exemplo, Admin como padrão


        EventManager.configurar_eventos(self.ui, self)
        EventManager.iniciar_tempo(self.ui, self)
    


class WindowManager:
    SecondWindow = None

    @classmethod
    def open_admin(cls, user_name):
        if cls.SecondWindow is None or not cls.SecondWindow.isVisible():
            cls.SecondWindow = FrmAdmin(user_name)
            cls.SecondWindow.show()
