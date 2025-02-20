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
        ui.btn_clientes.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_clientes))
        ui.btn_cadastrar_clientes.clicked.connect(
                lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastrar_clientes))
        ui.btn_alterar_clientes.clicked.connect(
                lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_alterar_clientes))
        ui.btn_fornecedores.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_fornecedores))
        ui.btn_adicionar_forncedores.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastrar_fornecedores))
        ui.btn_editar_fornecedores.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_alterar_fornecedores))

        ui.btn_Vendas.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_vendas))
        ui.btn_produtos.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_produtos))
        ui.btn_cadastrar_produto.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_cadastar_produtos))
        ui.btn_alterar_produto.clicked.connect(
            lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_alterar_produtos))
        ui.btn_configs.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.pg_configuracoes))
        ui.btn_vendas_2.clicked.connect(lambda: ui.Telas_do_menu.setCurrentWidget(ui.monitoramento))


        ui.btn_Vendas.clicked.connect(lambda: print("Botão Vendas clicado!"))

        ui.tabela_clientes.setColumnWidth(0, 192)
        ui.tabela_clientes.setColumnWidth(1, 192)
        ui.tabela_clientes.setColumnWidth(2, 192)
        ui.tabela_clientes.setColumnWidth(3, 194)

        # Tabela Cadastrar Clientes
        ui.tabela_cadastrar_clientes.setColumnWidth(0, 247)
        ui.tabela_cadastrar_clientes.setColumnWidth(1, 247)
        ui.tabela_cadastrar_clientes.setColumnWidth(2, 247)
        ui.tabela_cadastrar_clientes.setColumnWidth(3, 249)

        # Tabela Alterar Clientes
        ui.tabela_alterar_clientes.setColumnWidth(0, 247)
        ui.tabela_alterar_clientes.setColumnWidth(1, 247)
        ui.tabela_alterar_clientes.setColumnWidth(2, 247)
        ui.tabela_alterar_clientes.setColumnWidth(3, 249)
        
        # Tabela Vendas
        ui.tabela_vendas.setColumnWidth(0, 50)
        ui.tabela_vendas.setColumnWidth(1, 131)
        ui.tabela_vendas.setColumnWidth(2, 250)
        ui.tabela_vendas.setColumnWidth(3, 131)
        ui.tabela_vendas.setColumnWidth(4, 75)
        ui.tabela_vendas.setColumnWidth(5, 155)
        
        # Tabela Fornecedores
        ui.tabela_fornecedores.setColumnWidth(0, 257)
        ui.tabela_fornecedores.setColumnWidth(1, 257)
        ui.tabela_fornecedores.setColumnWidth(2, 257)

        # Tabela Cadastrar Fornecedores
        ui.tabela_cadastrar_fornecedores.setColumnWidth(0, 330)
        ui.tabela_cadastrar_fornecedores.setColumnWidth(1, 330)
        ui.tabela_cadastrar_fornecedores.setColumnWidth(2, 330)

        # Tabela Alterar Fornecedores
        ui.tabela_alterar_fornecedores.setColumnWidth(0, 330)
        ui.tabela_alterar_fornecedores.setColumnWidth(1, 330)
        ui.tabela_alterar_fornecedores.setColumnWidth(2, 330)
        
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
        ui.tabela_alterar_produto.setColumnWidth(0, 50)
        ui.tabela_alterar_produto.setColumnWidth(1, 165)
        ui.tabela_alterar_produto.setColumnWidth(2, 300)
        ui.tabela_alterar_produto.setColumnWidth(3, 165)
        ui.tabela_alterar_produto.setColumnWidth(4, 75)
        ui.tabela_alterar_produto.setColumnWidth(5, 250)
        
        