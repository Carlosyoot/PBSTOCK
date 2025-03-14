from datetime import datetime
from functions.events.InterfaceError.popup import Popup, SucessPopup
from pycpfcnpj import cpfcnpj,gen
from functions.events.DabaseEvents.UpdateTables import AtualizaTabelasLogin, AtualizarTablesRecent
from functions.events.DabaseEvents.UpdateTables import AtualizarTabelasProdutos
from database.Datalogic import AdicionarUsuario, AdicionarProduto
from PyQt5.QtWidgets import QLineEdit
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores
from functions.events.searchs.ProdutoSearch import AtualizaCompleterSearchProdutos
import logging
from PyQt5.QtWidgets import QMessageBox, QPushButton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def CadastroUsuario(ui):
    """
    Valida os dados do formulário e envia para o servidor.
    """
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
        ResultCpf = gen.cpf()

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
    """
    Valida os dados do formulário e envia para o servidor.
    """
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
    
    try:
        data = datetime.now()
        
        response = AdicionarProduto(Produto, Cód, Quantidade, Valor, Descrição,data)
        SucessPopup(response.get("message", "Cadastro realizado com sucesso!"))


        # Atualiza a tabela de recentes

        AtualizarTabelasProdutos(ui)
        AtualizaCompleterSearchProdutos(ui)
        AtualizarTablesRecent(ui)

        # Pergunta ao usuário se deseja adicionar outro produto
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
            

    except Exception as e:
        logger.error(f"Erro ao conectar ao servidor: {e}", exc_info=True)
        Popup(f"Erro ao conectar ao servidor: {e}. Tente novamente mais tarde.")

def CadastroVenda(ui):
    Cód = ui.line_codigo_vendas.text().strip()
    Quantidade = ui.line_quantidade_vendas.text().strip()
    Vendedor = ui.line_colaborador_vendedor.text().strip()
    Data = ui.line_data_venda.text().strip()
    
    missing_fields = [
            field for field, value in {
                'Código': Cód,
                '\nQuantidade': Quantidade,
                '\nVendedor': Vendedor,
                '\nData': Data
            }.items() if not value
        ]

    if missing_fields:
            Popup(f'Os seguintes campos estão faltando ou são inválidos:\n{"    ".join(missing_fields)}')
            return
        


        
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
        """Marca Admin e desmarca Colaborador"""
        print('entrou funcao admin')
        ui.admin_button.setChecked(True)
        ui.colaborador_button.setChecked(False)

def selecionar_colaborador(ui):
        """Marca Colaborador e desmarca Admin"""
        print('entrou funcao colaborador')
        ui.admin_button.setChecked(False)
        ui.colaborador_button.setChecked(True)

def alternar_visibilidade_senha(ui):
    # Verifica o modo atual do line_senha
    if ui.line_senha.echoMode() == QLineEdit.Normal:
        # Se estiver em modo normal, muda para modo de senha (ocultar)
        ui.line_senha.setEchoMode(QLineEdit.Password)
    
    else:
        # Se estiver em modo de senha, muda para modo normal (mostrar)
        ui.line_senha.setEchoMode(QLineEdit.Normal)
