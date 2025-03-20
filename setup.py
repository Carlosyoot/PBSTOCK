import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from functions.Login import logar
from view.pages.FRMlogin import Ui_login

import zeromq  # Importa o zeromq.py

class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login()
        self.ui.setupUi(self)

        # Botão de logar no sistema
        self.ui.pushButton.clicked.connect(lambda: logar(self.ui, self))


def start_zeromq_thread():
    """Inicia o servidor ZeroMQ em uma thread separada."""
    zeromq_thread = threading.Thread(target=zeromq.start_zeromq, daemon=True)
    zeromq_thread.start()

if __name__ == "__main__":
    # Inicia a thread do ZeroMQ (observador)
    start_zeromq_thread()

    # Inicia a aplicação PyQt
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    app.exec_()
