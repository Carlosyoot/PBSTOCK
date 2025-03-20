from datetime import datetime
from functions.events.InterfaceError.popup import Popup, SucessPopup
from pycpfcnpj import cpfcnpj,gen
from functions.events.DabaseEvents.UpdateTables import AtualizaTabelasLogin, AtualizarTabelaEventos, AtualizarTabelaVendas, AtualizarTablesRecent
from functions.events.DabaseEvents.UpdateTables import AtualizarTabelasProdutos
from database.Datalogic import AdicionarEvento, AdicionarProdutosEvento, AdicionarUsuario, AdicionarProduto, AdicionarVenda, DecrementarEstoque, gerar_id_evento
from PyQt5.QtWidgets import QLineEdit
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores
from functions.events.searchs.ProdutoSearch import AtualizaCompleterSearchProdutos
import logging
from PyQt5.QtWidgets import QMessageBox, QPushButton

from functions.events.searchs.eventos import AtualizaCompleterSearchEventos
from functions.events.searchs.monitoramentoSearch import AtualizaCompleterSearchMonitoramento
from functions.events.searchs.vendas import AtualizaCompleterSearchVendas

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def CadastroUsuario(ui):

    Name = ui.line_nome.text().strip()
    User = ui.line_login.text().strip()
    Cpf = ui.line_cpf.text().strip()
    Birth = ui.line_data_nascimento.text().strip()
    Password = ui.line_senha.text().strip()
    AdminUser = ui.admin_button.isChecked()
    NormalUser = ui.colaborador_button.isChecked()

    missing_fields = [
        field for field, value in {
            'Nome': Name,
            'Login': User,
            'Data de Nascimento': Birth,
            'Senha': Password
        }.items() if not value
    ]

    if not AdminUser and not NormalUser:
        missing_fields.append('Tipo de Usuário (Admin ou Colaborador)')

    ResultCpf = CpfValidate(Cpf)
    if ResultCpf is not True:
        Popup("O Cpf digitado não\n é válido")
        return
        
        
    if missing_fields:
        Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{', '.join(missing_fields)}')
        return

    try:
        tipo_usuario = 'A' if AdminUser else 'C'

        response = AdicionarUsuario(Name, Birth, ResultCpf, User, Password, tipo_usuario)

        SucessPopup(response.get("message", "Cadastro realizado com sucesso!"))
        
        AtualizaTabelasLogin(ui)
        AtualizaCompleterSearchColaboradores(ui)

        ui.line_nome.clear()
        ui.line_login.clear()
        ui.line_cpf.clear()
        ui.line_data_nascimento.clear()
        ui.line_senha.clear()

        ui.admin_button.setChecked(False)
        ui.colaborador_button.setChecked(False)

    except Exception as e:
        Popup("Erro ao conectar ao servidor. Tente novamente mais tarde.")
        



def CadastroProduto(ui):

    Produto = ui.line_produto_cadastrar.text().strip()
    Cód = ui.line_codigo_produto_cadastrar.text().strip()
    Quantidade = ui.line_qtde_cadastrar.text().strip()
    Valor = ui.line_valor_cadastrar.text().strip()
    Descrição = ui.line_descricao_cadastrar.text().strip()
    missing_fields = [
        field for field, value in {
            'Nome': Produto,
            '\nCódigo': Cód,
            '\nQuantidade': Quantidade,
            '\nValor': Valor,
            '\nDescrição': Descrição
        }.items() if not value
    ]
    
    if missing_fields:
        Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{", ".join(missing_fields)}')
        return
    
    if len(Cód) < 5:
        Popup(f'Tamanho mínimo de 5 Dígitos no Código')
        return
    try:
        data = datetime.now()
        
        response = AdicionarProduto(Produto, Cód, Quantidade, Valor, Descrição,data)
        SucessPopup(response.get("message", "Cadastro realizado com sucesso!"))



        AtualizarTabelasProdutos(ui)
        AtualizaCompleterSearchProdutos(ui)
        AtualizarTablesRecent(ui)

        msg = QMessageBox()
        msg.setWindowTitle("Adicionar outro produto?")
        msg.setText("Deseja adicionar outro produto?")
        msg.setIcon(QMessageBox.Question)

        btn_sim = QPushButton("Sim")
        btn_nao = QPushButton("Não")
        msg.addButton(btn_sim, QMessageBox.YesRole)
        msg.addButton(btn_nao, QMessageBox.NoRole)

        msg.exec_()

        if msg.clickedButton() == btn_sim:
            ui.line_produto_cadastrar.clear()
            ui.line_codigo_produto_cadastrar.clear()
            ui.line_qtde_cadastrar.clear()
            ui.line_valor_cadastrar.clear()
            ui.line_descricao_cadastrar.clear()
        else:
            msg.close()
            ui.line_produto_cadastrar.clear()
            ui.line_codigo_produto_cadastrar.clear()
            ui.line_qtde_cadastrar.clear()
            ui.line_valor_cadastrar.clear()
            ui.line_descricao_cadastrar.clear()
            ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos)
            

    except Exception as e:
        logger.error(f"Erro ao conectar ao servidor: {e}", exc_info=True)
        Popup(f"Erro ao conectar ao servidor: {e}. Tente novamente mais tarde.")

def CadastroVenda(ui):
    Cód = ui.line_codigo_vendas.text().strip()
    Quantidade = ui.line_quantidade_vendas.text().strip()
    Vendedor = ui.line_colaborador_vendedor.text().strip()
    Data = ui.line_data_venda.text().strip()
    Horário = ui.line_data_horario.text().strip()
    Total = ui.line_total_venda.text().strip()

    TotalReplaced = Total.replace("R$:", "").strip()

    data_format = "%d/%m/%Y"  
    hora_format = "%H:%M"     

    missing_fields = [
        field for field, value in {
            'Código': Cód,
            'Quantidade': Quantidade,
            'Vendedor': Vendedor,
            'Data': Data,
            'Horário': Horário,
            'Total': Total
        }.items() if not value
    ]

    if missing_fields:
        Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{"    ".join(missing_fields)}')
        return

    try:
        datetime.strptime(Data, data_format)
        datetime.strptime(Horário, hora_format)
    except ValueError:
        Popup('A data ou Hora fornecida não está no formato correto (dd/mm/aaaa)-(HH:MM).')
        return

    HorárioCompleto = f"{Horário}:00"
    Timestamp = f"{Data} {HorárioCompleto}"

    try:
        ValorTotal = float(TotalReplaced)
    except ValueError:
        Popup('O valor total não é um número válido.')
        return

    if Cód.startswith("EVT"):
        ID_Produto_Evento = Cód  
        ID_Produto = None  

        resultado_estoque = DecrementarEstoque(Quantidade, ID_Produto_Evento, 'produto evento')
        if resultado_estoque == "Quantidade insuficiente em estoque.":
            Popup(resultado_estoque) 
            return 

        AdicionarVenda(
            Quantidade=Quantidade,
            Vendedor=Vendedor,
            Data=datetime.strptime(Timestamp, "%d/%m/%Y %H:%M:%S"),
            Valor_Total=ValorTotal,
            ID_Produto=ID_Produto,
            ID_Produto_Evento=ID_Produto_Evento
        )
        Popup('Venda cadastrada com sucesso!')
    else:
        ID_Produto = Cód  
        ID_Produto_Evento = None  

        resultado_estoque = DecrementarEstoque(Quantidade, ID_Produto, 'produto')
        if resultado_estoque == "Quantidade insuficiente em estoque.":
            Popup(resultado_estoque)  
            return 

        AdicionarVenda(
            Quantidade=Quantidade,
            Vendedor=Vendedor,
            Data=datetime.strptime(Timestamp, "%d/%m/%Y %H:%M:%S"),
            Valor_Total=ValorTotal,
            ID_Produto=ID_Produto,
            ID_Produto_Evento=ID_Produto_Evento
        )
        Popup('Venda cadastrada com sucesso!')
        AtualizaCompleterSearchMonitoramento(ui)
        

    try:
        AtualizarTabelaVendas(ui)
        AtualizaCompleterSearchVendas(ui)
        ui.line_codigo_vendas.clear()
        ui.line_quantidade_vendas.clear()
        ui.line_colaborador_vendedor.clear()
        ui.line_data_venda.clear()
        ui.line_data_horario.clear()
        ui.line_total_venda.clear()
    except Exception as e:
        Popup(f'Erro ao cadastrar venda: {e}')
        
        
def CadastrarEvento(ui):
    nome = ui.line_event_name.text().strip()
    datainicio = ui.line_data_event.text().strip()
    datafim = ui.line_dataend_event.text().strip()
    descricao = ui.line_descricao_event.text().strip()

    missing_fields = [
        field for field, value in {
            'Nome': nome,
            '\nData Inicio': datainicio,
            '\nData Fim': datafim,
            '\nDescrição': descricao
        }.items() if not value
    ]

    if missing_fields:
        Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{"    ".join(missing_fields)}')
        return

    try:
        data_inicio = datetime.strptime(datainicio, '%d/%m/%Y')
        data_fim = datetime.strptime(datafim, '%d/%m/%Y')
    except ValueError:
        Popup('Formato de data inválido. Use o formato DD/MM/AAAA.')
        return

    if data_inicio > data_fim:
        Popup('A data de início não pode ser maior que a data de fim.')
        return

    if not hasattr(ui, 'lista_produtos') or not ui.lista_produtos:
        Popup('Adicione pelo menos um produto ao evento.')
        return

    id_evento = gerar_id_evento()
    if not id_evento:
        Popup('Erro ao gerar ID do evento. Tente novamente.')
        return

    try:
        AdicionarEvento(id_evento, nome, data_inicio, data_fim, descricao)
        print('PRINT DO CADASTRO', id_evento, nome, data_inicio, data_fim, descricao)
    except Exception as e:
        print(f"Erro ao cadastrar evento: {e}")
        Popup('Erro ao cadastrar evento. Tente novamente.')
        return

    try:
        AdicionarProdutosEvento(id_evento, ui.lista_produtos)
        Popup('Evento e produtos cadastrados com sucesso!')
        AtualizarTabelaEventos(ui)
        AtualizaCompleterSearchProdutos(ui)
        
   
    except Exception as e:
        print(f"Erro ao cadastrar produtos: {e}")
        Popup('Erro ao cadastrar produtos. Verifique os dados.')
        
    
    AtualizaCompleterSearchEventos(ui)



        
def CpfValidate(cpf):
    digits = ''.join(filter(str.isdigit, cpf))

    if len(digits) != 11:
        return 'CPF deve ter 11 dígitos'
    is_valid = cpfcnpj.validate(digits)
    if not is_valid:
        return 'CPF inválido'

    print("O cpf é válido")
    return True  

def selecionar_admin(ui):
        print('entrou funcao admin')
        ui.admin_button.setChecked(True)
        ui.colaborador_button.setChecked(False)

def selecionar_colaborador(ui):
        print('entrou funcao colaborador')
        ui.admin_button.setChecked(False)
        ui.colaborador_button.setChecked(True)

def alternar_visibilidade_senha(ui):
    if ui.line_senha.echoMode() == QLineEdit.Normal:
        ui.line_senha.setEchoMode(QLineEdit.Password)
    
    else:
        ui.line_senha.setEchoMode(QLineEdit.Normal)
