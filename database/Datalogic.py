import pymysql
from dbutils.pooled_db import PooledDB
from fastapi import HTTPException
import hashlib




import logging
from datetime import datetime, timedelta


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuração do pool de conexões
pool = PooledDB(
    creator=pymysql,       # O driver do banco de dados PyMySQL
    host='localhost',       # Endereço do MySQL
    port=3306,              # Porta do MySQL
    user='root',            # Nome de usuário
    password='',            # Senha (se houver)
    db='pbstock',           # Nome do banco de dados
    maxconnections=10,      # Número máximo de conexões abertas no pool
    mincached=2,            # Número mínimo de conexões mantidas no pool
    maxcached=5,            # Número máximo de conexões em cache
    blocking=True,          # Espera por uma conexão disponível caso o pool esteja cheio
    maxusage=None,          # Número máximo de usos de uma conexão antes de ser fechada
    setsession=[]           # Comandos para configurar a sessão do MySQL
)

# Obtendo uma conexão do pool
connection = pool.connection()

def DeleteUsers(Name, User):
    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usuários WHERE Nome = %s AND Login = %s', (Name, User))
            conn.commit()
            return {"message": "Usuário excluído com sucesso"}

    except Exception as e:
        conn.rollback()
        print(f"Erro ao excluir: {e}")
        return {"message": "Erro ao excluir usuário."}
    
def DeleteProduto(produto, id):
    try:
        print("Delete", produto, id)
        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Produtos WHERE Produto = %s AND Id_produto = %s', (produto, id))
            conn.commit()
            return {"message": "Usuário excluído com sucesso"}

    except Exception as e:
        conn.rollback()
        print(f"Erro ao excluir: {e}")
        return {"message": "Erro ao excluir usuário."}

def AdicionarUsuario(Name, Nasc, Cpf, User, Password, Tip):
    start_time = datetime.now()

    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = """
            INSERT INTO `pbstock`.`usuários`
            (`Nome`, `Data Nasc`, `CPF`, `Login`, `Senha`, `Privileges`)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            query_start_time = datetime.now()
            cursor.execute(query, (Name, Nasc, Cpf, User, Password, Tip))
            query_execution_time = datetime.now() - query_start_time

            conn.commit()

            total_execution_time = datetime.now() - start_time

            print(f"Tempo de Conexão: {connection_time.total_seconds()} segundos")
            print(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")
            print(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            return {"message": "Usuário adicionado com sucesso!"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar usuário: {e}")
    


def AdicionarProduto(Produto, Cód, Quantidade, Valor, Descrição, Data, Condição='Ativo', TIP='Produto'):
    start_time = datetime.now()
    Formated = Data.strftime("%Y-%m-%d %H:%M:%S")

    try:
        logger.debug(f"Adicionando produto: Produto={Produto}, Cód={Cód}, Quantidade={Quantidade}, Valor={Valor}, Descrição={Descrição}, Condição={Condição}, TIP={TIP}, Data={Formated}")

        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time
            logger.debug(f"Tempo de Conexão: {connection_time.total_seconds()} segundos")

            query = """
            INSERT INTO `pbstock`.`produtos`
            (`Produto`, `Cód`, `Quantidade`, `ValorUn`, `Descrição`, `Data`, `Condição`, `TIP`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            query_start_time = datetime.now()
            cursor.execute(query, (Produto, Cód, Quantidade, Valor, Descrição, Formated, Condição, TIP))
            query_execution_time = datetime.now() - query_start_time
            logger.debug(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")

            conn.commit()

            total_execution_time = datetime.now() - start_time
            logger.debug(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            return {"message": "Produto adicionado com sucesso!"}

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        logger.error(f"Erro ao adicionar produto: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar produto: {e}")



def AlterarUsuario(Id, Name, Nasc, User, Password):
    start_time = datetime.now()

    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = """
            UPDATE `pbstock`.`usuários`
            SET `Nome` = %s, `Data Nasc` = %s, `Login` = %s, `Senha` = %s
            WHERE `Id` = %s
            """

            query_start_time = datetime.now()
            cursor.execute(query, (Name, Nasc, User, Password, Id))  
            query_execution_time = datetime.now() - query_start_time

            conn.commit()

            total_execution_time = datetime.now() - start_time

            print(f"Tempo de Conexão: {connection_time.total_seconds()} segundos")
            print(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")
            print(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            return {"message": "Usuário atualizado com sucesso!"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar usuário: {e}")
    
def AlterarProduto(Id, Nome, Quantidade, Valor, Descrição):
    start_time = datetime.now()
    
    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = """
            UPDATE `pbstock`.`produtos`
            SET `Produto` = %s, `Quantidade` = %s, `ValorUn` = %s, `Descrição` = %s
            WHERE `Id_produto` = %s
            """

            query_start_time = datetime.now()
            cursor.execute(query, (Nome, Quantidade, Valor, Descrição, Id))  
            query_execution_time = datetime.now() - query_start_time

            conn.commit()

            total_execution_time = datetime.now() - start_time

            print(f"Tempo de Conexão: {connection_time.total_seconds()} segundos")
            print(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")
            print(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            return {"message": "Produto atualizado com sucesso!"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {e}")
    
def DataGetAllColaboradoresNomes():
    try:
        with pool.connection() as conn:  
            with conn.cursor() as cursor: 
                cursor.execute('SELECT Nome FROM usuários')  
                nomes = cursor.fetchall()  
                
                
                return [nome[0] for nome in nomes]

    except Exception as e:
        print(f"Erro ao buscar nomes de colaboradores: {e}")
        return []  # Retorna uma lista vazia em caso de erro

def DataGetAllLogins():
    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuários')
            logins = cursor.fetchall()
            
            return logins

    except Exception as e:
        print(f"Erro ao buscar logins: {e}")
        return []
    
def GetProdutos():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Id_produto, Produto, Cód, Quantidade , ValorUn, Descrição, Condição FROM produtos"
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Verifica se a consulta retornou dados
                if not data:
                    return []  # Retorna uma lista vazia se não houver dados

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []

    
def GetQuantidadeProduto(product_id):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Quantidade FROM produtos WHERE Id_Produto = %s"
                cursor.execute(query, (product_id,))
                data = cursor.fetchall()
                
               
                if data:
                    return data[0][0]  
                else:
                    return []
                
    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return 0  # Retorna 0 em caso de erro

def UpdateStatus(product_id, Status):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                print('UPDATESTATUS', product_id, Status)

                # Atualizar a coluna 'Condição' (com crase para lidar com acentos)
                query = """
                UPDATE `pbstock`.`produtos`
                SET `Condição` = %s
                WHERE `id_produto` = %s
                """
                
                cursor.execute(query, (Status, product_id))
                
                # Garantir que as mudanças sejam salvas no banco
                conn.commit()

                # Verifique se alguma linha foi afetada
                if cursor.rowcount > 0:
                    print(f"Status atualizado para o produto ID {product_id}.")
                    return True
                else:
                    print(f"Nenhuma linha foi afetada. Verifique o ID do produto.")
                    return False

    except Exception as e:
        print(f"Erro ao atualizar o status do produto: {e}")
        return False  # Retorna False em caso de erro




    
def GetProdutoNomesCod():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Produto, Cód FROM produtos"
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Formatar os dados no formato "Produto - Cód"
                lista_produtos_cod = [f"{produto} - {cod}" for produto, cod in data]
                
                return lista_produtos_cod

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []
    
def GetProdutosAll():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Produto, Cód, Quantidade, ValorUn, Descrição FROM produtos"
                cursor.execute(query)
                data = cursor.fetchall()
                return data
    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []
    
def GetRecentsProduct():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Define a data limite (5 dias atrás)
                data_limite = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
                
                # Logs para depuração
                print("Data limite:", data_limite)
                print("Horário agora:", datetime.now())

                # Query SQL para buscar produtos recentes que não excederam 5 dias
                query = """
                SELECT Produto, Cód, Quantidade, ValorUn, Descrição, Data 
                FROM produtos 
                WHERE Data >= %s
                """
                cursor.execute(query, (data_limite,))
                data = cursor.fetchall()
                return data
    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []
    
def GetValueProduto(cod):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Consulta SQL para buscar o valor unitário e a quantidade do produto
                query = "SELECT ValorUn FROM produtos WHERE Cód = %s"
                cursor.execute(query, (cod,))  # Passa o código como parâmetro para evitar SQL injection
                result = cursor.fetchone()  # Busca apenas uma linha (já que estamos procurando por um código específico)

                if result:
                    valor_un = result[0]  # Pega o valor unitário (primeira coluna do resultado)
                    return valor_un  # Retorna apenas o valor unitário
                else:
                    print(f"Produto com código {cod} não encontrado.")
                    return None  # Retorna None se o produto não for encontrado

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return None  # Retorna None em caso de erro

    
def DataLoginUser(User, Password):
    
    start_time = datetime.now()

    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = "SELECT * FROM usuários WHERE Login = %s AND Senha = %s"
            query_start_time = datetime.now()
            cursor.execute(query, (User, Password))  # Usando parâmetros para evitar injeção de SQL
            query_execution_time = datetime.now() - query_start_time

            user = cursor.fetchone()  # Pega apenas o primeiro resultado (não precisa de um 'for' aqui)
            
            total_execution_time = datetime.now() - start_time

            print(f"Tempo de Conexão: {connection_time.total_seconds()} segundos")
            print(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")
            print(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            if user:
                return {'status': 'success', 'message': 'Bem-vindo, administrador!', 'redirect': 'admin'}
            else:
                return {'status': 'error', 'message': 'Usuário ou senha incorretos'}

    except Exception as e:
        print("Erro ao executar a consulta:", e)
        return {'status': 'error', 'message': str(e)}


