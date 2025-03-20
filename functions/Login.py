from database.Datalogic import DataLoginUser
from PyQt5.QtCore import QTimer




def logar(ui, janela_atual):
    from functions.Admin import WindowManager

   
    User = ui.lineEdit.text()
    Password = ui.lineEdit_2.text()

    result = DataLoginUser(User, Password)

    if result['status'] == 'success' and result['redirect'] == 'admin':
        ui.lineEdit.setStyleSheet(StyleSucess.style)
        ui.lineEdit_2.setStyleSheet(StyleSucess.style)
        print("Redirecionando para Admin")
        janela_atual.close()
        WindowManager.open_admin(User)  
      
    else:
        ui.lineEdit.setStyleSheet(StyleError.style)
        ui.lineEdit_2.setStyleSheet(StyleError.style)
        print('Erro ao efetuar login')

class StyleSucess:
    style = ('border: 2px solid rgb(245, 185, 66);'
             'border-bottom-color: rgb(245, 185, 66);color: rgb(0,0,0);'
             'border-radius: 12px;font: 10pt "Montserrat"; padding-left:10px')

class StyleError:
    style = ('border: 2px solid rgb(255, 17, 49);'
             'border-bottom-color: rgb(255, 17, 49);color: rgb(0,0,0);'
             'border-radius: 12px; font: 10pt "Montserrat";padding-left: 10px;')
    
