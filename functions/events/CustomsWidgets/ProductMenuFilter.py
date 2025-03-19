from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from functions.events.DabaseEvents.UpdateTables import AtualizarTabelasProdutosStatus
from view.pages.filterbotao import Ui_Dialog  # Importando a classe gerada do arquivo .ui
from view.QRC import file_principal_rc  # Importando o arquivo de recursos


class FiltroDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Inicializa a interface gerada pela classe Ui_Dialog

        # Conectar o botão "Aplicar" à função aplicar_filtros
        self.filter_aplicar_btn.clicked.connect(self.aplicar_filtros)

        # Definir o foco no botão "Aplicar"
        self.filter_aplicar_btn.setFocus()

    def aplicar_filtros(self):
        """Aplica os filtros e fecha o diálogo."""
        filtros = []
        if self.checkbox_esgotado.isChecked():
            filtros.append("Esgotado")
        if self.checkbox_ativos.isChecked():
            filtros.append("Ativo")
        if self.checkbox_pausados.isChecked():
            filtros.append("Pausado")
        if self.checkbox_eventos.isChecked():
            filtros.append("Eventos")

        if filtros: 
            print("Filtros aplicados:", filtros)
            # Atualiza os botões no parent (MainWindow)
            if self.parent():
                self.parent().atualizar_botoes_pesquisar(filtros)
        else:
            print("Nenhum filtro selecionado.")

        self.close()  # Fecha o diálogo após aplicar os filtros


def FILTERPRODUTO(ui, parent_widget):
    """
    Configura os botões de pesquisa para abrir a janela de filtro e atualizar os ícones.

    Args:
        ui: A interface gerada pelo pyuic5 (por exemplo, Ui_FrmAdmin).
        parent_widget: O widget pai (por exemplo, a janela principal ou o widget que contém os botões).
    """
    def abrir_menu_filtro(ui):
        """Abre o diálogo de filtros."""
        dialog = FiltroDialog(parent_widget)  # Passa o widget pai como parent para o diálogo
        dialog.exec_()  # Exibe o diálogo de forma modal

    def atualizar_botoes_pesquisar(ui, filtros):
        """Atualiza o visual dos botões com base nos filtros aplicados."""
        AtualizarTabelasProdutosStatus(ui, filtros)

        if filtros:
            # Atualiza o botão "btn_pesquisar_produto"
            ui.btn_pesquisar_produto.setIcon(QIcon(":/icones/removefilter2.png"))  # Adiciona um ícone de "X"
            ui.btn_pesquisar_produto.setText("")  # Limpa o texto, deixando apenas o ícone

            # Evitar múltiplas conexões ao botão
            try:
                ui.btn_pesquisar_produto.clicked.disconnect()  # Remove conexões anteriores
            except TypeError:
                pass  # Se já estiver desconectado, ignora o erro

            ui.btn_pesquisar_produto.clicked.connect(lambda: remover_filtros(ui))  # Conecta à função de remover filtros

            # Atualiza o botão "btn_pesquisar_alterar_produto"
            ui.btn_pesquisar_alterar_produto.setIcon(QIcon(":/icones/removefilter2.png"))  # Adiciona um ícone de "X"
            ui.btn_pesquisar_alterar_produto.setText("")  # Limpa o texto, deixando apenas o ícone

            # Evitar múltiplas conexões ao botão
            try:
                ui.btn_pesquisar_alterar_produto.clicked.disconnect()  # Remove conexões anteriores
            except TypeError:
                pass  # Se já estiver desconectado, ignora o erro

            ui.btn_pesquisar_alterar_produto.clicked.connect(lambda: remover_filtros(ui))  # Conecta à função de remover filtros
        else:
            # Restaura o ícone da lupa no botão "btn_pesquisar_produto"
            ui.btn_pesquisar_produto.setIcon(QIcon(":/icones/lupa.png"))  # Caminho do ícone no arquivo .qrc
            ui.btn_pesquisar_produto.setText("")  # Limpa o texto, deixando apenas o ícone

            # Evitar múltiplas conexões ao botão
            try:
                ui.btn_pesquisar_produto.clicked.disconnect()  # Remove conexões anteriores
            except TypeError:
                pass  # Se já estiver desconectado, ignora o erro

            ui.btn_pesquisar_produto.clicked.connect(lambda: abrir_menu_filtro(ui))  # Conecta à função de abrir filtro

            # Restaura o ícone da lupa no botão "btn_pesquisar_alterar_produto"
            ui.btn_pesquisar_alterar_produto.setIcon(QIcon(":/icones/lupa.png"))  # Caminho do ícone no arquivo .qrc
            ui.btn_pesquisar_alterar_produto.setText("")  # Limpa o texto, deixando apenas o ícone

            # Evitar múltiplas conexões ao botão
            try:
                ui.btn_pesquisar_alterar_produto.clicked.disconnect()  # Remove conexões anteriores
            except TypeError:
                pass  # Se já estiver desconectado, ignora o erro

           

    def remover_filtros(ui):
        """Remove os filtros e restaura os botões ao estado original."""
        print("Filtros removidos.")
        atualizar_botoes_pesquisar(ui, [])  # Atualiza os botões para o estado original

    # Conectar os botões à função abrir_menu_filtro
    ui.btn_pesquisar_alterar_produto.clicked.connect(lambda: abrir_menu_filtro(ui))  # Conecta à função de abrir filtro
    ui.btn_pesquisar_produto.clicked.connect(lambda: abrir_menu_filtro(ui))
    ui.OutStockButton.clicked.connect(lambda: (ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos), atualizar_botoes_pesquisar(ui, filtros=["Esgotado","Eventos"])))

    # Adicionar o método atualizar_botoes_pesquisar ao widget pai
    parent_widget.atualizar_botoes_pesquisar = lambda filtros: atualizar_botoes_pesquisar(ui, filtros)
