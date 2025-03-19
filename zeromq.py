import pymysql
import time
import threading
from dbutils.pooled_db import PooledDB
import zmq
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuração do pool de conexões
pool = PooledDB(
    creator=pymysql,
    host='localhost',
    port=3306,
    user='root',
    password='',
    db='pbstock',
    maxconnections=10,
    mincached=2,
    maxcached=5,
    blocking=True,
    maxusage=None,
    setsession=[]
)

def start_zeromq():
    """Inicia o loop do ZeroMQ para monitoramento do banco de dados."""
    context = zmq.Context.instance()
    socket = context.socket(zmq.PUB)  # Socket de publicação
    socket.bind("tcp://*:5555")  # Escuta na porta 5555

    print("Publicador iniciado. Monitorando mudanças no banco de dados...")

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MAX(id) FROM log_mudancas")
            ultimo_id = cursor.fetchone()[0] or 0  

    while True:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, tabela, tipo_mudanca, data_modificacao FROM log_mudancas WHERE id > %s ORDER BY id", (ultimo_id,))
                    mudancas = cursor.fetchall()

                    for mudanca in mudancas:
                        id_mudanca, tabela, tipo_mudanca, data_modificacao = mudanca
                        mensagem = f"{tipo_mudanca}:{tabela}"
                        socket.send_string(mensagem)
                        print(f"Notificação enviada: {mensagem}")
                        ultimo_id = id_mudanca

                    cursor.execute("SELECT COUNT(*) FROM log_mudancas")
                    num_linhas = cursor.fetchone()[0]
                    if num_linhas > 60:
                        cursor.execute("DELETE FROM log_mudancas")
                        cursor.execute("ALTER TABLE log_mudancas AUTO_INCREMENT = 1")
                        conn.commit()
                        socket.send_string("Renovação Log")
                        print("Tabela limpa e IDs reiniciados.")
                        ultimo_id = 0  

        except Exception as e:
            print(f"Erro ao verificar mudanças no banco de dados: {e}")

        time.sleep(1)  # Verifica a cada 1 segundo
