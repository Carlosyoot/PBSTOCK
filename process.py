import sys
import os

def executar_setup():
    # Caminho para o setup.exe (que será incluído no executável)
    if getattr(sys, 'frozen', False):
        # Se o código estiver rodando como um executável
        diretorio_base = sys._MEIPASS
    else:
        # Se estiver rodando como script Python normal
        diretorio_base = os.path.dirname(os.path.abspath(__file__))

    caminho_setup = os.path.join(diretorio_base, 'setup.exe')

    # Executa o setup.exe diretamente
    try:
        os.system(caminho_setup)
        print("Setup.exe executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar setup.exe: {e}")

if __name__ == "__main__":
    print("Executando o programa principal...")
    executar_setup()