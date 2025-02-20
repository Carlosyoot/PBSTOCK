import re

def corrigir_stylesheet(codigo):
    # Junta todas as linhas que fazem parte de um setStyleSheet em uma única linha
    codigo_corrigido = re.sub(r'(\.setStyleSheet\(")(.*?)("\))', lambda m: m.group(1) + m.group(2).replace('\n', '').replace('    ', '') + m.group(3), codigo, flags=re.DOTALL)
    return codigo_corrigido

# Ler o código do arquivo original
with open("FRMadmin.py", "r", encoding="utf-8") as f:
    codigo_original = f.read()

# Aplicar a correção
codigo_formatado = corrigir_stylesheet(codigo_original)

# Salvar o código corrigido em um novo arquivo
with open("seu_codigo_corrigido.py", "w", encoding="utf-8") as f:
    f.write(codigo_formatado)

print("Código corrigido e salvo como 'seu_codigo_corrigido.py'.")
