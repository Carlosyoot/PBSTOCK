import sys
import subprocess
import socket
import ctypes
import psutil
import os
import time
import atexit

def enviar_notificacao(titulo, mensagem):
    """Exibe uma caixa de diálogo no Windows."""
    ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, 0x10)  # 0x10 = Ícone de erro

def matar_processo_na_porta(porta):
    """Mata o processo que está utilizando a porta especificada no Windows."""
    try:
        netstat_output = subprocess.check_output(["netstat", "-ano"], text=True, shell=True)

        for line in netstat_output.splitlines():
            if f":{porta}" in line:
                parts = line.split()
                pid = parts[-1]  

                try:
                    pid = int(pid)
                    processo = psutil.Process(pid)
                    processo.terminate()  
                    processo.wait(timeout=5)  
                    print(f"Processo {pid} na porta {porta} foi encerrado.")
                    return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

        print(f"Nenhum processo encontrado na porta {porta}.")
        return False
    except Exception as e:
        print(f"Erro ao matar processo na porta {porta}: {e}")
        return False

def iniciar_subprocesso(script):
    """Inicia um subprocesso de forma segura."""
    try:
        return subprocess.Popen(
            [sys.executable, os.path.join(script_dir, script)],
            start_new_session=True  # Evita processos órfãos
        )
    except Exception as e:
        print(f"Erro ao iniciar {script}: {e}")
        return None

def finalizar_processos():
    """Encerra todos os subprocessos ao sair."""
    for processo in [loading_process, zeromq_process, setup_process]:
        if processo and processo.poll() is None:  # Se ainda estiver rodando
            print(f"Encerrando {processo.args[-1]}...")
            processo.terminate()
            try:
                processo.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"Forçando encerramento de {processo.args[-1]}")
                processo.kill()

def main():
    global script_dir, loading_process, zeromq_process, setup_process
    
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if matar_processo_na_porta(5555):
        print("Processo na porta 5555 foi encerrado.")
    else:
        print("Nenhum processo encontrado na porta 5555.")

    # Inicia subprocessos
    loading_process = iniciar_subprocesso("a.py")
    zeromq_process = iniciar_subprocesso("zeromq.py")
    setup_process = iniciar_subprocesso("setup.py")

    # Garante que os processos sejam encerrados ao sair
    atexit.register(finalizar_processos)

    # Configura socket para comunicação com setup.py
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 5000))
        s.listen()

        print("Aguardando setup.py...")
        timeout = 300  # 5 minutos
        start_time = time.time()

        while time.time() - start_time < timeout:
            if setup_process.poll() is not None:  # Se setup.py terminou
                if setup_process.returncode != 0:
                    print("Erro: setup.py falhou.")
                    enviar_notificacao("Erro no Servidor", "O setup.py falhou ao iniciar.")
                
                # Finaliza loading.py
                if loading_process and loading_process.poll() is None:
                    loading_process.terminate()
                    loading_process.wait()
                
                break  # Sai do loop

            # Espera mensagem do setup.py
            s.settimeout(1)
            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data == b"ready":
                        print("Janela PyQt5 criada com sucesso!")

                        # Encerra loading.py quando setup.py está pronto
                        if loading_process and loading_process.poll() is None:
                            loading_process.terminate()
                            loading_process.wait()

                        break  # Sai do loop
            except socket.timeout:
                continue  # Continua esperando

    # **Mantém zeromq.py rodando enquanto setup.py estiver ativo**
    print("Monitorando setup.py...")
    while setup_process.poll() is None:  
        try:
            setup_process.wait(timeout=1)  # Espera 1 segundo antes de checar novamente
        except subprocess.TimeoutExpired:
            continue  # Continua monitorando

    # **Agora que setup.py terminou, encerra zeromq.py**
    if zeromq_process and zeromq_process.poll() is None:
        zeromq_process.terminate()
        zeromq_process.wait()
        print("zeromq.py foi encerrado.")

if __name__ == "__main__":
    main()
