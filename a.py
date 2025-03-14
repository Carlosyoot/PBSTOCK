import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

class LoadingScreen(QMainWindow):
    def __init__(self, gif_path):
        super().__init__()

        # Configura a janela de carregamento
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Fundo transparente (opcional)

        # Cria um QLabel para exibir o GIF
        self.label = QLabel(self)
        self.movie = QMovie(gif_path)
        self.label.setMovie(self.movie)

        # Define o tamanho do GIF (opcional)
        self.movie.setScaledSize(QtCore.QSize(200, 150))  # Redimensiona o GIF para 400x300 pixels

        # Centraliza o QLabel na janela
        self.setCentralWidget(self.label)

        # Redimensiona a janela para o tamanho do GIF
        self.resize(self.movie.scaledSize())

        # Inicia a animação do GIF
        self.movie.start()

        # Centraliza a janela na tela
        self.center_window()

    def center_window(self):
        # Obtém a geometria da tela atual usando QScreen
        screen_geometry = QApplication.primaryScreen().geometry()

        # Print para exibir o tamanho da tela
        print(f"Tamanho da tela: largura = {screen_geometry.width()}, altura = {screen_geometry.height()}")

        # Calcula a posição central considerando o tamanho atual da janela
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        
        # Print para mostrar a posição calculada para a janela
        print(f"Posição calculada para a janela: x = {x}, y = {y}")

        # Move a janela para o centro
        self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Exibe a tela de carregamento
    splash = LoadingScreen("GIFLOAD.gif")  # Substitua pelo caminho do seu GIF
    splash.show()

    # Mantém a janela aberta até que o processo seja finalizado
    sys.exit(app.exec_())
