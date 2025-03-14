import sys
import subprocess
import socket
import ctypes

def enviar_notificacao(titulo, mensagem):
    """Exibe uma caixa de diálogo no Windows."""
    ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, 0x10)  # 0x10 = Ícone de erro

def main():
    # Inicia o loading.py como um subprocesso
    loading_process = subprocess.Popen([sys.executable, "a.py"])

    # Inicia o setup.py como um subprocesso
    setup_process = subprocess.Popen([sys.executable, "setup.py"])

    # Configura um socket para receber a mensagem do setup.py
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 5000))  # Escuta na porta 5000
        s.listen()

        # Aguarda uma conexão do setup.py ou verifica se ele falhou
        print("Aguardando setup.py...")
        while True:
            # Verifica se o setup.py terminou (com ou sem erro)
            if setup_process.poll() is not None:
                if setup_process.returncode != 0:  # Se o setup.py falhou
                    print("Erro: setup.py falhou.")
                    if loading_process.poll() is None:  # Se o loading.py ainda estiver rodando
                        loading_process.terminate()  # Encerra o loading.py imediatamente
                        loading_process.wait()  # Aguarda o término do processo
                    enviar_notificacao("Erro no Servidor", "O setup.py falhou ao iniciar.")  # Notificação de erro
                break  # Sai do loop

            # Verifica se há uma conexão do setup.py
            s.settimeout(1)  # Timeout para não bloquear indefinidamente
            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data == b"ready":
                        print("Janela PyQt5 criada com sucesso!")
                        if loading_process.poll() is None:  # Se o loading.py ainda estiver rodando
                            loading_process.terminate()  # Encerra o loading.py
                            loading_process.wait()  # Aguarda o término do processo
                        break  # Sai do loop
            except socket.timeout:
                continue  # Continua esperando

if __name__ == "__main__":
    main()