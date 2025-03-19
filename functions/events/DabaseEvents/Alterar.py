
from database.Datalogic import AlterarProdutoEvento, AlterarUsuario, AlterarProduto, VerificarSeProdutoEhEvento
from functions.events.InterfaceError.popup import Popup, SucessPopup
from functions.events.DabaseEvents.UpdateTables import AtualizaTabelasLogin, AtualizarTabelasProdutos
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores



def AlterarColaboradores(ui):
    Nome = ui.line_nome_alterar_colaboradores.text()
    DataNasc = ui.line_datanasc_alterar_colaboradores.text()
    Login = ui.line_login_alterar_colaboradores.text()
    Senha = ui.line_senha_alterar_colaboradores.text()
    Cpf = ui.line_cpf_alterar_colaboradores.text()
    
    missing_fields = [
        field for field, value in {
            'Nome': Nome,
            'Login': Login,
            'Data de Nascimento': DataNasc,
            'Senha': Senha
        }.items() if not value
    ]
        
    if not hasattr(ui, 'IDUSERNAME') or not ui.IDUSERNAME:
        Popup("Erro: Nenhum colaborador selecionado.")
        return

    Oldusername = ui.IDUSERNAME
    
    if missing_fields:
        Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{', '.join(missing_fields)}')
        return

    
        
    # Chama a função para atualizar o usuário no banco de dados
    response = AlterarUsuario(Oldusername, Nome, DataNasc, Login, Senha, Cpf)
    SucessPopup(response.get("message", "Cadastro realizado com sucesso!"))
    
    AtualizaTabelasLogin(ui)
    AtualizaCompleterSearchColaboradores(ui)

    
    
    ui.line_nome_alterar_colaboradores.clear()
    ui.line_datanasc_alterar_colaboradores.clear()
    ui.line_login_alterar_colaboradores.clear()
    ui.line_senha_alterar_colaboradores.clear()
    ui.line_cpf_alterar_colaboradores.clear()
    
def AlterarProdutos(ui):
    Nome = ui.line_nome_alterar_produto.text()
    Quantidade = ui.line_qtde_alterar_produto.text()
    Valor = ui.line_valor_alterar_produto.text()
    Descrição = ui.line_decricao_alterar_produto.text()
    
    missing_fields = [
        field for field, value in {
            'Nome': Nome,
            'Quantidade': Quantidade,
            'Valor': Valor,
            'Descrição': Descrição
        }.items() if not value
    ]
    
    if not hasattr(ui, 'IDPRODUTO') or not ui.IDPRODUTO:
        Popup("Erro: Nenhum produto selecionado.")
        return
    
    Id = ui.IDPRODUTO
    
    if missing_fields:
        Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{", ".join(missing_fields)}')
        return

    try:
        # Verifica se o produto é de um evento
        if VerificarSeProdutoEhEvento(Id):
            # Se for um produto de evento, chama a função de alteração de produto de evento
            response = AlterarProdutoEvento(Id, Nome, Quantidade, Valor, Descrição)
        else:
            # Se não for um produto de evento, chama a função de alteração de produto normal
            response = AlterarProduto(Id, Nome, Quantidade, Valor, Descrição)
        
        SucessPopup(response.get("message", "Cadastro realizado com sucesso!"))
        
        AtualizarTabelasProdutos(ui)
        
        ui.line_nome_alterar_produto.clear()
        ui.line_qtde_alterar_produto.clear()
        ui.line_valor_alterar_produto.clear()
        ui.line_decricao_alterar_produto.clear()
    except Exception as e:
        print(f"Erro ao conectar ao servidor {e}. Tente novamente mais tarde.")