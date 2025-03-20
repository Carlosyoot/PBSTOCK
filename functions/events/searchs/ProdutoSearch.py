from decimal import Decimal
from database.Datalogic import GetProdutoNomesCod, GetProdutoNomesCodAtivo, GetValueProduto
from functions.events.searchs.CustomSugestion import CustomCompleterCód, CustomCompleterNome

def AtualizaCompleterSearchProdutos(ui):

    try:

        CustomCompt = CustomCompleterCód(GetProdutoNomesCodAtivo)
        CustomComptNome = CustomCompleterNome(GetProdutoNomesCod)


        ui.line_search_Bar_produtos.setCompleter(CustomComptNome)
        ui.line_search_Bar_alterar_produto.setCompleter(CustomComptNome)
        ui.line_codigo_vendas.setCompleter(CustomCompt)
        
        
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
            lambda: ProdutosTotal(ui) 
        )

        ui.line_codigo_vendas.textChanged.connect(
            lambda: ProdutosTotal(ui)  
        )
        
        
        
        



    except Exception as e:
        print(f"Erro ao configurar completer para produtos: {e}")


def filtrar_tabela_produtos(ui, alter):
   
    try:
        if alter == 1:
            texto_busca = ui.line_search_Bar_produtos.text().strip().lower()
            tabela = ui.tabela_produto
        elif alter == 2:
            texto_busca = ui.line_search_Bar_alterar_produto.text().strip().lower()
            tabela = ui.tabela_alterar_produto
        else:
            return

        print(f"Texto de busca: {texto_busca}")

        if " - " in texto_busca:
            nome_busca, codigo_busca = texto_busca.rsplit(" - ", 1)
        else:
            nome_busca = texto_busca
            codigo_busca = texto_busca

        row_count = tabela.rowCount()

        for row in range(row_count):
            nome = tabela.item(row, 0).text().lower()  
            codigo = tabela.item(row, 1).text().lower()  

            match_nome = nome_busca in nome if nome_busca else True
            match_codigo = codigo_busca == codigo if codigo_busca else True

            match = match_nome or match_codigo
            tabela.setRowHidden(row, not match)

    except Exception as e:
        print(f"Erro ao filtrar tabela de produtos: {e}")


def reexibir_tabela_produtos(ui):
  
    try:
        row_count_produto = ui.tabela_produto.rowCount()
        for row in range(row_count_produto):
            ui.tabela_produto.setRowHidden(row, False)  

        row_count_alterar_produto = ui.tabela_alterar_produto.rowCount()
        for row in range(row_count_alterar_produto):
            ui.tabela_alterar_produto.setRowHidden(row, False) 

    except Exception as e:
        print(f"Erro ao reexibir tabelas de produtos: {e}")
        

def ProdutosTotal(ui):
    Quantidade = ui.line_quantidade_vendas.text().strip()
    Código = ui.line_codigo_vendas.text().strip()

    print("Texto modificado enter", Quantidade, Código)

    try:
        if "EVT" in Código:
            if Código and Quantidade:  
                valor_unitario = GetValueProduto(Código)
                if valor_unitario is not None:  
                    quantidade = Decimal(Quantidade)  
                    valor_total = valor_unitario * quantidade 
                    ui.line_total_venda.setText(f'R$: {float(valor_total):.2f}')  
                else:
                    print("Produto não encontrado ou erro ao buscar valor unitário.")
            else:
                print("Preencha ambos os campos: código e quantidade.")
        else:
            if len(Código) == 5:
                if Código and Quantidade:  
                    valor_unitario = GetValueProduto(Código)
                    if valor_unitario is not None: 
                        quantidade = Decimal(Quantidade) 
                        valor_total = valor_unitario * quantidade  
                        ui.line_total_venda.setText(f'R$: {float(valor_total):.2f}')  
                    else:
                        print("Produto não encontrado ou erro ao buscar valor unitário.")
                else:
                    print("Preencha ambos os campos: código e quantidade.")
            else:
                print("Código precisa ter 5 dígitos")
                
    except Exception as e:
        print(f"Erro ao calcular o valor total: {e}")

