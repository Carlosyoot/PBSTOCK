import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow
from functions.Login import logar
from view.pages.FRMlogin import Ui_login
import cProfile
import pstats


class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login()
        self.ui.setupUi(self)

        # Botão de logar no sistema
        #self.ui.pushButton.clicked.connect(lambda: logar(self.ui, self))
        
        logar(self.ui, self)

    def showEvent(self, event):
        """
        Método chamado quando a janela é exibida.
        Envia uma mensagem via socket para sinalizar que a janela foi exibida.
        """
        super().showEvent(event)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5000))  # Conecta ao processo pai
            s.sendall(b"ready")  # Envia a mensagem "ready"


if __name__ == "__main__":

    # Cria a aplicação PyQt5
    app = QApplication(sys.argv)

    # Cria e exibe a janela
    janela = MinhaJanela()
    janela.show()

    # Executa a aplicação
    app_exec_return = app.exec_()

    # Encerra o programa
    sys.exit(app_exec_return)