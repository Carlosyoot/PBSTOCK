from functions.events.dialogBox.frameCalendar import MyDialog
from PyQt5.QtWidgets import QDialog
from functions.events.NavEvents.filtro import aplicar_filtro_por_intervalo




def iniciarFiltro(parent):
    dialog = MyDialog(parent)
    if dialog.exec_() == QDialog.Accepted:
        print("Dados coletados:", dialog.collected_data)
        data_inicio, data_fim = dialog.collected_data  
        aplicar_filtro_por_intervalo(parent.ui, data_inicio, data_fim)
