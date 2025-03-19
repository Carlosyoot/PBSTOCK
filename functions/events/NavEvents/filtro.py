from datetime import datetime, timedelta
from PyQt5.QtWidgets import QTableWidgetItem

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        """Sobrescreve a comparação para ordenação numérica."""
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)

def aplicar_filtro(ui):
    """Filtra os dados da tabela_monitoramento com base no valor_filtro."""
    dados = obter_dados_tabela(ui)  # Obtém os dados da tabela

    if ui.valor_filtro == 'day':
        dados_filtrados = filtrar_por_dia(dados)
    elif ui.valor_filtro == 'week':
        dados_filtrados = filtrar_por_semana(dados)
    elif ui.valor_filtro == 'month':
        dados_filtrados = filtrar_por_mes(dados)
    else:
        dados_filtrados = dados  # Caso padrão, sem filtro

    atualizar_tabela(ui, dados_filtrados)

def obter_dados_tabela(ui):
    """Retorna os dados da tabela_monitoramento e os armazena em ui.dados_tabela."""
    if not hasattr(ui, 'dados_tabela'):  # Verifica se os dados já foram carregados
        ui.dados_tabela = []  # Inicializa a lista de dados
        for row in range(ui.tabela_monitoramento.rowCount()):
            if ui.tabela_monitoramento.item(row, 0) is None:
                continue

            # Armazena todas as colunas da linha
            linha = {
                "vendedor": ui.tabela_monitoramento.item(row, 0).text(),  # Coluna 0: Vendedor
                "produto": ui.tabela_monitoramento.item(row, 1).text(),  # Coluna 1: Produto
                "vendas": ui.tabela_monitoramento.item(row, 2).text(),  # Coluna 2: Vendas (Quantidade)
                "valor_un": ui.tabela_monitoramento.item(row, 3).text(),  # Coluna 3: Valor Un
                "dia": ui.tabela_monitoramento.item(row, 4).text(),  # Coluna 4: Dia
                "hora": ui.tabela_monitoramento.item(row, 5).text(),  # Coluna 5: Hora
                "valor_total": ui.tabela_monitoramento.item(row, 6).text(),  # Coluna 6: Valor Total
            }
            ui.dados_tabela.append(linha)
    return ui.dados_tabela

def filtrar_por_dia(dados):
    """Filtra os dados para exibir apenas os registros do dia atual."""
    hoje = datetime.now().strftime("%d/%m/%Y")  # Formato da data na tabela
    return [registro for registro in dados if registro["dia"] == hoje]


def filtrar_por_semana(dados):
    """Filtra os dados para exibir apenas os registros da semana atual (começando no domingo)."""
    hoje = datetime.now()
    
    # Calcula o início da semana (domingo)
    inicio_semana = hoje - timedelta(days=hoje.weekday() + 1)  # Subtrai o número de dias até o domingo anterior
    # Se hoje for domingo, o início da semana já é hoje
    if hoje.weekday() == 6:  # Domingo é 6
        inicio_semana = hoje
    
    # Calcula o fim da semana (sábado)
    fim_semana = inicio_semana + timedelta(days=6)
    
    # Ajusta o início e o fim da semana para o início do dia (00:00:00)
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_semana = fim_semana.replace(hour=23, minute=59, second=59, microsecond=999999)

    dados_filtrados = []
    for registro in dados:
        dia_registro = datetime.strptime(registro["dia"], "%d/%m/%Y")  # Converte a string para datetime
        if inicio_semana <= dia_registro <= fim_semana:
            dados_filtrados.append(registro)
    return dados_filtrados

def filtrar_por_mes(dados):
    """Filtra os dados para exibir apenas os registros do mês atual."""
    hoje = datetime.now().strftime("%m/%Y")  # Formato do mês na tabela
    return [registro for registro in dados if registro["dia"].endswith(hoje)]



def atualizar_tabela(ui, dados_filtrados):
    """Atualiza a tabela_monitoramento com os dados filtrados."""
    ui.tabela_monitoramento.setSortingEnabled(False)  # Desativa a ordenação
    ui.tabela_monitoramento.setRowCount(0)  # Limpa a tabela

    for registro in dados_filtrados:
        row = ui.tabela_monitoramento.rowCount()
        ui.tabela_monitoramento.insertRow(row)
        
        # Preenche as colunas da tabela
        ui.tabela_monitoramento.setItem(row, 0, QTableWidgetItem(registro["vendedor"]))  # Vendedor
        ui.tabela_monitoramento.setItem(row, 1, QTableWidgetItem(registro["produto"]))  # Produto
        ui.tabela_monitoramento.setItem(row, 2, NumericTableWidgetItem(registro["vendas"]))  # Vendas (Quantidade)
        ui.tabela_monitoramento.setItem(row, 3, NumericTableWidgetItem(registro["valor_un"]))  # Valor Un
        ui.tabela_monitoramento.setItem(row, 4, QTableWidgetItem(registro["dia"]))  # Dia
        ui.tabela_monitoramento.setItem(row, 5, QTableWidgetItem(registro["hora"]))  # Hora
        ui.tabela_monitoramento.setItem(row, 6, NumericTableWidgetItem(registro["valor_total"]))  # Valor Total

    ui.tabela_monitoramento.setSortingEnabled(True)  # Reativa a ordenação
            
def filtrar_por_intervalo(dados, data_inicio, data_fim):
    """Filtra os dados para exibir apenas os registros dentro do intervalo de datas."""
    dados_filtrados = []
    for registro in dados:
        # Acessa a data do registro usando a chave "dia"
        dia_registro = datetime.strptime(registro["dia"], "%d/%m/%Y")  # Converte a string para datetime
        if data_inicio <= dia_registro <= data_fim:
            dados_filtrados.append(registro)
    return dados_filtrados

def aplicar_filtro_por_intervalo(ui, data_inicio, data_fim):
    """Filtra os dados da tabela_monitoramento com base no intervalo de datas."""
    dados = obter_dados_tabela(ui)  # Obtém os dados da tabela

    # Converte as strings de data para objetos datetime
    data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
    data_fim = datetime.strptime(data_fim, "%d/%m/%Y")

    # Filtra os dados pelo intervalo de datas
    dados_filtrados = filtrar_por_intervalo(dados, data_inicio, data_fim)

    # Atualiza a tabela com os dados filtrados
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


