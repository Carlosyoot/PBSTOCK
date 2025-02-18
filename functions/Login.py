from request.Request import GetLogin
from functions.Admin import WindowManager


def logar(ui, janela_atual):
    
    global SecondWindow
    
    User = ui.lineEdit.text()
    Password = ui.lineEdit_2.text()

    # Envia os dados para o servidor
    response = GetLogin(User, Password)
    
    status = response.get('status')
    redirect = response.get('redirect')

    if redirect == 'admin' and status == 'sucess':
        ui.lineEdit.setStyleSheet(StyleSucess.style)
        ui.lineEdit_2.setStyleSheet(StyleSucess.style)
        print("Redirecionando para Admin")

        janela_atual.close()
        WindowManager.open_admin()
        
#    FUTURA PAGE DE COLABORADOR
    #elif redirect == 'colaborador' and status == 'sucess':
    #    ui.lineEdit.setStyleSheet(StyleSucess.style)
    #    ui.lineEdit_2.setStyleSheet(StyleSucess.style)
    #    print("Redirecionando para colaborador")
#
    #    # Fecha a janela atual
    #    janela_atual.close()
    
    
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
    
