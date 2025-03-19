from functions.events.DabaseEvents.Cadastro import *
from functions.events.dialogBox.dialogedit import adicionar_produtos, verificar_texto_apagado
from functions.events.dialogBox.filteredit import iniciarFiltro
from functions.events.DabaseEvents.Excluir import *
from functions.events.searchs.ColaboradorSearch import *
from functions.events.DabaseEvents.Alterar import *
from functions.events.searchs.ColaboradorSearch import filtrar_tabela_colaboradores, reexibir_tabela_colaboradores
from functions.events.DabaseEvents.Exports import *
from functions.events.NavEvents.filtro import alternar_filtro_e_atualizar_botao

def conect_button(ui, parent):
    ui.btn_cadastro.clicked.connect(lambda: CadastroUsuario(ui))
    ui.btn_finalizar_cadastro.clicked.connect(lambda: CadastroProduto(ui))
    ui.btn_exluir_colaboradores.clicked.connect(lambda: ExcluirColaboradores(ui))
    ui.btn_excluir_produto.clicked.connect(lambda: ExcluirProdutos(ui))
    ui.btn_adicionar_produtos_event.clicked.connect(lambda: adicionar_produtos(ui, parent))
    ui.admin_button.clicked.connect(lambda: selecionar_admin(ui))
    ui.colaborador_button.clicked.connect(lambda:selecionar_colaborador(ui))
    ui.btn_ver_senha.clicked.connect(lambda: alternar_visibilidade_senha(ui))
    ui.btn_finalizar_alterar_colaboradores.clicked.connect(lambda: AlterarColaboradores(ui))    
    ui.btn_finalizar_alterar.clicked.connect(lambda:AlterarProdutos(ui))
    ui.btn_custom_filter.clicked.connect(lambda:iniciarFiltro(parent))
    ui.line_search_bar_colaboradores.returnPressed.connect(lambda: filtrar_tabela_colaboradores(ui, 1))
    ui.line_search_bar_buscar_colaboradores.returnPressed.connect(lambda: filtrar_tabela_colaboradores(ui, 2))
    ui.line_search_bar_colaboradores.textChanged.connect(lambda: reexibir_tabela_colaboradores(ui, 1) if ui.line_search_bar_colaboradores.text().strip() == "" else None)
    ui.line_search_bar_buscar_colaboradores.textChanged.connect(lambda: reexibir_tabela_colaboradores(ui, 2) if ui.line_search_bar_buscar_colaboradores.text().strip() == "" else None)
    ui.btn_gerar_excel.clicked.connect(lambda: exportar_para_excel(ui))
    ui.btn_gerar_pdf.clicked.connect(lambda: exportar_para_pdf(ui.tabela_monitoramento))
    ui.btn_filtro_vendas.clicked.connect(lambda: alternar_filtro_e_atualizar_botao(ui))
    ui.btn_finalizar_venda.clicked.connect(lambda: CadastroVenda(ui))
    ui.line_produtos_block.textChanged.connect(lambda: verificar_texto_apagado(ui))
    ui.btn_finalizar_cadastro_evento.clicked.connect(lambda: CadastrarEvento(ui))    

