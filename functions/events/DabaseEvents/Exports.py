import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side
from openpyxl.utils import get_column_letter



def exportar_para_excel(ui, nome_arquivo="tabela_monitoramento.xlsx"):
    """
    Exporta a tabela_monitoramento para um arquivo Excel.

    :param ui: Interface do usuário (contendo a tabela_monitoramento).
    :param nome_arquivo: Nome do arquivo Excel a ser gerado.
    """
    try:
        # Coleta os dados da tabela
        dados = []
        colunas = []

        # Obtém os cabeçalhos da tabela
        for col in range(ui.tabela_monitoramento.columnCount()):
            colunas.append(ui.tabela_monitoramento.horizontalHeaderItem(col).text())

        # Obtém os dados da tabela
        for row in range(ui.tabela_monitoramento.rowCount()):
            linha = []
            for col in range(ui.tabela_monitoramento.columnCount()):
                item = ui.tabela_monitoramento.item(row, col)
                if item is not None:
                    linha.append(item.text())
                else:
                    linha.append("")  # Célula vazia
            dados.append(linha)

        # Cria um DataFrame do pandas
        df = pd.DataFrame(dados, columns=colunas)

        # Cria um arquivo Excel usando openpyxl
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Monitoramento', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Monitoramento']

            # Define larguras de coluna (3,00 cm para todas, 4,00 cm para a última)
            col_widths = [17] * (len(colunas))  # 3,00 cm para todas as colunas
            col_widths[-1] = 17.07  # 4,00 cm para a última coluna

            for i, width in enumerate(col_widths, start=1):
                col_letter = get_column_letter(i)
                worksheet.column_dimensions[col_letter].width = width

            # Estilo de cabeçalho: cor cinza claro
            cinza_claro = PatternFill(start_color='D3D3D3', end_color='D3D3D3', fill_type='solid')

            # Estilo de borda
            borda = Border(left=Side(style='thin'),
                           right=Side(style='thin'),
                           top=Side(style='thin'),
                           bottom=Side(style='thin'))

            # Aplica o estilo ao cabeçalho
            for col_num, cell in enumerate(worksheet[1], start=1):
                cell.fill = cinza_claro
                cell.border = borda

            # Aplica bordas às células com dados
            for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
                for cell in row:
                    cell.border = borda

        print(f"Tabela exportada para {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao exportar para Excel: {e}")
        
def exportar_para_pdf(tabela, nome_arquivo="tabela_monitoramento.pdf"):
    """Exporta a tabela para PDF."""
    try:
        dados = [[tabela.horizontalHeaderItem(col).text() for col in range(tabela.columnCount())]]
        for row in range(tabela.rowCount()):
            linha = [tabela.item(row, col).text() if tabela.item(row, col) else "" for col in range(tabela.columnCount())]
            dados.append(linha)
        pdf = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        tabela_pdf = Table(dados)
        tabela_pdf.setStyle(estilo_tabela)
        pdf.build([tabela_pdf])
        print(f"Tabela exportada para {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao exportar para PDF: {e}")
        
