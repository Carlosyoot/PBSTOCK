from PyQt5.QtWidgets import QTableWidgetItem
from functions.events.InterfaceError.popup import Popup
from PyQt5.QtCore import Qt  
from database.Datalogic import DataGetAllLogins, GetProdutos, GetRecentsProduct
import random
from datetime import datetime, timedelta
from functions.events.CustomsWidgets.ProductTable import UiTabelaProduto




def InitializeTables(ui):
    
    AtualizarTabelasProdutos(ui)
    AtualizaTabelasLogin(ui)
    UiTabelaProduto.setup_table(ui)
    AtualizarTablesRecent(ui)


def AtualizarTabelasProdutos(ui):
    try: 
        banco_produtos = GetProdutos()
        
        if not banco_produtos:
            print("Nenhum produto encontrado")
            return
        
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
        # Supondo que a função DataGetAllLogins() retorne uma lista de tuplas ou listas
        banco_login = DataGetAllLogins()
        

        if not banco_login:
            Popup("Erro ao buscar dados de login.")
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
        


def gerar_dados_simulados(ui, tipo_data='diaria', num_registros=30):
    """
    Gera dados simulados para a tabela_monitoramento e preenche a tabela no UI.
    
    tipo_data: pode ser 'diaria', 'semanal' ou 'mensal'.
    num_registros: número de registros simulados a serem gerados.
    """
    produtos = ["Produto A", "Produto B", "Produto C", "Produto D"]
    
    # Define a data de referência como 05 de março de 2025
    data_referencia = datetime(2025, 3, 5)
    
    # Geração de dados baseados no tipo de data
    if tipo_data == 'diaria':
        # Dados diários, todos do mesmo dia (05/03/2025)
        datas = [data_referencia + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59)) for _ in range(num_registros)]
    elif tipo_data == 'semanal':
        # Dados semanais, espalhados até o fim da semana (09/03/2025)
        fim_da_semana = data_referencia + timedelta(days=(6 - data_referencia.weekday()))
        datas = [data_referencia + timedelta(days=random.randint(0, (fim_da_semana - data_referencia).days)) for _ in range(num_registros)]
    elif tipo_data == 'mensal':
        # Dados mensais, em qualquer dia de março de 2025
        datas = [datetime(2025, 3, random.randint(1, 31), random.randint(0, 23), random.randint(0, 59)) for _ in range(num_registros)]
    
    # Preenche a tabela com dados simulados
    ui.tabela_monitoramento.setRowCount(num_registros)
    colunas = ['Produto', 'Total de Venda', 'Valor Unitário', 'Dia', 'Hora', 'Valor Total']
    ui.tabela_monitoramento.setHorizontalHeaderLabels(colunas)
    
    for row in range(num_registros):
        produto = random.choice(produtos)
        total_venda = random.randint(1, 100)
        valor_unitario = round(random.uniform(5, 100), 2)
        dia = datas[row].strftime('%d/%m/%Y')
        hora = datas[row].strftime('%H:%M')
        valor_total = round(total_venda * valor_unitario, 2)
        
        # Insere os itens na tabela
        ui.tabela_monitoramento.setItem(row, 0, QTableWidgetItem(produto))
        ui.tabela_monitoramento.setItem(row, 1, NumericTableWidgetItem(str(total_venda)))  # Coluna numérica
        ui.tabela_monitoramento.setItem(row, 2, NumericTableWidgetItem(f"{valor_unitario:.2f}"))  # Coluna numérica
        ui.tabela_monitoramento.setItem(row, 3, QTableWidgetItem(dia))
        ui.tabela_monitoramento.setItem(row, 4, QTableWidgetItem(hora))
        ui.tabela_monitoramento.setItem(row, 5, NumericTableWidgetItem(f"{valor_total:.2f}"))  # 
    

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        """Sobrescreve a comparação para ordenação numérica."""
        try:
            # Converte o texto para float antes de comparar
            return float(self.text()) < float(other.text())
        except ValueError:
            # Se não for possível converter, usa a ordenação padrão (alfanumérica)
            return super().__lt__(other)
        
