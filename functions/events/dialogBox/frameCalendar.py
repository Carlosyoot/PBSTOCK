from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QHBoxLayout, QLineEdit, QToolButton, QCalendarWidget, QMessageBox, QWidget
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIntValidator


class DateEditCompleto(QWidget):
    def __init__(ui, parent=None):
        super().__init__(parent)

       
        layout = QHBoxLayout(ui)
        layout.setContentsMargins(0, 0, 0, 0) 
       
        ui.line_edit = QLineEdit(ui)
        ui.line_edit.setPlaceholderText("dd/MM/yyyy")
        ui.line_edit.setMaxLength(10) 
        ui.line_edit.setValidator(QIntValidator(0, 99999999, ui)) 
        ui.line_edit.textChanged.connect(ui.format_date)
        layout.addWidget(ui.line_edit)

        ui.calendar_button = QToolButton(ui)
        ui.calendar_button.setText("▼")  
        ui.calendar_button.clicked.connect(ui.show_calendar)
        layout.addWidget(ui.calendar_button)

        ui.calendar = QCalendarWidget(ui)
        ui.calendar.setWindowFlags(Qt.Popup) 
        ui.calendar.clicked.connect(ui.on_calendar_clicked)

    def format_date(ui):
        text = ui.line_edit.text().replace("/", "")  
        if len(text) > 8: 
            text = text[:8]
        
       
        formatted_text = ""
        for i, char in enumerate(text):
            if i in [2, 4]: 
                formatted_text += "/"
            formatted_text += char
        
        ui.line_edit.setText(formatted_text)

    def show_calendar(ui):
       
        date = ui.get_date()
        if date and date.isValid():
            ui.calendar.setSelectedDate(date)  

        ui.calendar.move(ui.mapToGlobal(ui.line_edit.geometry().bottomLeft()))
        ui.calendar.show()

    def on_calendar_clicked(ui, date):
        ui.line_edit.setText(date.toString("dd/MM/yyyy"))
        ui.calendar.hide()

    def get_date(ui):
        text = ui.line_edit.text()
        try:
            day, month, year = map(int, text.split("/"))
            return QDate(year, month, day)
        except (ValueError, AttributeError):
            return None


class MyDialog(QDialog):
    def __init__(ui, parent=None):
        super().__init__(parent)

        ui.setWindowTitle("Diálogo Personalizado")
        ui.setGeometry(100, 100, 500, 200) 
        ui.collected_data = None
        ui.selected_date_type = None
        ui.start_date = None
        ui.end_date = None

        main_layout = QVBoxLayout(ui)

        
        top_layout = QHBoxLayout()

       
        ui.date_type_combo = QComboBox(ui)
        ui.date_type_combo.addItem("Selecione o tipo de data")
        ui.date_type_combo.addItem("Semanal")
        ui.date_type_combo.addItem("Mensal")
        ui.date_type_combo.currentIndexChanged.connect(ui.on_date_type_changed)
        top_layout.addWidget(QLabel("Selecione o tipo de data:"))
        top_layout.addWidget(ui.date_type_combo)

        main_layout.addLayout(top_layout)

       
        ui.date_range_layout = QVBoxLayout()

       
        ui.start_date_edit = DateEditCompleto(ui)
        ui.start_date_edit.line_edit.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        ui.date_range_layout.addWidget(QLabel("Data Inicial:"))
        ui.date_range_layout.addWidget(ui.start_date_edit)

      
        ui.end_date_edit = DateEditCompleto(ui)
        ui.end_date_edit.line_edit.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        ui.date_range_layout.addWidget(QLabel("Data Final:"))
        ui.date_range_layout.addWidget(ui.end_date_edit)

        main_layout.addLayout(ui.date_range_layout)

       
        ui.btn_ok = QPushButton("OK", ui)
        ui.btn_ok.clicked.connect(ui.on_ok_clicked)
        main_layout.addWidget(ui.btn_ok, alignment=Qt.AlignRight)
        if parent:
            ui.move(parent.geometry().center() - ui.rect().center())

    def on_date_type_changed(ui, index):
        if index == 1: 
            ui.update_weekly_dates()
        elif index == 2:  
            ui.update_monthly_dates()

    def update_weekly_dates(self):
        start_date = self.start_date_edit.get_date()
        if start_date:
           
            day_of_week = start_date.dayOfWeek()

           
            days_to_sunday = (day_of_week % 7) 
            sunday = start_date.addDays(-days_to_sunday)

            saturday = sunday.addDays(6)

            self.start_date_edit.line_edit.setText(sunday.toString("dd/MM/yyyy"))
            self.end_date_edit.line_edit.setText(saturday.toString("dd/MM/yyyy"))


    def update_monthly_dates(ui):
        start_date = ui.start_date_edit.get_date()
        if start_date:
            end_date = QDate(start_date.year(), start_date.month(), start_date.daysInMonth())
            ui.end_date_edit.line_edit.setText(end_date.toString("dd/MM/yyyy"))

    def on_ok_clicked(ui):
        data = []

        ui.selected_date_type = ui.date_type_combo.currentText()
        start_date = ui.start_date_edit.get_date()
        end_date = ui.end_date_edit.get_date()

        if not start_date or not end_date:
            QMessageBox.warning(ui, "Erro", "Por favor, insira datas válidas.")
            return

        ui.start_date = start_date.toString("dd/MM/yyyy")
        ui.end_date = end_date.toString("dd/MM/yyyy")

        data.append(ui.start_date)
        data.append(ui.end_date)

        ui.collected_data = data

        ui.accept()

        return data
