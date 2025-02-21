# eventos.py

def conectar_eventos(ui):
        """Função que atribui eventos aos botões da UI"""
        ui.btn_home.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_home))
        ui.btn_colaboradores.clicked.connect(
                lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_colaboradores))
        ui.btn_cadastrar_colaboradores.clicked.connect(
                lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastro_colaboradores))
        ui.btn_alterar_colaboradores.clicked.connect(
                lambda: ui.Telas_do_menu.setCurrentWidget(ui.alterar_colaboradores))

        ui.btn_vendas.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_vendas))
        ui.btn_produtos.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos))
        ui.btn_cadastrar_produto.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastar_produtos))
        ui.btn_alterar_produto.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_alterar_produtos))
        ui.btn_configs.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_configuracoes))
        ui.btn_monitoramento.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.monitoramento))


        ui.btn_vendas.clicked.connect(lambda: print("Botão Vendas clicado!"))


        # Tabela Vendas
        ui.tabela_vendas.setColumnWidth(0, 50)
        ui.tabela_vendas.setColumnWidth(1, 131)
        ui.tabela_vendas.setColumnWidth(2, 250)
        ui.tabela_vendas.setColumnWidth(3, 131)
        ui.tabela_vendas.setColumnWidth(4, 75)
        ui.tabela_vendas.setColumnWidth(5, 155)
        
        # Tabela Produtos
        ui.tabela_produto.setColumnWidth(0, 50)
        ui.tabela_produto.setColumnWidth(1, 131)
        ui.tabela_produto.setColumnWidth(2, 250)
        ui.tabela_produto.setColumnWidth(3, 131)
        ui.tabela_produto.setColumnWidth(4, 75)
        ui.tabela_produto.setColumnWidth(5, 155)

        # Tabela Cadastrar Produtos
        ui.tabela_cadastro.setColumnWidth(0, 50)
        ui.tabela_cadastro.setColumnWidth(1, 165)
        ui.tabela_cadastro.setColumnWidth(2, 300)
        ui.tabela_cadastro.setColumnWidth(3, 165)
        ui.tabela_cadastro.setColumnWidth(4, 75)
        ui.tabela_cadastro.setColumnWidth(5, 250)

        # Tabela Alterar Produtos
        ui.tabela_alterar_produto_2.setColumnWidth(0, 50)
        ui.tabela_alterar_produto_2.setColumnWidth(1, 165)
        ui.tabela_alterar_produto_2.setColumnWidth(2, 300)
        ui.tabela_alterar_produto_2.setColumnWidth(3, 165)
        ui.tabela_alterar_produto_2.setColumnWidth(4, 75)
        ui.tabela_alterar_produto_2.setColumnWidth(5, 250)
        
        