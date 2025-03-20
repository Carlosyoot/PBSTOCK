from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QPixmap


def Popup(missing_fields):
    msg = QMessageBox()
    msg.setWindowTitle("Aviso")
    msg.setText(f'{missing_fields}')
    icon = QIcon()
    icon.addPixmap(QPixmap("view/QRC/alerticon.png"), QIcon.Normal, QIcon.Off)
    msg.setWindowIcon(icon)
    x = msg.exec_()
    
def SucessPopup(missing_fields):
    msg = QMessageBox()
    msg.setWindowTitle("Sucesso - Operação realizada com sucesso")
    msg.setText(f'{missing_fields}')
    icon = QIcon()
    icon.addPixmap(QPixmap("view/QRC/alerticon.png"), QIcon.Normal, QIcon.Off)
    msg.setWindowIcon(icon)
    x = msg.exec_()

        
def PopupXlsDiretorio(self):
        msg = QMessageBox()
        msg.setWindowTitle("Erro - Gerar Excel")
        msg.setText('Selecione um diretório válido!')

        icon = QIcon()
        icon.addPixmap(QPixmap("view/QRC/alerticon.png"), QIcon.Normal, QIcon.Off)
        msg.setWindowIcon(icon)
        x = msg.exec_()

def PopupXls(self):
        msg = QMessageBox()
        msg.setWindowTitle("Erro - Gerar Excel")
        msg.setText('Verifique se não há um ARQUIVO com o mesmo nome aberto!')

        icon = QIcon()
        icon.addPixmap(QPixmap("view/QRC/alerticon.png"), QIcon.Normal, QIcon.Off)
        msg.setWindowIcon(icon)
        x = msg.exec_()

def PoupXlsBancoVazio(self):
        msg = QMessageBox()
        msg.setWindowTitle("Erro - Gerar Excel")
        msg.setText('Nenhuma venda informada!')

        icon = QIcon()
        icon.addPixmap(QPixmap("view/QRC/alerticon.png"), QIcon.Normal, QIcon.Off)
        msg.setWindowIcon(icon)
        x = msg.exec_()
