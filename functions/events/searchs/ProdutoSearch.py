from decimal import Decimal
from database.Datalogic import GetProdutoNomesCod, GetProdutoNomesCodAtivo, GetValueProduto
from functions.events.searchs.CustomSugestion import CustomCompleterCód, CustomCompleterNome

def AtualizaCompleterSearchProdutos(ui):
    """
    Configura o QCompleter com base nos nomes e códigos dos produtos.
    """
    try:



        
        CustomCompt = CustomCompleterCód(GetProdutoNomesCodAtivo)
        CustomComptNome = CustomCompleterNome(GetProdutoNomesCod)


        ui.line_search_Bar_produtos.setCompleter(CustomComptNome)
        ui.line_search_Bar_alterar_produto.setCompleter(CustomComptNome)
        ui.line_codigo_vendas.setCompleter(CustomCompt)
        
        
        # Conecta os sinais para filtrar as tabelas de acordo com a busca
        ui.line_search_Bar_produtos.returnPressed.connect(
            lambda: filtrar_tabela_produtos(ui, 1)
        )

        ui.line_search_Bar_alterar_produto.returnPressed.connect(
            lambda: filtrar_tabela_produtos(ui, 2)
        )

        ui.line_search_Bar_produtos.textChanged.connect(
            lambda: reexibir_tabela_produtos(ui) if ui.line_search_Bar_produtos.text().strip() == "" else None
        )
        
        ui.line_search_Bar_alterar_produto.textChanged.connect(
            lambda: reexibir_tabela_produtos(ui) if ui.line_search_Bar_alterar_produto.text().strip() == "" else None
        )
        
        ui.line_quantidade_vendas.textChanged.connect(
            lambda: ProdutosTotal(ui)  # Chama a função sempre que o texto da quantidade mudar
        )

        ui.line_codigo_vendas.textChanged.connect(
            lambda: ProdutosTotal(ui)  # Chama a função sempre que o texto do código mudar
        )
        
        
        
        



    except Exception as e:
        print(f"Erro ao configurar completer para produtos: {e}")


def filtrar_tabela_produtos(ui, alter):
    """
    Filtra a tabela de produtos com base no texto digitado no campo de busca.
    Pode filtrar por nome, código ou pelo formato "nome - código".
    """
    try:
        if alter == 1:
            # Campo de busca e tabela para produtos
            texto_busca = ui.line_search_Bar_produtos.text().strip().lower()
            tabela = ui.tabela_produto
        elif alter == 2:
            # Campo de busca e tabela para alteração de produtos
            texto_busca = ui.line_search_Bar_alterar_produto.text().strip().lower()
            tabela = ui.tabela_alterar_produto
        else:
            return

        print(f"Texto de busca: {texto_busca}")

        # Faz o parsing do texto de busca para obter nome e código
        if " - " in texto_busca:
            nome_busca, codigo_busca = texto_busca.rsplit(" - ", 1)  # Alteração aqui
        else:
            # Se não houver " - ", assume que o texto pode ser nome ou código
            nome_busca = texto_busca
            codigo_busca = texto_busca

        # Percorre as linhas da tabela e verifica se o texto de busca está presente
        row_count = tabela.rowCount()

        for row in range(row_count):
            # Obtém o nome e o código da linha atual
            nome = tabela.item(row, 0).text().lower()  # Coluna 0: Nome
            codigo = tabela.item(row, 1).text().lower()  # Coluna 1: Código

            # Verifica se o nome ou o código da busca está presente nas colunas correspondentes
            match_nome = nome_busca in nome if nome_busca else True
            match_codigo = codigo_busca == codigo if codigo_busca else True

            # Mostra ou oculta a linha com base no resultado da busca
            match = match_nome or match_codigo
            tabela.setRowHidden(row, not match)
            print(f"Linha {row}: {'Mostrar' if match else 'Ocultar'} - Nome: {nome}, Código: {codigo}")

    except Exception as e:
        print(f"Erro ao filtrar tabela de produtos: {e}")


def reexibir_tabela_produtos(ui):
    """
    Reexibe todas as linhas das tabelas de produtos e alteração de produtos.
    """
    try:
        # Reexibe todas as linhas da tabela de produtos
        row_count_produto = ui.tabela_produto.rowCount()
        for row in range(row_count_produto):
            ui.tabela_produto.setRowHidden(row, False)  # Mostra todas as linhas

        # Reexibe todas as linhas da tabela de alteração de produtos
        row_count_alterar_produto = ui.tabela_alterar_produto.rowCount()
        for row in range(row_count_alterar_produto):
            ui.tabela_alterar_produto.setRowHidden(row, False)  # Mostra todas as linhas

    except Exception as e:
        print(f"Erro ao reexibir tabelas de produtos: {e}")
        

def ProdutosTotal(ui):
    Quantidade = ui.line_quantidade_vendas.text().strip()
    Código = ui.line_codigo_vendas.text().strip()

    print("Texto modificado enter", Quantidade, Código)

    try:
        # Verifica se o código contém "EVT"
        if "EVT" in Código:
            if Código and Quantidade:  # Se ambos os campos estiverem preenchidos
                # Busca o valor unitário do produto
                valor_unitario = GetValueProduto(Código)
                if valor_unitario is not None:  # Se o valor unitário foi encontrado
                    quantidade = Decimal(Quantidade)  # Converte a quantidade para Decimal
                    valor_total = valor_unitario * quantidade  # Calcula o valor total (ambos são Decimal)
                    ui.line_total_venda.setText(f'R$: {float(valor_total):.2f}')  # Converte para float para exibição
                else:
                    print("Produto não encontrado ou erro ao buscar valor unitário.")
            else:
                print("Preencha ambos os campos: código e quantidade.")
        else:
            # Verifica se o código tem exatamente 5 dígitos
            if len(Código) == 5:
                if Código and Quantidade:  # Se ambos os campos estiverem preenchidos
                    # Busca o valor unitário do produto
                    valor_unitario = GetValueProduto(Código)
                    if valor_unitario is not None:  # Se o valor unitário foi encontrado
                        quantidade = Decimal(Quantidade)  # Converte a quantidade para Decimal
                        valor_total = valor_unitario * quantidade  # Calcula o valor total (ambos são Decimal)
                        ui.line_total_venda.setText(f'R$: {float(valor_total):.2f}')  # Converte para float para exibição
                    else:
                        print("Produto não encontrado ou erro ao buscar valor unitário.")
                else:
                    print("Preencha ambos os campos: código e quantidade.")
            else:
                print("Código precisa ter 5 dígitos")
                
    except Exception as e:
        print(f"Erro ao calcular o valor total: {e}")

