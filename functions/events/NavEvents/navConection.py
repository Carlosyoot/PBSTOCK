from functions.events.DabaseEvents.UpdateTables import InitializeTables, gerar_dados_simulados
from functions.events.searchs.ColaboradorSearch import AtualizaCompleterSearchColaboradores
from functions.events.searchs.ProdutoSearch import AtualizaCompleterSearchProdutos
from functions.events.alterable.ManagerAlter import IniciarAlterarText
from PyQt5.QtCore import Qt




def conectar_eventos(ui):
        """Função que atribui eventos aos botões da UI"""
        # Conectar botões de navegação
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
        
        
        
        

        # Conecta os botões à função de alternância




        ## Ajustar largura das colunas das tabelas
        #ui.tabela_vendas.setColumnWidth(0, 50)
        #ui.tabela_vendas.setColumnWidth(1, 50)
        #ui.tabela_vendas.setColumnWidth(2, 50)
        #ui.tabela_vendas.setColumnWidth(3, 50)
        #ui.tabela_vendas.setColumnWidth(4, 50)
        #ui.tabela_vendas.setColumnWidth(5, 50)
#       
        ui.tabela_produto.setColumnWidth(0, 180)
        ui.tabela_produto.setColumnWidth(1, 80)
        ui.tabela_produto.setColumnWidth(2, 80)
        ui.tabela_produto.setColumnWidth(3, 100)
        ui.tabela_produto.setColumnWidth(4, 280)
        ui.tabela_produto.setColumnWidth(5, 100)
        
        ui.tabela_alterar_produto.setColumnWidth(0, 200)
        ui.tabela_alterar_produto.setColumnWidth(1, 80)
        ui.tabela_alterar_produto.setColumnWidth(2, 80)
        ui.tabela_alterar_produto.setColumnWidth(3, 100)
        ui.tabela_alterar_produto.setColumnWidth(4, 200)
        #
        ui.tabela_cadastro.setColumnWidth(0, 50)
        ui.tabela_cadastro.setColumnWidth(1, 50)
        ui.tabela_cadastro.setColumnWidth(2, 50)
        ui.tabela_cadastro.setColumnWidth(3, 50)
        ui.tabela_cadastro.setColumnWidth(4, 50)
        ui.tabela_cadastro.setColumnWidth(5, 50)
        
        
        
        ui.tabela_alterar_colaboradores.setColumnWidth(0, 200)
        ui.tabela_alterar_colaboradores.setColumnWidth(1, 150)
        ui.tabela_alterar_colaboradores.setColumnWidth(2, 150)
        ui.tabela_alterar_colaboradores.setColumnWidth(3, 150)
        ui.tabela_alterar_colaboradores.setColumnWidth(4, 100)
        #
        #
        ui.tabela_colaboradores.setColumnWidth(0, 270)
        ui.tabela_colaboradores.setColumnWidth(1, 270)
        ui.tabela_colaboradores.setColumnWidth(2, 270)  
        
        
#
        #ui.tabela_alterar_produto_2.setColumnWidth(0, 50)
        #ui.tabela_alterar_produto_2.setColumnWidth(1, 50)
        #ui.tabela_alterar_produto_2.setColumnWidth(2, 50)
        #ui.tabela_alterar_produto_2.setColumnWidth(3, 50)
        #ui.tabela_alterar_produto_2.setColumnWidth(4, 50)
        #ui.tabela_alterar_produto_2.setColumnWidth(5, 50)

        # Configurações do filtro de vendas
        ui.valor_filtro = None
        IniciarAlterarText(ui)
        InitializeTables(ui)
        AtualizaCompleterSearchColaboradores(ui)
        AtualizaCompleterSearchProdutos(ui)
        
        gerar_dados_simulados(ui, tipo_data='diaria', num_registros=30)

        # Exemplo para gerar dados semanais
        gerar_dados_simulados(ui, tipo_data='semanal', num_registros=30)
        
        # Exemplo para gerar dados mensais
        gerar_dados_simulados(ui, tipo_data='mensal', num_registros=30)
        
       
# py            uic5 -o view/ui/FrmAdmin.py view/ui/FrmAdmin.ui
# pyrcc5 -o view/QRC/file_principal_rc.py view/QRC/file_principal_rc.qrc