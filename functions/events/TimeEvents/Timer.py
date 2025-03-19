from PyQt5.QtCore import QTime
import datetime

def HoraData(ui):
    """Atualiza os rótulos com a data e hora atuais"""
    tempoAtual = QTime.currentTime()
    tempoTexto = tempoAtual.toString('hh:mm:ss')
    data_atual = datetime.date.today()
    dataTexto = data_atual.strftime('%d/%m/%Y')

    labels = [
        ui.lbl_hora_data_colaboradores, ui.lbl_hora_data_alterar_colaboradores,
        ui.lbl_hora_data_monitoramento, ui.lbl_hora_data,
        ui.lbl_hora_data_produtos, ui.lbl_hora_data_alterar_produto,
        ui.lbl_hora_data_cadastrar_produto, ui.lbl_hora_data_evento,
        ui.lbl_hora_data_evento, ui.lbl_hora_data_cadastro_evento
    ]

    for label in labels:
        label.setText(f'{dataTexto} {tempoTexto}')

