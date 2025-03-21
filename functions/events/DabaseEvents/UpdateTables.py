from PyQt5.QtWidgets import QTableWidgetItem
from functions.events.CustomsWidgets.cardInit import UpdateFrames
from functions.events.InterfaceError.popup import Popup
import zmq
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from database.Datalogic import DataGetAllLogins, GetAllEventos, GetContagemProduto, GetProdutos, GetProdutosEvento, GetProdutosVendas, GetRecentsProduct
from functions.events.searchs.ProdutoSearch import AtualizaCompleterSearchProdutos
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores
import random
from datetime import datetime, timedelta
from functions.events.CustomsWidgets.ProductTable import UiTabelaProduto
from functions.events.searchs.eventos import AtualizaCompleterSearchEventos
from functions.events.searchs.monitoramentoSearch import AtualizaCompleterSearchMonitoramento
from functions.events.searchs.vendas import AtualizaCompleterSearchVendas




def InitializeTables(ui):
    
    AtualizarTabelasProdutos(ui)
    AtualizaTabelasLogin(ui)
    AtualizarTabelaVendas(ui)
    AtualizarTabelaEventos(ui)
    UiTabelaProduto.setup_table(ui)
    AtualizarTablesRecent(ui)
    AtualizaCompleterSearchColaboradores(ui)
    AtualizaCompleterSearchVendas(ui)
    AtualizaCompleterSearchProdutos(ui)
    AtualizaCompleterSearchEventos(ui)
    AtualizaCompleterSearchMonitoramento(ui)
    
    ui.listener = ZeroMQListener()
    ui.listener.notification_received.connect(lambda msg: atualizarInterface(ui, msg))
    ui.listener.start()


def AtualizarTabelasProdutos(ui):
    try: 
        banco_produtos = GetProdutos()
        
        
        ui.tabela_produto.clearContents()
        ui.tabela_alterar_produto.clearContents()

        ui.tabela_produto.setRowCount(len(banco_produtos))
        ui.tabela_alterar_produto.setRowCount(len(banco_produtos))

        for i, produto in enumerate(banco_produtos):
            # Tabela produto
            ui.tabela_produto.setItem(i, 0, QTableWidgetItem(str(produto[1]))) 
            ui.tabela_produto.setItem(i, 1, QTableWidgetItem(str(produto[2]))) 
            ui.tabela_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3]))) 
            ui.tabela_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4]))) 
            ui.tabela_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  
            ui.tabela_produto.setItem(i, 5, QTableWidgetItem(str(produto[6])))  

            item_produto = ui.tabela_produto.item(i, 0) 
            item_produto.setData(Qt.UserRole, produto[0]) 

            ui.tabela_alterar_produto.setItem(i, 0, QTableWidgetItem(str(produto[1])))  
            ui.tabela_alterar_produto.setItem(i, 1, QTableWidgetItem(str(produto[2])))  
            ui.tabela_alterar_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3]))) 
            ui.tabela_alterar_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4]))) 
            ui.tabela_alterar_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  

            item_alterar = ui.tabela_alterar_produto.item(i, 0)  
            item_alterar.setData(Qt.UserRole, produto[0])  
            
            UiTabelaProduto.Estilizar(ui)


    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de produtos: {e}")

        

def AtualizaTabelasLogin(ui):
    try:
        banco_login = DataGetAllLogins()
        

        if not banco_login:
            Popup("Erro ao buscar dados de login.")
            return
        
        if banco_login == ['vazio']:
            ui.tabela_colaboradores.clearContents()
            ui.tabela_alterar_colaboradores.clearContents()

            ui.tabela_colaboradores.setRowCount(0)
            ui.tabela_alterar_colaboradores.setRowCount(0)
            
            return

        ui.tabela_colaboradores.clearContents()
        ui.tabela_alterar_colaboradores.clearContents()

        row_count = len(banco_login)
        ui.tabela_colaboradores.setRowCount(row_count)
        ui.tabela_alterar_colaboradores.setRowCount(row_count)

        for i, produto in enumerate(banco_login):
            ui.tabela_colaboradores.setItem(i, 0, QTableWidgetItem(str(produto[1]))) 
            ui.tabela_colaboradores.setItem(i, 1, QTableWidgetItem(str(produto[4]))) 
            ui.tabela_colaboradores.setItem(i, 2, QTableWidgetItem(str(produto[2]))) 

            ui.tabela_alterar_colaboradores.setItem(i, 0, QTableWidgetItem(str(produto[1])))  
            ui.tabela_alterar_colaboradores.setItem(i, 1, QTableWidgetItem(str(produto[4])))  
            ui.tabela_alterar_colaboradores.setItem(i, 2, QTableWidgetItem(str(produto[5])))  
            ui.tabela_alterar_colaboradores.setItem(i, 3, QTableWidgetItem(str(produto[2])))  
            ui.tabela_alterar_colaboradores.setItem(i, 4, QTableWidgetItem(str(produto[3])))  

            item = ui.tabela_alterar_colaboradores.item(i, 0)  
            item.setData(Qt.UserRole, produto[0])  
    except Exception as e:
        print(f"Erro ao atualizar tabelas: {e}")
        Popup("Erro ao atualizar tabelas. Tente novamente mais tarde.")
        
def AtualizarTablesRecent(ui):
    banco_recentes = GetRecentsProduct()
    
    
    try:
        

        ui.tabela_cadastro.clearContents()
        ui.tabela_cadastro.setRowCount(len(banco_recentes))

        for i, produto in enumerate(banco_recentes):
            ui.tabela_cadastro.setItem(i, 0, QTableWidgetItem(str(produto[0]))) 
            ui.tabela_cadastro.setItem(i, 1, QTableWidgetItem(str(produto[1]))) 
            ui.tabela_cadastro.setItem(i, 2, NumericTableWidgetItem(str(produto[2])))  
            ui.tabela_cadastro.setItem(i, 3, NumericTableWidgetItem(str(produto[3])))  
            ui.tabela_cadastro.setItem(i, 4, QTableWidgetItem(str(produto[4]))) 
            ui.tabela_cadastro.setItem(i, 5, QTableWidgetItem(str(produto[5]))) 


    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de recentes: {e}")

def AtualizarTabelaVendas(ui):

    try:
        vendas = GetProdutosVendas()

        ui.tabela_vendas.clearContents()
        ui.tabela_vendas.setRowCount(len(vendas))

        for i, venda in enumerate(vendas):

            ui.tabela_vendas.setItem(i, 0, QTableWidgetItem(str(venda[0]))) 
            ui.tabela_vendas.setItem(i, 1, QTableWidgetItem(str(venda[1]))) 
            ui.tabela_vendas.setItem(i, 2, QTableWidgetItem(str(venda[2]))) 
            ui.tabela_vendas.setItem(i, 3, QTableWidgetItem(str(venda[3]))) 
            ui.tabela_vendas.setItem(i, 4, QTableWidgetItem(str(venda[4]))) 
            
        preencher_tabela_monitoramento(ui)

    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de vendas: {e}")
        
def AtualizarTabelaEventos(ui):

    try:
        eventos = GetAllEventos()

        ui.tabela_evento.clearContents()
        ui.tabela_evento.setRowCount(len(eventos))

        for i, evento in enumerate(eventos):
            id_evento = evento[0] 

            contagem_produtos = GetContagemProduto(id_evento)

            data_inicio = datetime.strptime(str(evento[2]), '%Y-%m-%d').strftime('%d-%m-%Y')
            data_fim = datetime.strptime(str(evento[3]), '%Y-%m-%d').strftime('%d-%m-%Y')

            # Preenche as colunas da tabela
            ui.tabela_evento.setItem(i, 0, QTableWidgetItem(str(evento[0])))  
            ui.tabela_evento.setItem(i, 1, QTableWidgetItem(str(evento[1])))  
            ui.tabela_evento.setItem(i, 2, QTableWidgetItem(data_inicio))     
            ui.tabela_evento.setItem(i, 3, QTableWidgetItem(data_fim))      
            ui.tabela_evento.setItem(i, 4, QTableWidgetItem(str(contagem_produtos))) 
            ui.tabela_evento.setItem(i, 5, QTableWidgetItem(str(evento[4])))  
        preencher_tabela_monitoramento(ui)

    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de eventos: {e}")

def preencher_tabela_monitoramento(ui):

    try:
                
        vendas = GetProdutosVendas()
        
        ui.tabela_monitoramento.clearContents()
        ui.tabela_monitoramento.setRowCount(len(vendas))


        for i, venda in enumerate(vendas):
           
            

            
            dia = venda[3].strftime('%d/%m/%Y') 
            hora = venda[3].strftime('%H:%M')   
            

            valor_total_formatado = f"R$ {float(venda[4]):.2f}"
            valor_un_formatado = f"R$ {float(venda[5]):.2f}"

            # Insere os itens na tabela
            ui.tabela_monitoramento.setItem(i, 0, QTableWidgetItem(str(venda[2]))) 
            ui.tabela_monitoramento.setItem(i, 1, QTableWidgetItem(str(venda[0])))  
            ui.tabela_monitoramento.setItem(i, 2, QTableWidgetItem(str(venda[1])))  
            ui.tabela_monitoramento.setItem(i, 3, QTableWidgetItem(str(valor_un_formatado)))  
            ui.tabela_monitoramento.setItem(i, 4, QTableWidgetItem(str(dia)))  
            ui.tabela_monitoramento.setItem(i, 5, QTableWidgetItem(str(hora))) 
            ui.tabela_monitoramento.setItem(i, 6, QTableWidgetItem(str(valor_total_formatado)))  


    except Exception as e:
        print(f"Erro ao preencher a tabela de monitoramento: {e}")


contador_atualizar_interface = 0

def atualizarInterface(ui, msg):
    global contador_atualizar_interface
    print(f"Mudança observada: {msg}")
    
    try:
        if ':' in msg:
            tipo_mudanca, descricao = msg.split(':', 1)
        else:
            print(f"Mensagem recebida sem formato esperado: {msg}")
            return
        
        contador_atualizar_interface += 1

        if 'produto' in descricao:  
            AtualizarTabelasProdutos(ui)
            AtualizaCompleterSearchProdutos(ui)
            print("Mudança na tabela produto, atualizando...")
        
        elif 'usuarios' in descricao: 
            AtualizaTabelasLogin(ui)
            AtualizaCompleterSearchColaboradores(ui)
            print("Mudança na tabela usuários, atualizando...")
            
        elif 'cards' in descricao:
            UpdateFrames(ui)
            print("Mudança nos card iniciais.....")
            
        elif 'evento' in descricao:
            AtualizarTabelaEventos(ui)
            AtualizaCompleterSearchEventos(ui)
            

        if tipo_mudanca == "RENOVACAO_LOG":
            AtualizaTabelasLogin(ui)
            AtualizaCompleterSearchColaboradores(ui)
            AtualizarTabelasProdutos(ui)
            AtualizaCompleterSearchProdutos(ui)
            print("RENOVAÇÃO DE LINHA")
        
        if contador_atualizar_interface >= 5:
            print("Executando InitializeTables para garantir consistência...")
            AtualizarTabelasProdutos(ui)
            AtualizaTabelasLogin(ui)
            AtualizarTabelaVendas(ui)
            AtualizarTabelaEventos(ui)
            UiTabelaProduto.setup_table(ui)
            AtualizarTablesRecent(ui)
            AtualizaCompleterSearchColaboradores(ui)
            AtualizaCompleterSearchVendas(ui)
            AtualizaCompleterSearchProdutos(ui)
            AtualizaCompleterSearchEventos(ui)
            AtualizaCompleterSearchMonitoramento(ui)
            contador_atualizar_interface = 0  # Reinicia o contador
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def AtualizarTabelasProdutosStatus(ui, status_filtro=None):

    try:
        if status_filtro and 'Eventos' in status_filtro:
            banco_produtos_evento = list(GetProdutosEvento())  
            banco_produtos_normal = list(GetProdutos())  
            banco_produtos = banco_produtos_evento + banco_produtos_normal 
        else:
            banco_produtos = list(GetProdutos())  

        if not banco_produtos:
            print("Nenhum produto encontrado.")
            return

        if status_filtro:
            filtro_status = [status for status in status_filtro if status != 'Eventos']
            
            if filtro_status: 
                banco_produtos = [produto for produto in banco_produtos if produto[6] in filtro_status]

        ui.tabela_produto.clearContents()
        ui.tabela_produto.setRowCount(len(banco_produtos))
        ui.tabela_alterar_produto.clearContents()
        ui.tabela_alterar_produto.setRowCount(len(banco_produtos))

        for i, produto in enumerate(banco_produtos):
            # Tabela produto
            ui.tabela_produto.setItem(i, 0, QTableWidgetItem(str(produto[1])))  
            ui.tabela_produto.setItem(i, 1, QTableWidgetItem(str(produto[2])))  
            ui.tabela_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3]))) 
            ui.tabela_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4]))) 
            ui.tabela_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))
            ui.tabela_produto.setItem(i, 5, QTableWidgetItem(str(produto[6])))

            item_produto = ui.tabela_produto.item(i, 0)  
            item_produto.setData(Qt.UserRole, produto[0])
            
        for i, produto in enumerate(banco_produtos):
            # Tabela produto
            ui.tabela_alterar_produto.setItem(i, 0, QTableWidgetItem(str(produto[1]))) 
            ui.tabela_alterar_produto.setItem(i, 1, QTableWidgetItem(str(produto[2]))) 
            ui.tabela_alterar_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3]))) 
            ui.tabela_alterar_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4]))) 
            ui.tabela_alterar_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  
            ui.tabela_alterar_produto.setItem(i, 5, QTableWidgetItem(str(produto[6])))  

            item_produto = ui.tabela_alterar_produto.item(i, 0) 
            item_produto.setData(Qt.UserRole, produto[0])  

        UiTabelaProduto.Estilizar(ui)

    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de produtos status: {e}")
        

    

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)
        
class ZeroMQListener(QThread):
    notification_received = pyqtSignal(str)  

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB) 
        socket.connect("tcp://localhost:5555") 
        socket.setsockopt_string(zmq.SUBSCRIBE, "")  

        print("Assinante iniciado. Recebendo notificações...")
        while True:
            mensagem = socket.recv_string()  
            self.notification_received.emit(mensagem)  