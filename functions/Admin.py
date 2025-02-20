from view.pages.NonFormatedFRMadmin import Ui_FrmAdmin
from PyQt5.QtWidgets import QMainWindow
from functions.events.adminevents import *



class FrmAdmin(QMainWindow):
    def __init__(self, user_name):

        #global filtro, search_fornecedores, window


        super().__init__()
        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)
        
        # Aqui, use 'user_name' para configurar o texto
        self.ui.lbl_seja_bem_vindo.setText(f'Seja Bem-Vindo(a) - {user_name}')
        self.ui.lbl_titulo_vendas.setText(f'Vendedor(a) - {user_name}')
        self.ui.lbl_seja_bem_vindo.setFixedWidth(500)
        
        conectar_eventos(self.ui)

class WindowManager:
    SecondWindow = None  # Armazena referência global para evitar fechamento automático

    @classmethod
    def open_admin(cls, user_name):
        if cls.SecondWindow is None or not cls.SecondWindow.isVisible():
            cls.SecondWindow = FrmAdmin(user_name)
            cls.SecondWindow.show()

