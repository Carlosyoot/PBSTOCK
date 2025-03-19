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
    
    #ui.listener = ZeroMQListener()
    #ui.listener.notification_received.connect(lambda msg: atualizarInterface(ui, msg))
    #ui.listener.start()


def AtualizarTabelasProdutos(ui):
    try: 
        banco_produtos = GetProdutos()
        
        #if not banco_produtos:
        #    print("Nenhum produto encontrado")
        #    return
        
        # Limpar tabela antes de adicionar novos dados
        ui.tabela_produto.clearContents()
        ui.tabela_alterar_produto.clearContents()

        # Definir o número de linhas da tabela de acordo com o número de produtos
        ui.tabela_produto.setRowCount(len(banco_produtos))
        ui.tabela_alterar_produto.setRowCount(len(banco_produtos))

        # Preencher as células com os dados dos produtos
        for i, produto in enumerate(banco_produtos):
            # Tabela produto
            ui.tabela_produto.setItem(i, 0, QTableWidgetItem(str(produto[1])))  # Produto
            ui.tabela_produto.setItem(i, 1, QTableWidgetItem(str(produto[2])))  # Cód
            ui.tabela_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3])))  # Quantidade
            ui.tabela_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4])))  # ValorUn
            ui.tabela_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  # Descrição
            ui.tabela_produto.setItem(i, 5, QTableWidgetItem(str(produto[6])))  # Condição

            # Armazenando o ID na tabela produto
            item_produto = ui.tabela_produto.item(i, 0)  # Aqui, o ID é armazenado no primeiro item da coluna
            item_produto.setData(Qt.UserRole, produto[0])  # Armazenando o ID na propriedade UserRole (assumindo que o ID é produto[0])

            # Tabela alterar produto
            ui.tabela_alterar_produto.setItem(i, 0, QTableWidgetItem(str(produto[1])))  # Produto
            ui.tabela_alterar_produto.setItem(i, 1, QTableWidgetItem(str(produto[2])))  # Cód
            ui.tabela_alterar_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3])))  # Quantidade
            ui.tabela_alterar_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4])))  # ValorUn
            ui.tabela_alterar_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  # Descrição

            # Armazenando o ID na tabela alterar_produto
            item_alterar = ui.tabela_alterar_produto.item(i, 0)  # Aqui, o ID é armazenado no primeiro item da coluna
            item_alterar.setData(Qt.UserRole, produto[0])  # Armazenando o ID na propriedade UserRole (assumindo que o ID é produto[0])
            
            UiTabelaProduto.Estilizar(ui)


    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de produtos: {e}")

        

def AtualizaTabelasLogin(ui):
    try:
        #DataGetAllLogins() retorne uma lista de tuplas ou listas
        banco_login = DataGetAllLogins()
        

        if not banco_login:
            Popup("Erro ao buscar dados de login.")
            return
        
        if banco_login == ['vazio']:
            ui.tabela_colaboradores.clearContents()
            ui.tabela_alterar_colaboradores.clearContents()

            # Define o número de linhas como 0 para deixar as tabelas vazias
            ui.tabela_colaboradores.setRowCount(0)
            ui.tabela_alterar_colaboradores.setRowCount(0)
            
            return

        # Limpa as tabelas
        ui.tabela_colaboradores.clearContents()
        ui.tabela_alterar_colaboradores.clearContents()

        # Define o número de linhas para a tabela
        row_count = len(banco_login)
        ui.tabela_colaboradores.setRowCount(row_count)
        ui.tabela_alterar_colaboradores.setRowCount(row_count)

        for i, produto in enumerate(banco_login):
            # Preenchendo a tabela de colaboradores
            ui.tabela_colaboradores.setItem(i, 0, QTableWidgetItem(str(produto[1])))  # Nome
            ui.tabela_colaboradores.setItem(i, 1, QTableWidgetItem(str(produto[4])))  # Login
            ui.tabela_colaboradores.setItem(i, 2, QTableWidgetItem(str(produto[2])))  # Senha/Nascimento

            # Preenchendo a tabela de alterar colaboradores
            ui.tabela_alterar_colaboradores.setItem(i, 0, QTableWidgetItem(str(produto[1])))  # Nome
            ui.tabela_alterar_colaboradores.setItem(i, 1, QTableWidgetItem(str(produto[4])))  # Login
            ui.tabela_alterar_colaboradores.setItem(i, 2, QTableWidgetItem(str(produto[5])))  # Senha
            ui.tabela_alterar_colaboradores.setItem(i, 3, QTableWidgetItem(str(produto[2])))  # Data Nasc
            ui.tabela_alterar_colaboradores.setItem(i, 4, QTableWidgetItem(str(produto[3])))  # CPF

            # Salva o ID usando Qt.UserRole (assumindo que o ID é o primeiro item da tupla)
            item = ui.tabela_alterar_colaboradores.item(i, 0)  # Aqui, o ID é armazenado no primeiro item da coluna
            item.setData(Qt.UserRole, produto[0])  # Armazenando o ID na propriedade UserRole (assumindo que o ID é produto[0])

    except Exception as e:
        print(f"Erro ao atualizar tabelas: {e}")
        Popup("Erro ao atualizar tabelas. Tente novamente mais tarde.")
        
def AtualizarTablesRecent(ui):
    """
    Atualiza a tabela de produtos recentes com base na lista global recent_products.
    """
    banco_recentes = GetRecentsProduct()
    
    
    try:
        

        # Limpa a tabela de recentes
        ui.tabela_cadastro.clearContents()
        ui.tabela_cadastro.setRowCount(len(banco_recentes))

        # Preenche a tabela com os produtos recentes
        for i, produto in enumerate(banco_recentes):
            ui.tabela_cadastro.setItem(i, 0, QTableWidgetItem(str(produto[0])))  # Produto
            ui.tabela_cadastro.setItem(i, 1, QTableWidgetItem(str(produto[1])))  # Cód
            ui.tabela_cadastro.setItem(i, 2, NumericTableWidgetItem(str(produto[2])))  # Quantidade
            ui.tabela_cadastro.setItem(i, 3, NumericTableWidgetItem(str(produto[3])))  # ValorUn
            ui.tabela_cadastro.setItem(i, 4, QTableWidgetItem(str(produto[4])))  # Descrição
            ui.tabela_cadastro.setItem(i, 5, QTableWidgetItem(str(produto[5])))  # Data


    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de recentes: {e}")

def AtualizarTabelaVendas(ui):
    """
    Atualiza a tabela de vendas com base nos dados retornados por GetProdutosVendas.
    """
    try:
        # Obtém os dados das vendas
        vendas = GetProdutosVendas()

        # Limpa a tabela de vendas
        ui.tabela_vendas.clearContents()
        ui.tabela_vendas.setRowCount(len(vendas))

        # Preenche a tabela com os dados das vendas
        for i, venda in enumerate(vendas):
            # Extrai os dados da tupla usando índices

            # Preenche as colunas da tabela
            ui.tabela_vendas.setItem(i, 0, QTableWidgetItem(str(venda[0])))  # Produto
            ui.tabela_vendas.setItem(i, 1, QTableWidgetItem(str(venda[1])))  # Quantidade_vendida
            ui.tabela_vendas.setItem(i, 2, QTableWidgetItem(str(venda[2])))  # Vendedor
            ui.tabela_vendas.setItem(i, 3, QTableWidgetItem(str(venda[3])))  # Data
            ui.tabela_vendas.setItem(i, 4, QTableWidgetItem(str(venda[4])))  # Valor_total
            
        preencher_tabela_monitoramento(ui)

    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de vendas: {e}")
        
def AtualizarTabelaEventos(ui):
    """
    Atualiza a tabela de eventos com base nos dados retornados por GetAllEventos.
    As datas são formatadas no formato dd-mm-yyyy.
    """
    try:
        # Obtém os dados dos eventos
        eventos = GetAllEventos()

        # Limpa a tabela de eventos
        ui.tabela_evento.clearContents()
        ui.tabela_evento.setRowCount(len(eventos))

        # Preenche a tabela com os dados dos eventos
        for i, evento in enumerate(eventos):
            id_evento = evento[0]  # ID do evento

            # Obtém a contagem de produtos associados ao evento
            contagem_produtos = GetContagemProduto(id_evento)

            # Formata as datas no formato dd-mm-yyyy
            data_inicio = datetime.strptime(str(evento[2]), '%Y-%m-%d').strftime('%d-%m-%Y')
            data_fim = datetime.strptime(str(evento[3]), '%Y-%m-%d').strftime('%d-%m-%Y')

            # Preenche as colunas da tabela
            ui.tabela_evento.setItem(i, 0, QTableWidgetItem(str(evento[0])))  # ID    
            ui.tabela_evento.setItem(i, 1, QTableWidgetItem(str(evento[1])))  # NOME
            ui.tabela_evento.setItem(i, 2, QTableWidgetItem(data_inicio))     # DATA INICIO (formatada)
            ui.tabela_evento.setItem(i, 3, QTableWidgetItem(data_fim))        # DATA FIM (formatada)
            ui.tabela_evento.setItem(i, 4, QTableWidgetItem(str(contagem_produtos)))  # PRODUTOS (contagem)
            ui.tabela_evento.setItem(i, 5, QTableWidgetItem(str(evento[4])))  # DESCRIÇÃO

        # Atualiza a tabela de monitoramento (se necessário)
        preencher_tabela_monitoramento(ui)

    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de eventos: {e}")

def preencher_tabela_monitoramento(ui):
    """
    Preenche a tabela_monitoramento com os dados fornecidos, separando a data em "Dia" e "Hora".
    
    dados: Lista de tuplas no formato (produto, quantidade, vendedor, data, valor_total, valor_un).
    """
    try:
                
        vendas = GetProdutosVendas()
        
        ui.tabela_monitoramento.clearContents()
        ui.tabela_monitoramento.setRowCount(len(vendas))


        # Preenche a tabela com os dados
        for i, venda in enumerate(vendas):
            # Formata a data em "Dia" e "Hora"
            

            
            dia = venda[3].strftime('%d/%m/%Y')  # Formato: dd/mm/yyyy
            hora = venda[3].strftime('%H:%M')    # Formato: HH:MM
            

            # Formata o valor total e o valor unitário para exibição
            valor_total_formatado = f"R$ {float(venda[4]):.2f}"
            valor_un_formatado = f"R$ {float(venda[5]):.2f}"

            # Insere os itens na tabela
            ui.tabela_monitoramento.setItem(i, 0, QTableWidgetItem(str(venda[2])))  # vendedor
            ui.tabela_monitoramento.setItem(i, 1, QTableWidgetItem(str(venda[0])))  # produto
            ui.tabela_monitoramento.setItem(i, 2, QTableWidgetItem(str(venda[1])))  # total de vendas
            ui.tabela_monitoramento.setItem(i, 3, QTableWidgetItem(str(valor_un_formatado)))  # valor un
            ui.tabela_monitoramento.setItem(i, 4, QTableWidgetItem(str(dia)))  # dia
            ui.tabela_monitoramento.setItem(i, 5, QTableWidgetItem(str(hora)))  # Vhora
            ui.tabela_monitoramento.setItem(i, 6, QTableWidgetItem(str(valor_total_formatado)))  # Valor Total


    except Exception as e:
        print(f"Erro ao preencher a tabela de monitoramento: {e}")


def atualizarInterface(ui, msg):
    print(f"Mudança observada: {msg}")
    

    try:
        # Verifica se a mensagem contém o caractere ':'
        if ':' in msg:
            # Divide a mensagem no primeiro ":" (tipo_mudanca:descrição)
            tipo_mudanca, descricao = msg.split(':', 1)
        else:
            # Mensagem sem ":" (tratamento especial)
            print(f"Mensagem recebida sem formato esperado: {msg}")
            return
        
        InitializeTables(ui)

        # Lógica de atualização com base no conteúdo da mensagem
        if 'produto' in descricao:  
            AtualizarTabelasProdutos(ui)
            AtualizaCompleterSearchProdutos(ui)
            print("Mudança na tabela produto, atualizando...")
        
        elif 'usuarios' in descricao: 
            AtualizaTabelasLogin(ui)
            AtualizaCompleterSearchColaboradores(ui)
            print("Mudança na tabela usuários, atualizando...")
            
        elif 'CARD' in descricao:
            UpdateFrames(ui)
            print("Mudança nos card iniciais.....")

        # Tratamento para mensagens específicas (exemplo: "Renovação Log")
        if tipo_mudanca == "RENOVACAO_LOG":
            AtualizaTabelasLogin(ui)
            AtualizaCompleterSearchColaboradores(ui)
            AtualizarTabelasProdutos(ui)
            AtualizaCompleterSearchProdutos(ui)
            print("RENOVAÇÃO DE LINHA")
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def AtualizarTabelasProdutosStatus(ui, status_filtro=None):
    """
    Atualiza a tabela de produtos com base no status fornecido.

    :param ui: Referência para a interface do usuário.
    :param status_filtro: Lista de status para filtrar os produtos (ex: ['ativo'], ['esgotado']).
                          Se None, exibe todos os produtos.
    """
    try:
        # Verifica se o filtro 'Eventos' está ativo
        if status_filtro and 'Eventos' in status_filtro:
            # Obtém produtos de eventos e produtos normais
            banco_produtos_evento = GetProdutosEvento()
            banco_produtos_normal = GetProdutos()
            banco_produtos = banco_produtos_evento + banco_produtos_normal  # Combina as duas listas
        else:
            # Obtém apenas produtos normais
            banco_produtos = GetProdutos()

        # Verifica se há produtos para exibir
        if not banco_produtos:
            print("Nenhum produto encontrado.")
            return

        # Filtra os produtos com base no status (se fornecido)
        if status_filtro:
            # Remove 'Eventos' da lista de filtros (já foi tratado acima)
            filtro_status = [status for status in status_filtro if status != 'Eventos']
            
            if filtro_status:  # Se houver filtros de status para aplicar
                banco_produtos = [produto for produto in banco_produtos if produto[6] in filtro_status]

        # Limpa a tabela antes de adicionar novos dados
        ui.tabela_produto.clearContents()
        ui.tabela_produto.setRowCount(len(banco_produtos))
        ui.tabela_alterar_produto.clearContents()
        ui.tabela_alterar_produto.setRowCount(len(banco_produtos))

        # Preenche as células com os dados dos produtos
        for i, produto in enumerate(banco_produtos):
            # Tabela produto
            ui.tabela_produto.setItem(i, 0, QTableWidgetItem(str(produto[1])))  # Produto
            ui.tabela_produto.setItem(i, 1, QTableWidgetItem(str(produto[2])))  # Cód
            ui.tabela_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3])))  # Quantidade
            ui.tabela_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4])))  # ValorUn
            ui.tabela_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  # Descrição
            ui.tabela_produto.setItem(i, 5, QTableWidgetItem(str(produto[6])))  # Condição

            # Armazenando o ID na tabela produto
            item_produto = ui.tabela_produto.item(i, 0)  # Aqui, o ID é armazenado no primeiro item da coluna
            item_produto.setData(Qt.UserRole, produto[0])  # Armazenando o ID na propriedade UserRole (assumindo que o ID é produto[0])
            
        for i, produto in enumerate(banco_produtos):
            # Tabela produto
            ui.tabela_alterar_produto.setItem(i, 0, QTableWidgetItem(str(produto[1])))  # Produto
            ui.tabela_alterar_produto.setItem(i, 1, QTableWidgetItem(str(produto[2])))  # Cód
            ui.tabela_alterar_produto.setItem(i, 2, NumericTableWidgetItem(str(produto[3])))  # Quantidade
            ui.tabela_alterar_produto.setItem(i, 3, NumericTableWidgetItem(str(produto[4])))  # ValorUn
            ui.tabela_alterar_produto.setItem(i, 4, QTableWidgetItem(str(produto[5])))  # Descrição
            ui.tabela_alterar_produto.setItem(i, 5, QTableWidgetItem(str(produto[6])))  # Condição

            # Armazenando o ID na tabela produto
            item_produto = ui.tabela_alterar_produto.item(i, 0)  # Aqui, o ID é armazenado no primeiro item da coluna
            item_produto.setData(Qt.UserRole, produto[0])  # Armazenando o ID na propriedade UserRole (assumindo que o ID é produto[0])

        # Estilizar a tabela
        UiTabelaProduto.Estilizar(ui)

    except Exception as e:
        Popup(f"Erro ao atualizar a tabela de produtos: {e}")
        

    

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        """Sobrescreve a comparação para ordenação numérica."""
        try:
            # Converte o texto para float antes de comparar
            return float(self.text()) < float(other.text())
        except ValueError:
            # Se não for possível converter, usa a ordenação padrão (alfanumérica)
            return super().__lt__(other)
        
class ZeroMQListener(QThread):
    notification_received = pyqtSignal(str)  # Sinal para notificar a interface

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)  # Socket de assinatura
        socket.connect("tcp://localhost:5555")  # Conecta ao publicador
        socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Assina todas as mensagens

        print("Assinante iniciado. Recebendo notificações...")
        while True:
            mensagem = socket.recv_string()  # Recebe a mensagem
            self.notification_received.emit(mensagem)  # Emite o sinal