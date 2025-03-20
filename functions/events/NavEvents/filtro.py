from datetime import datetime, timedelta
from PyQt5.QtWidgets import QTableWidgetItem

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)

def aplicar_filtro(ui):
    dados = obter_dados_tabela(ui) 

    if ui.valor_filtro == 'day':
        dados_filtrados = filtrar_por_dia(dados)
    elif ui.valor_filtro == 'week':
        dados_filtrados = filtrar_por_semana(dados)
    elif ui.valor_filtro == 'month':
        dados_filtrados = filtrar_por_mes(dados)
    else:
        dados_filtrados = dados  

    atualizar_tabela(ui, dados_filtrados)

def obter_dados_tabela(ui):
    if not hasattr(ui, 'dados_tabela'): 
        ui.dados_tabela = []  
        for row in range(ui.tabela_monitoramento.rowCount()):
            if ui.tabela_monitoramento.item(row, 0) is None:
                continue

            linha = {
                "vendedor": ui.tabela_monitoramento.item(row, 0).text(), 
                "produto": ui.tabela_monitoramento.item(row, 1).text(), 
                "vendas": ui.tabela_monitoramento.item(row, 2).text(), 
                "valor_un": ui.tabela_monitoramento.item(row, 3).text(),  
                "dia": ui.tabela_monitoramento.item(row, 4).text(), 
                "hora": ui.tabela_monitoramento.item(row, 5).text(), 
                "valor_total": ui.tabela_monitoramento.item(row, 6).text(),  
            }
            ui.dados_tabela.append(linha)
    return ui.dados_tabela

def filtrar_por_dia(dados):
    hoje = datetime.now().strftime("%d/%m/%Y")  
    return [registro for registro in dados if registro["dia"] == hoje]


def filtrar_por_semana(dados):
    hoje = datetime.now()
    
   
    inicio_semana = hoje - timedelta(days=hoje.weekday() + 1) 
    if hoje.weekday() == 6: 
        inicio_semana = hoje
    
    fim_semana = inicio_semana + timedelta(days=6)
    
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_semana = fim_semana.replace(hour=23, minute=59, second=59, microsecond=999999)

    dados_filtrados = []
    for registro in dados:
        dia_registro = datetime.strptime(registro["dia"], "%d/%m/%Y") 
        if inicio_semana <= dia_registro <= fim_semana:
            dados_filtrados.append(registro)
    return dados_filtrados

def filtrar_por_mes(dados):
    hoje = datetime.now().strftime("%m/%Y")  
    return [registro for registro in dados if registro["dia"].endswith(hoje)]



def atualizar_tabela(ui, dados_filtrados):
    ui.tabela_monitoramento.setSortingEnabled(False)  
    ui.tabela_monitoramento.setRowCount(0) 

    for registro in dados_filtrados:
        row = ui.tabela_monitoramento.rowCount()
        ui.tabela_monitoramento.insertRow(row)
        
        ui.tabela_monitoramento.setItem(row, 0, QTableWidgetItem(registro["vendedor"])) 
        ui.tabela_monitoramento.setItem(row, 1, QTableWidgetItem(registro["produto"]))  
        ui.tabela_monitoramento.setItem(row, 2, NumericTableWidgetItem(registro["vendas"]))  
        ui.tabela_monitoramento.setItem(row, 3, NumericTableWidgetItem(registro["valor_un"]))  
        ui.tabela_monitoramento.setItem(row, 4, QTableWidgetItem(registro["dia"]))  
        ui.tabela_monitoramento.setItem(row, 5, QTableWidgetItem(registro["hora"]))  
        ui.tabela_monitoramento.setItem(row, 6, NumericTableWidgetItem(registro["valor_total"]))  

    ui.tabela_monitoramento.setSortingEnabled(True) 
def filtrar_por_intervalo(dados, data_inicio, data_fim):
    """Filtra os dados para exibir apenas os registros dentro do intervalo de datas."""
    dados_filtrados = []
    for registro in dados:
        dia_registro = datetime.strptime(registro["dia"], "%d/%m/%Y")  
        if data_inicio <= dia_registro <= data_fim:
            dados_filtrados.append(registro)
    return dados_filtrados

def aplicar_filtro_por_intervalo(ui, data_inicio, data_fim):
    """Filtra os dados da tabela_monitoramento com base no intervalo de datas."""
    dados = obter_dados_tabela(ui)  
    data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
    data_fim = datetime.strptime(data_fim, "%d/%m/%Y")

    dados_filtrados = filtrar_por_intervalo(dados, data_inicio, data_fim)

    atualizar_tabela(ui, dados_filtrados)
    
def alternar_filtro_e_atualizar_botao(ui):
    """Altera o filtro e atualiza o texto do botão com base no estado atual."""
    
    if ui.valor_filtro is None:
        ui.valor_filtro = 'day'
        ui.btn_filtro_vendas.setText('DIA')
    
    elif ui.valor_filtro == 'day':
        ui.valor_filtro = 'week'
        ui.btn_filtro_vendas.setText('SEMANA')
    
    elif ui.valor_filtro == 'week':
        ui.valor_filtro = 'month'
        ui.btn_filtro_vendas.setText('MÊS')
    
    else:
        ui.valor_filtro = 'day'
        ui.btn_filtro_vendas.setText('DIA')

    aplicar_filtro(ui)


