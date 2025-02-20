# eventos.py

def conectar_eventos(ui):
    """Função que atribui eventos aos botões da UI"""
    
    ui.btn_home.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_home))


    ui.btn_Vendas.clicked.connect(lambda: print("Botão Vendas clicado!"))

