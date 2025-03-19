from database.Datalogic import DeleteUsers, DeleteProduto
from functions.events.InterfaceError.popup import Popup
from functions.events.DabaseEvents.UpdateTables import AtualizaTabelasLogin, AtualizarTabelasProdutos, AtualizarTablesRecent
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores
from functions.events.searchs.ProdutoSearch import AtualizaCompleterSearchProdutos
from PyQt5.QtCore import Qt


def ExcluirColaboradores(ui):
    # Obtém o índice da linha selecionada
    row = ui.tabela_colaboradores.currentRow()
        
    if row == -1:
        # Nenhuma linha selecionada
        Popup("Por favor, selecione um usuário para excluir.")
        return
    
    Nome = ui.tabela_colaboradores.item(row, 0).text()  # Primeira coluna (Nome)
    Login = ui.tabela_colaboradores.item(row, 1).text()  # Segunda coluna (Login)
    
    try:

        print('excluindo', Nome, Login)
        DeleteUsers(Nome, Login)
        
        # Atualiza a tabela após exclusão
        AtualizaTabelasLogin(ui)
        AtualizaCompleterSearchColaboradores(ui)
    
    except Exception as e:
        # Em caso de erro, exibe uma mensagem de erro
        Popup(f"Erro ao excluir o usuário: {e}")
        
def ExcluirProdutos(ui):
    # Obtém o índice da linha selecionada
    row = ui.tabela_produto.currentRow()
        
    if row == -1:
        # Nenhuma linha selecionada
        Popup("Por favor, selecione um usuário para excluir.")
        return
    
    Produto = ui.tabela_produto.item(row, 0).text()  # Primeira coluna (Nome)
    id_produto = ui.tabela_produto.item(row, 0).data(Qt.UserRole)  #


    try:

        DeleteProduto(Produto, id_produto)
    
        AtualizarTabelasProdutos(ui)
        AtualizaCompleterSearchProdutos(ui)
        AtualizarTablesRecent(ui)
    
    except Exception as e:
        # Em caso de erro, exibe uma mensagem de erro
        Popup(f"Erro ao excluir o usuário: {e}")

#
        #self.AtualizaTabelasLogin()
        #self.AtualizaCompleterSearchColaboradores()