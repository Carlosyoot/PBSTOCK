import os
import subprocess

def list_files_and_directories_in_current_folder():
    """
    Lista todos os arquivos e diretórios no nível atual da execução do script.
    """
    current_directory = os.getcwd()  # Obtém o diretório atual de execução
    items = []  # Lista que irá armazenar arquivos e diretórios
    
    # Percorre todos os itens no diretório atual
    for item in os.listdir(current_directory):
        # Adiciona todos os itens (arquivos e diretórios)
        items.append(item)
    
    return items

def generate_requirements_txt():
    """
    Gera um arquivo `requirements.txt` com as dependências instaladas no ambiente.
    """
    try:
        # Executa o comando 'pip freeze' para obter as dependências
        result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            # Salva as dependências no arquivo requirements.txt
            with open('requirements.txt', 'w') as f:
                f.write(result.stdout)
            print("requirements.txt gerado com sucesso!")
        else:
            print(f"Erro ao gerar requirements.txt: {result.stderr}")
    except Exception as e:
        print(f"Erro ao gerar requirements.txt: {str(e)}")

if __name__ == "__main__":
    # Listando todos os arquivos e diretórios no nível atual
    items = list_files_and_directories_in_current_folder()
    print("Arquivos e Diretórios no nível atual de execução:")
    for item in items:
        print(item)
    
    # Gerando o arquivo requirements.txt
    generate_requirements_txt()
