from database.Datalogic import DeleteUsers, DeleteProduto
from functions.events.InterfaceError.popup import Popup
from functions.events.DabaseEvents.UpdateTables import AtualizaTabelasLogin, AtualizarTabelasProdutos, AtualizarTablesRecent
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores
from functions.events.searchs.ProdutoSearch import AtualizaCompleterSearchProdutos
from PyQt5.QtCore import Qt


def ExcluirColaboradores(ui):
    row = ui.tabela_colaboradores.currentRow()
        
    if row == -1:
        Popup("Por favor, selecione um usuário para excluir.")
        return
    
    Nome = ui.tabela_colaboradores.item(row, 0).text() 
    Login = ui.tabela_colaboradores.item(row, 1).text()  
    
    try:

        print('excluindo', Nome, Login)
        DeleteUsers(Nome, Login)
        
        AtualizaTabelasLogin(ui)
        AtualizaCompleterSearchColaboradores(ui)
    
    except Exception as e:
        Popup(f"Erro ao excluir o usuário: {e}")
        
def ExcluirProdutos(ui):
    row = ui.tabela_produto.currentRow()
        
    if row == -1:
        Popup("Por favor, selecione um usuário para excluir.")
        return
    
    Produto = ui.tabela_produto.item(row, 0).text() 
    id_produto = ui.tabela_produto.item(row, 0).data(Qt.UserRole)  


    try:

        DeleteProduto(Produto, id_produto)
    
        AtualizarTabelasProdutos(ui)
        AtualizaCompleterSearchProdutos(ui)
        AtualizarTablesRecent(ui)
    
    except Exception as e:
        Popup(f"Erro ao excluir o usuário: {e}")


     