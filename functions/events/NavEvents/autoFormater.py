from PyQt5.QtWidgets import QLineEdit


def format_date(line_edit: QLineEdit):
    text = line_edit.text()
    digits = [c for c in text if c.isdigit()]  
    formatted_text = ""

    for i, digit in enumerate(digits):
        if i == 2 or i == 4: 
            formatted_text += "/"
        formatted_text += digit

    if len(formatted_text) > 10:
        formatted_text = formatted_text[:10]

    line_edit.blockSignals(True)
    line_edit.setText(formatted_text)
    line_edit.blockSignals(False)
    line_edit.setCursorPosition(len(formatted_text))


def format_time(line_edit: QLineEdit):
    text = line_edit.text()
    digits = [c for c in text if c.isdigit()] 
    formatted_text = ""

    for i, digit in enumerate(digits):
        if i == 2: 
            formatted_text += ":"
        formatted_text += digit

    if len(formatted_text) > 5:
        formatted_text = formatted_text[:5]

    line_edit.blockSignals(True)
    line_edit.setText(formatted_text)
    line_edit.blockSignals(False)
    line_edit.setCursorPosition(len(formatted_text))


def initAutoFormatar(ui):


    date_fields = [ui.line_data_venda, ui.line_data_event, ui.line_dataend_event]
    time_fields = [ui.line_data_horario]

    for field in date_fields:
        if isinstance(field, QLineEdit):
            field.textChanged.connect(lambda _, le=field: format_date(le))

    for field in time_fields:
        if isinstance(field, QLineEdit):
            field.textChanged.connect(lambda _, le=field: format_time(le))
