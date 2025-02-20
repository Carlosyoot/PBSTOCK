import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from functions.Login import logar
from view.pages.FRMlogin import Ui_login


class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_login()
        self.ui.setupUi(self)

        # Botão de logar no sistema
        self.ui.pushButton.clicked.connect(lambda: logar(self.ui, self))  # Passa 'self INTERFACE' e 'self' REF PARA FECHAR
        
        #Código para passar diretamente para as páginas, sem login necessário
        logar(self.ui,self)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Cria a aplicação
    janela = MinhaJanela()  # Cria a instância da janela
    janela.show()  # Exibe a janela
    sys.exit(app.exec_())  # Executa o loop da aplicação