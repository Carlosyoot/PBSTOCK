from functions.events.CustomsWidgets.ProductMenuFilter import FILTERPRODUTO
from setup import MinhaJanela
from view.pages.FRMadmin import Ui_FrmAdmin
from PyQt5.QtWidgets import QMainWindow
from functions.events.eventManager import EventManager
from PyQt5 import QtWidgets, QtCore



class FrmAdmin(QMainWindow):
    def __init__(self, user_name, parent_window=None):
        super().__init__()
        self.ui = Ui_FrmAdmin()
        self.ui.setupUi(self)

        self.parent_window = parent_window  

        #self.ui.lbl_seja_bem_vindo_primary.setText(f'Olá, {user_name}')
        #self.ui.lbl_seja_bem_vindo.setText('Seja Bem-Vindo')
        self.ui.lbl_seja_bem_vindo.setFixedWidth(500)

        self.ui.admin_button.setChecked(True)

        self.load_combo_selections()

        self.ui.ordenar_item_combo.currentIndexChanged.connect(self.save_ordenar_item_combo_selection)
        self.ui.update_time_combo.currentIndexChanged.connect(self.save_update_time_combo_selection)

        self.ui.btn_voltar.clicked.connect(self.voltar_para_login)

        EventManager.configurar_eventos(self.ui, self)
        EventManager.iniciar_tempo(self.ui, self)
        
    def voltar_para_login(self):
        self.close()  
        self.parent_window = MinhaJanela() 
        self.parent_window.show()  

    def save_ordenar_item_combo_selection(self):
        settings = QtCore.QSettings("MeuApp", "Config")
        settings.setValue("ordenar_item_combo_index", self.ui.ordenar_item_combo.currentIndex())

    def save_update_time_combo_selection(self):
        settings = QtCore.QSettings("MeuApp", "Config")
        settings.setValue("update_time_combo_index", self.ui.update_time_combo.currentIndex())

    def load_combo_selections(self):
        settings = QtCore.QSettings("MeuApp", "Config")

       
        ordenar_item_index = settings.value("ordenar_item_combo_index", 0, type=int) 
        self.ui.ordenar_item_combo.setCurrentIndex(ordenar_item_index)

      
        update_time_index = settings.value("update_time_combo_index", 0, type=int) 
        self.ui.update_time_combo.setCurrentIndex(update_time_index)


class WindowManager:
    SecondWindow = None

    @classmethod
    def open_admin(cls, user_name):
        if cls.SecondWindow is None or not cls.SecondWindow.isVisible():
            cls.SecondWindow = FrmAdmin(user_name)
            cls.SecondWindow.show()