from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from functions.events.DabaseEvents.UpdateTables import AtualizarTabelasProdutosStatus
from functions.events.InterfaceError.popup import Popup
from view.pages.filterbotao import Ui_Dialog  
from view.QRC import file_principal_rc  


class FiltroDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  

        self.filter_aplicar_btn.clicked.connect(self.aplicar_filtros)

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
            if self.parent():
                self.parent().atualizar_botoes_pesquisar(filtros)
        else:
            print("Nenhum filtro selecionado.")

        self.close() 


def FILTERPRODUTO(ui, parent_widget):

    def abrir_menu_filtro(ui):
        dialog = FiltroDialog(parent_widget) 
        dialog.exec_() 

    def atualizar_botoes_pesquisar(ui, filtros=None):

        try:
            if filtros is None:
                filtros = []
    
            AtualizarTabelasProdutosStatus(ui, filtros)
    
            def configurar_botao(botao, icone, funcao):
                botao.setIcon(QIcon(icone))  
                botao.setText("") 
                try:
                    botao.clicked.disconnect() 
                except TypeError:
                    pass  
                botao.clicked.connect(funcao) 
    
            if filtros:
                configurar_botao(ui.btn_pesquisar_produto, ":/icones/removefilter2.png", lambda: remover_filtros(ui))
                configurar_botao(ui.btn_pesquisar_alterar_produto, ":/icones/removefilter2.png", lambda: remover_filtros(ui))
            else:
                configurar_botao(ui.btn_pesquisar_produto, ":/icones/lupa.png", lambda: abrir_menu_filtro(ui))
                configurar_botao(ui.btn_pesquisar_alterar_produto, ":/icones/lupa.png", lambda: abrir_menu_filtro(ui))
    
        except Exception as e:
            print(f"Erro ao atualizar botões de pesquisa: {e}")
            Popup(f"Erro ao atualizar botões de pesquisa: {e}")

           

    def remover_filtros(ui):
        print("Filtros removidos.")
        atualizar_botoes_pesquisar(ui, [])  

    ui.btn_pesquisar_alterar_produto.clicked.connect(lambda: abrir_menu_filtro(ui)) 
    ui.btn_pesquisar_produto.clicked.connect(lambda: abrir_menu_filtro(ui))
    ui.OutStockButton.clicked.connect(lambda: (ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos), atualizar_botoes_pesquisar(ui, filtros=["Esgotado","Eventos"])))

    parent_widget.atualizar_botoes_pesquisar = lambda filtros: atualizar_botoes_pesquisar(ui, filtros)
