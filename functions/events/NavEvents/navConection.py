from database.Datalogic import UpdateTimes
from functions.events.CustomsWidgets.ProductMenuFilter import FILTERPRODUTO
from functions.events.CustomsWidgets.cardInit import init_custom_frame
from functions.events.DabaseEvents.UpdateTables import InitializeTables
from functions.events.NavEvents.autoFormater import initAutoFormatar
from functions.events.alterable.ManagerAlter import IniciarAlterarText
from PyQt5.QtCore import Qt





def conectar_eventos(ui, parent):
        """Função que atribui eventos aos botões da UI"""
        ui.btn_home.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_home))
        ui.btn_colaboradores.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_colaboradores))
        ui.btn_cadastrar_colaboradores.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastro_colaboradores))
        ui.btn_alterar_colaboradores.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.alterar_colaboradores))
        ui.btn_vendas.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_vendas))
        ui.btn_produtos.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos))
        ui.btn_cadastrar_produto.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastar_produtos))
        ui.btn_alterar_produto.clicked.connect( lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_alterar_produtos))
        ui.btn_configs.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_configuracoes))
        ui.btn_monitoramento.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.monitoramento))
        ui.btn_events.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_eventos))
        ui.btn_cadastrar_evento.clicked.connect(lambda:ui.Telas_do_menu.setCurrentWidget(ui.page_cadastro_eventos))
        


        '''FUNÇÃO RETORNO DO CADASTRO'''
        ui.btn_voltar_cadastro.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos))
        ui.btn_voltar_cadastro_colaborador.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_colaboradores))
        ui.btn_voltar_cadastro_evento.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_eventos))
        
        ''''FUNÇÃO RETORNO ALTERAÇÃO'''
        ui.btn_voltar_alterar_produto.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos))
        ui.btn_voltar_alterar_colaboradores.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_colaboradores))
        
        
        '''FUNÇÃO DE MOSTRAR SENHAS'''
        ui.btn_ver_senha.setCursor(Qt.PointingHandCursor)
        ui.btn_ver_senha.setToolTip("Clique para mostrar/ocultar a senha")
        
        '''FUNÇÃO DE ESTADO, NOS COLABORADORES'''
        ui.admin_button.setCheckable(True)
        ui.colaborador_button.setCheckable(True)

        
        
        
        





        ## Ajustar largura das colunas das tabelas
        #ui.tabela_vendas.setColumnWidth(0, 50)
        #ui.tabela_vendas.setColumnWidth(1, 50)
        #ui.tabela_vendas.setColumnWidth(2, 50)
        #ui.tabela_vendas.setColumnWidth(3, 50)
        #ui.tabela_vendas.setColumnWidth(4, 50)
        #ui.tabela_vendas.setColumnWidth(5, 50)
     
        ui.tabela_produto.setColumnWidth(0, 180)
        ui.tabela_produto.setColumnWidth(1, 80)
        ui.tabela_produto.setColumnWidth(2, 80)
        ui.tabela_produto.setColumnWidth(3, 100)
        ui.tabela_produto.setColumnWidth(4, 275)
        ui.tabela_produto.setColumnWidth(5, 100)
        
        ui.tabela_alterar_produto.setColumnWidth(0, 200)
        ui.tabela_alterar_produto.setColumnWidth(1, 80)
        ui.tabela_alterar_produto.setColumnWidth(2, 80)
        ui.tabela_alterar_produto.setColumnWidth(3, 100)
        ui.tabela_alterar_produto.setColumnWidth(4, 200)
        #
        ui.tabela_cadastro.setColumnWidth(0, 120)
        ui.tabela_cadastro.setColumnWidth(1, 80)
        ui.tabela_cadastro.setColumnWidth(2, 80)
        ui.tabela_cadastro.setColumnWidth(3, 80)
        ui.tabela_cadastro.setColumnWidth(4, 200)
        ui.tabela_cadastro.setColumnWidth(5, 120)
        
        
        
        ui.tabela_alterar_colaboradores.setColumnWidth(0, 120)
        ui.tabela_alterar_colaboradores.setColumnWidth(1, 120)
        ui.tabela_alterar_colaboradores.setColumnWidth(2, 100)
        ui.tabela_alterar_colaboradores.setColumnWidth(3, 100)
        ui.tabela_alterar_colaboradores.setColumnWidth(4, 160)
        #
        #
        ui.tabela_colaboradores.setColumnWidth(0, 270)
        ui.tabela_colaboradores.setColumnWidth(1, 270)
        ui.tabela_colaboradores.setColumnWidth(2, 270)  
        
        


        
        
        ui.valor_filtro = None
        ui.line_data_venda.setPlaceholderText("Data: DD/MM/YYYY")
        ui.line_data_horario.setPlaceholderText("Hora: HH:MM") 
        
        UpdateTimes()
        initAutoFormatar(ui)
        IniciarAlterarText(ui)
        FILTERPRODUTO(ui, parent) 
        init_custom_frame(ui)
        InitializeTables(ui)
        
        
        
# pyuic5 -o view/ui/FrmAdmin.py view/ui/FrmAdmin.ui
# pyrcc5 -o view/QRC/file_principal_rc.py view/QRC/file_principal_rc.qrc