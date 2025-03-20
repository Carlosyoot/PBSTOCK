from collections import defaultdict
import pymysql
import time
from dbutils.pooled_db import PooledDB
from fastapi import HTTPException
import hashlib
import zmq
import ctypes
import logging
from datetime import datetime, timedelta


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


try:
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
    
    connection = pool.connection()
    
    
    
except pymysql.MySQLError as e:
    logger.error(f"Erro ao configurar o pool de conexões: {e}")
    ctypes.windll.user32.MessageBoxW(0, 'Não foi possível iniciar\nBanco de dados não está presente', 'Erro ao conectar ao servidor', 0x10)  # 0x10 = Ícone de erro
# Tentando obter uma conexão do pool

# Obtendo uma conexão do pool



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
            (`Produto`, `Cód`, `Quantidade`, `ValorUn`, `Descrição`, `Data`,`Quantidade_Disponível`, `Condição`, `TIP`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
            """

            query_start_time = datetime.now()
            cursor.execute(query, (Produto, Cód, Quantidade, Valor, Descrição, Formated, Quantidade, Condição, TIP))
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
    
    
def AdicionarVenda(Quantidade, Vendedor, Data, Valor_Total, ID_Produto=None, ID_Produto_Evento=None):
    if not ID_Produto and not ID_Produto_Evento:
        raise HTTPException(status_code=400, detail="É necessário informar pelo menos um dos IDs: ID_Produto ou ID_Produto_Evento")

    start_time = datetime.now()
    Formated = Data.strftime("%Y-%m-%d %H:%M:%S")

    try:
        logger.debug(f"Adicionando venda: ID_Produto={ID_Produto}, ID_Produto_Evento={ID_Produto_Evento}, Quantidade={Quantidade}, Vendedor={Vendedor}, Data={Formated}, Valor_Total={Valor_Total}")

        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time
            logger.debug(f"Tempo de Conexão: {connection_time.total_seconds()} segundos")

            Produto = None
            ValorUn = None

            if ID_Produto:
                cursor.execute("SELECT Produto, ValorUn FROM pbstock.produtos WHERE Cód = %s", (ID_Produto,))
                resultado = cursor.fetchone()
                if resultado:
                    Produto, ValorUn = resultado
                else:
                    raise HTTPException(status_code=404, detail="Produto não encontrado.")
            elif ID_Produto_Evento:
                cursor.execute("SELECT Produto, ValorPromocional FROM pbstock.produtos_eventos WHERE Cód = %s", (ID_Produto_Evento,))
                resultado = cursor.fetchone()
                if resultado:
                    Produto, ValorUn = resultado
                else:
                    raise HTTPException(status_code=404, detail="Produto de evento não encontrado.")

            query = """
            INSERT INTO `pbstock`.`vendas`
            (`ID_PRODUTO`, `ID_PRODUTO_EVENTO`, `Produto`, `Valor Un`, `Quantidade_vendida`, `Vendedor`, `Data`, `Valor_total`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            query_start_time = datetime.now()
            cursor.execute(query, (ID_Produto, ID_Produto_Evento, Produto, ValorUn, Quantidade, Vendedor, Formated, Valor_Total))
            query_execution_time = datetime.now() - query_start_time
            logger.debug(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")

            conn.commit()

            total_execution_time = datetime.now() - start_time
            logger.debug(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            return {"message": "Venda adicionada com sucesso!"}

    except HTTPException as e:
        raise e 
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        logger.error(f"Erro ao adicionar venda: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar venda: {e}")






def AlterarUsuario(Id, Name, Nasc, User, Password, CPF):
    start_time = datetime.now()

    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = """
            UPDATE `pbstock`.`usuários`
            SET `Nome` = %s, `Data Nasc` = %s, `Login` = %s, `Senha` = %s, `CPF` = %s
            WHERE `Id` = %s
            """

            query_start_time = datetime.now()
            cursor.execute(query, (Name, Nasc, User, Password, CPF, Id))  
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
    
    
def AlterarProdutoEvento(Id, Nome, Quantidade, Valor, Descrição):
    start_time = datetime.now()
    
    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = """
            UPDATE `pbstock`.`produtos_eventos`
            SET `Produto` = %s, `Quantidade` = %s, `ValorPromocional` = %s, `Descrição` = %s
            WHERE `id_produto_evento` = %s
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
        return [] 
def DataGetAllLogins():
    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuários')
            logins = cursor.fetchall()
            
           
            if not logins:
                return ['vazio']
            
            return logins

    except Exception as e:
        print(f"Erro ao buscar logins: {e}")
        return []  

    
def GetProdutos():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Id_produto, Produto, Cód, Quantidade_Disponível , ValorUn, Descrição, Condição FROM produtos"
                cursor.execute(query)
                data = cursor.fetchall()
                
                
                if not data:
                    return []  

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []
    
def GetProdutosEvento():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id_produto_evento, Produto, Cód, Quantidade_Disponível , ValorPromocional, Descrição, Condição FROM produtos_eventos"
                cursor.execute(query)
                data = cursor.fetchall()
                
              
                if not data:
                    return [] 
                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []
    
def GetProdutosVendas():
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT Produto, Quantidade_vendida, Vendedor, Data, Valor_total, `Valor Un`
                FROM vendas
                """
                cursor.execute(query)
                data = cursor.fetchall()
                
                
                if not data:
                    return []  

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela vendas: {e}")
        return []
    
    
def GetAllEventos():
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT id_evento, nome, data_inicio, data_fim, descricao
                FROM eventos
                """
                cursor.execute(query)
                data = cursor.fetchall()
                
         
                if not data:
                    return [] 

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela vendas: {e}")
        return []
    
def GetContagemProduto(id_evento):
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT COUNT(*) 
                    FROM produtos_eventos 
                    WHERE id_evento = %s
                """
                cursor.execute(query, (id_evento,))
                contagem = cursor.fetchone()[0] 
                return contagem
    except Exception as e:
        print(f"Erro ao contar produtos do evento {id_evento}: {e}")
        return 0  
def inserir_mudanca_card_init():
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:

                tabela = 'card tela'
                tipo_mudanca = 'CARD'
                data_modificacao = datetime.now()  

              
                query = """
                    INSERT INTO log_mudancas (tabela, tipo_mudanca, data_modificacao)
                    VALUES (%s, %s,%s)
                """

               
                cursor.execute(query, (tabela, tipo_mudanca, data_modificacao))

               
                conn.commit()

                print("Registro inserido com sucesso!")
                
                return

    except Exception as e:
       
        conn.rollback()
        print(f"Erro ao inserir registro: {e}")


    
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
        return 0 
def GetQuantidadeProdutoEvento(product_id):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Quantidade FROM produtos_eventos WHERE id_produto_evento = %s"
                cursor.execute(query, (product_id,))
                data = cursor.fetchall()
                
               
                if data:
                    return data[0][0]  
                else:
                    return []
                
    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return 0  
    
def VerificarSeProdutoEhEvento(id_produto):
  
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id_produto_evento FROM produtos_eventos WHERE id_produto_evento = %s"
                cursor.execute(query, (id_produto,))
                data = cursor.fetchone()

                if data:
                    return True 
                else:
                    return False  

    except Exception as e:
        print(f"Erro ao verificar se o produto é de um evento: {e}")
        return False    
    
    

def UpdateStatus(id_produto, status):
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
              
                query_verificar_evento = "SELECT id_produto_evento FROM produtos_eventos WHERE id_produto_evento = %s"
                cursor.execute(query_verificar_evento, (id_produto,))
                is_evento = cursor.fetchone() is not None

                if is_evento:
                    query = "UPDATE produtos_eventos SET Condição = %s WHERE id_produto_evento = %s"
                else:
                    query = "UPDATE produtos SET Condição = %s WHERE Id_Produto = %s"

                cursor.execute(query, (status, id_produto))
                conn.commit()

    except Exception as e:
        print(f"Erro ao atualizar status do produto {id_produto}: {e}")
        raise


def UpdateStock(id, quantidade):
   
    try:
        print("updatestock", id, quantidade)

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                UPDATE pbstock.produtos
                SET Quantidade = %s, 
                Quantidade_Disponível = Quantidade_Disponível + %s
                WHERE Id_produto = %s
                """
                cursor.execute(query, (quantidade, quantidade, id))

                conn.commit()

        print("Status atualizado para o produto ID", id)
        return True

    except Exception as e:
        print(f"Erro ao atualizar o estoque: {e}")
        return False
    
def UpdateStockEvento(id, quantidade):
    """
    Atualiza a quantidade e a quantidade disponível de um produto no banco de dados.
    """
    try:
        print("updatestock", id, quantidade)

       
        with pool.connection() as conn:
         
            with conn.cursor() as cursor:
               
                query = """
                UPDATE pbstock.produtos_eventos
                SET Quantidade = %s, 
                Quantidade_Disponível = Quantidade_Disponível + %s
                WHERE id_produto_evento = %s
                """
               
                cursor.execute(query, (quantidade, quantidade, id))

             
                conn.commit()

        print("Status atualizado para o produto ID", id)
        return True

    except Exception as e:
        print(f"Erro ao atualizar o estoque: {e}")
        return False
    

def DecrementarEstoque(Quantidade_vendida, cod, filtro):
  
    start_time = datetime.now()

    try:
       
        Quantidade_vendida = int(Quantidade_vendida)

     
        if filtro == 'produto':
            tabela = 'produtos'
        elif filtro == 'produto evento':
            tabela = 'produtos_eventos'
        else:
            raise HTTPException(status_code=400, detail="Filtro inválido. Use 'produto' ou 'produto evento'.")

       
        query_busca = f"SELECT Quantidade_Disponível FROM pbstock.{tabela} WHERE Cód = %s"

        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query_busca, (cod,))
            resultado = cursor.fetchone()

            if not resultado:
                raise HTTPException(status_code=404, detail="Produto não encontrado.")

            quantidade_atual = resultado[0]

    
            if Quantidade_vendida > quantidade_atual:
                return "Quantidade insuficiente em estoque."

           
            nova_quantidade = max(quantidade_atual - Quantidade_vendida, 0)
            novo_status = 'Esgotado' if nova_quantidade == 0 else 'Ativo'


            query_update = f"""
            UPDATE pbstock.{tabela}
            SET Quantidade_Disponível = %s, Condição = %s
            WHERE Cód = %s
            """

            query_start_time = datetime.now()
            cursor.execute(query_update, (nova_quantidade, novo_status, cod))
            conn.commit()
            query_execution_time = datetime.now() - query_start_time

            total_execution_time = datetime.now() - start_time

            logger.debug(f"Tempo de Execução da Query: {query_execution_time.total_seconds()} segundos")
            logger.debug(f"Tempo Total de Execução: {total_execution_time.total_seconds()} segundos")

            return {"message": "Estoque atualizado com sucesso!"}

    except ValueError:
        raise HTTPException(status_code=400, detail="A quantidade vendida deve ser um número inteiro.")
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        logger.error(f"Erro ao decrementar estoque: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao decrementar estoque: {e}")



    
def GetProdutoNomesCod():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
              
                query_produtos = """
                    SELECT Produto, Cód FROM produtos
                """
                cursor.execute(query_produtos)
                data_produtos = cursor.fetchall()

              
                query_produtos_eventos = """
                    SELECT Produto, Cód FROM produtos_eventos
                """
                cursor.execute(query_produtos_eventos)
                data_produtos_eventos = cursor.fetchall()

                combined_data = data_produtos + data_produtos_eventos

             
                lista_produtos_cod = [f"{produto} - {cod}" for produto, cod in combined_data]

                return lista_produtos_cod

    except Exception as e:
        print(f"Erro ao obter dados das tabelas Produto e Produtos_Eventos: {e}")
        return []
    
    
def getVendas():
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Produto FROM vendas"
                cursor.execute(query)
                data = cursor.fetchall()
                
                produtos_unicos = list(set([item[0] for item in data])) 
                return produtos_unicos
    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []  

def GetProdutoNomesCodAtivo():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
              
                query_produtos = """
                    SELECT Produto, Cód FROM produtos WHERE Condição = 'Ativo'
                """
                cursor.execute(query_produtos)
                data_produtos = cursor.fetchall()

                query_produtos_eventos = """
                    SELECT Produto, Cód, id_evento FROM produtos_eventos WHERE Condição = 'Ativo'
                """
                cursor.execute(query_produtos_eventos)
                data_produtos_eventos = cursor.fetchall()

               
                eventos = {}
                if data_produtos_eventos:
                    
                    id_eventos = list(set([row[2] for row in data_produtos_eventos]))
                    
                    
                    query_eventos = """
                        SELECT id_evento, nome FROM eventos WHERE id_evento IN %s
                    """
                    cursor.execute(query_eventos, (tuple(id_eventos),))
                    eventos = {row[0]: row[1] for row in cursor.fetchall()}

                
                combined_data = []

               
                for produto, cod in data_produtos:
                    combined_data.append(f"{produto} - {cod}")

            
                for produto, cod, id_evento in data_produtos_eventos:
                    nome_evento = eventos.get(id_evento, "")
                    if nome_evento:
                        combined_data.append(f"{produto} - {nome_evento} - {cod}")
                    else:
                        combined_data.append(f"{produto} - {cod}")

                return combined_data

    except Exception as e:
        print(f"Erro ao obter dados das tabelas Produto e Produtos_Eventos: {e}")
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
    
def GetEventId():
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
    
def gerar_id_evento():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                data_atual = datetime.now()
                ano_mes = data_atual.strftime('%Y%m')  # Formato AAAAMM

                query = "SELECT id_evento FROM eventos WHERE id_evento LIKE %s ORDER BY id_evento DESC LIMIT 1"
                cursor.execute(query, (f"EVT{ano_mes}%",))
                ultimo_id = cursor.fetchone()

                if ultimo_id:
                    
                    ultimo_sequencial = int(ultimo_id[0][-4:]) 
                    novo_sequencial = ultimo_sequencial + 1
                else:
                    
                    novo_sequencial = 1

              
                codigo = f"{novo_sequencial:04d}"

                
                return f"EVT{ano_mes}-{codigo}"

    except Exception as e:
        print(f"Erro ao gerar ID do evento: {e}")
        return None
    
def AdicionarEvento(id_evento,nome, data_inicio, data_fim, descricao):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO eventos (id_evento, nome, data_inicio, data_fim, descricao)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (id_evento, nome, data_inicio, data_fim, descricao))
                conn.commit()
    except Exception as e:
        print(f"Erro ao cadastrar evento: {e}")
        return
    
def AdicionarProdutosEvento(id_evento, produtos):
   
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                for produto in produtos:
                   
                    nome_produto = produto[0]  
                    quantidade = produto[1]   
                    valor = produto[2]        
                    descricao_produto = produto[3]  
                    codigo_produto = produto[4] 

                    
                    data_atual = datetime.now()

                    
                    query = """
                        INSERT INTO produtos_eventos (
                            Produto, Cód, Quantidade, ValorPromocional, 
                            Descrição, Data, Quantidade_Disponível, id_evento
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        nome_produto,  
                        codigo_produto,   
                        quantidade,      
                        valor,            
                        descricao_produto, 
                        data_atual,       
                        quantidade,      
                        id_evento,        
                    ))
                conn.commit()
    except Exception as e:
        print(f"Erro ao cadastrar produtos: {e}")
        raise 

    
def GetUltimoCodigo():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Cód FROM produtos_eventos ORDER BY Cód DESC LIMIT 1"
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else None
    except Exception as e:
        print(f"Erro ao obter o último código da tabela Produto: {e}")
        return None
    
    
    
def GetRecentsProduct():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
              
                data_limite = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
                
                
                print("Data limite:", data_limite)
                print("Horário agora:", datetime.now())

            
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
        
        print('Código que chegou', cod)
        
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                if "EVT" in cod:
                    query = "SELECT ValorPromocional FROM produtos_eventos WHERE Cód = %s"
                else:
                    query = "SELECT ValorUn FROM produtos WHERE Cód = %s"
                
                cursor.execute(query, (cod,)) 
                result = cursor.fetchone()  
                if result:
                    valor_un = result[0] 
                    return valor_un 
                else:
                    print(f"Produto com código {cod} não encontrado.")
                    return None  

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return None 


    
def DataLoginUser(User, Password):
    from datetime import datetime

    start_time = datetime.now()

    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            connection_time = datetime.now() - start_time

            query = "SELECT * FROM usuários WHERE BINARY Login = %s AND BINARY Senha = %s"
            query_start_time = datetime.now()
            cursor.execute(query, (User, Password)) 
            query_execution_time = datetime.now() - query_start_time

            user = cursor.fetchone()  
            
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



def GetCardsInfo(intervalo):
    """
    Retorna os 3 produtos mais vendidos com base no intervalo de data especificado.

    Parâmetros:
        intervalo (str): Define o intervalo de data. Pode ser 'dia', 'semana', 'mes' ou 'total'.
                         Padrão: 'total'.

    Retorno:
        Lista de tuplas contendo (produto, quantidade_total) em ordem decrescente de quantidade.
    """
    start_time = datetime.now() 

    try:
       
        with pool.connection() as conn:
            cursor = conn.cursor()

           
            connection_time = datetime.now() - start_time

           
            if intervalo == 'dia':
                coluna = 'venda_dia'
            elif intervalo == 'semana':
                coluna = 'venda_semana'
            elif intervalo == 'mes':
                coluna = 'venda_mes'
            else: 
                coluna = 'venda_total'

            query_start_time = datetime.now()
            cursor.execute(f"""
                SELECT produto, {coluna}
                FROM vendas_produtos
                WHERE venda_total > 0  -- Sempre aplica a condição venda_total > 0
                ORDER BY {coluna} DESC
                LIMIT 3
            """)
            query_execution_time = datetime.now() - query_start_time  

            dados = cursor.fetchall()

            if not dados:
                return []

            resultado_formatado = [(produto, quantidade) for produto, quantidade in dados]

            total_execution_time = datetime.now() - start_time
            print(f"Tempo de Conexão: {connection_time.total_seconds():.4f} segundos")
            print(f"Tempo de Execução da Query: {query_execution_time.total_seconds():.4f} segundos")
            print(f"Tempo Total de Execução: {total_execution_time.total_seconds():.4f} segundos")

            return resultado_formatado

    except Exception as e:
        print(f"Erro ao processar os dados getcard: {e}")
        return []
    

def GetRecentSales():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT Produto, Quantidade_vendida, Vendedor
                    FROM vendas
                    ORDER BY Data DESC
                    LIMIT 3
                """
                cursor.execute(query)
                results = cursor.fetchall() 
                if results:
                    return results  
                else:
                    print("Nenhuma venda recente encontrada.")
                    return []  

    except Exception as e:
        print(f"Erro ao obter dados das vendas recentes: {e}")
        return [] 
def UpdateTimes():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
               
                agora = datetime.now().date()

                query = """
                SELECT proxima_mudanca_dia, proxima_mudanca_semana, proxima_mudanca_mes
                FROM atualizacao
                LIMIT 1
                """
                cursor.execute(query)
                result = cursor.fetchone()

                if not result or not all(result):
                    print("Nenhuma data de atualização definida, nada a fazer.")
                    return False

                proxima_dia, proxima_semana, proxima_mes = result

                if isinstance(proxima_dia, datetime):
                    proxima_dia = proxima_dia.date()
                if isinstance(proxima_semana, datetime):
                    proxima_semana = proxima_semana.date()
                if isinstance(proxima_mes, datetime):
                    proxima_mes = proxima_mes.date()

                if not (agora >= proxima_dia or agora >= proxima_semana or agora >= proxima_mes):
                    print("Nenhuma data de atualização atingida. Saindo da função sem alterações.")
                    return False

                if agora >= proxima_dia:
                    cursor.execute("UPDATE vendas_produtos SET venda_dia = 0")
                    nova_proxima_dia = agora + timedelta(days=1)
                    cursor.execute("""
                        UPDATE atualizacao
                        SET proxima_mudanca_dia = %s
                    """, (nova_proxima_dia.strftime("%Y-%m-%d"),))
                    print("Vendas do dia zeradas!")

                if agora >= proxima_semana:
                    cursor.execute("UPDATE vendas_produtos SET venda_semana = 0")
                    dias_ate_proxima_semana = 7 - agora.weekday()
                    nova_proxima_semana = agora + timedelta(days=dias_ate_proxima_semana)
                    cursor.execute("""
                        UPDATE atualizacao
                        SET proxima_mudanca_semana = %s
                    """, (nova_proxima_semana.strftime("%Y-%m-%d"),))
                    print("Vendas da semana zeradas!")

                if agora >= proxima_mes:
                    cursor.execute("UPDATE vendas_produtos SET venda_mes = 0")
                    primeiro_dia_proximo_mes = (agora.replace(day=1) + timedelta(days=32)).replace(day=1)
                    cursor.execute("""
                        UPDATE atualizacao
                        SET proxima_mudanca_mes = %s
                    """, (primeiro_dia_proximo_mes.strftime("%Y-%m-%d"),))
                    print("Vendas do mês zeradas!")

                conn.commit()
                return True

    except Exception as e:
        print(f"Erro ao verificar e zerar vendas: {e}")
        return False
    
    

def GetEventosAtivos():
    """
    Obtém a lista de eventos ativos.
    Retorna uma lista de tuplas contendo o nome e a data de início dos eventos.
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT nome, data_inicio FROM eventos"
                cursor.execute(query)
                data = cursor.fetchall()

                if not data:
                    return []
                
                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela Eventos: {e}")
        return []


def getevento():
    """
    Obtém a lista de eventos ativos.
    Retorna uma lista simples com os nomes dos eventos.
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT nome FROM eventos"
                cursor.execute(query)
                data = cursor.fetchall()

                return [evento[0] for evento in data] if data else []

    except Exception as e:
        print(f"Erro ao obter dados da tabela Eventos: {e}")
        return []



def GetItensForaEstoque():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT Produto, Data
                    FROM produtos
                    WHERE Condição = 'esgotado'
                    UNION
                    SELECT Produto, Data
                    FROM produtos_eventos
                    WHERE Condição = 'esgotado'
                """
                cursor.execute(query)
                data = cursor.fetchall()

                if not data:
                    return []

                return data

    except Exception as e:
        print(f"Erro ao obter dados dos produtos esgotados: {e}")
        return []
    
def ExcluirEvento(id_evento):
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM eventos WHERE id_evento = %s"
                cursor.execute(query, (id_evento,))
                conn.commit() 

                if cursor.rowcount > 0:
                    print(f"Evento com ID {id_evento} excluído com sucesso.")
                    return True
                else:
                    print(f"Nenhum evento encontrado com o ID {id_evento}.")
                    return False

    except Exception as e:
        print(f"Erro ao excluir evento: {e}")
        return False
    

    
#def excluir_venda(id_venda):
#    try:
#        with pool.connection() as conn:
#            with conn.cursor() as cursor:
#                # Obtém a venda
#                query = """
#                SELECT cod_produto, quantidade
#                FROM vendas
#                WHERE id = %s
#                """
#                cursor.execute(query, (id_venda,))
#                cod_produto, quantidade = cursor.fetchone()
#
#                # Exclui a venda
#                query = """
#                DELETE FROM vendas
#                WHERE id = %s
#                """
#                cursor.execute(query, (id_venda,))
#
#                # Atualiza os totais em vendas_produtos
#                query = """
#                UPDATE vendas_produtos
#                SET venda_dia = venda_dia - %s,
#                    venda_semana = venda_semana - %s,
#                    venda_mes = venda_mes - %s,
#                    venda_total = venda_total - %s
#                WHERE cod = %s
#                """
#                cursor.execute(query, (quantidade, quantidade, quantidade, quantidade, cod_produto))
#
#                # Confirma as alterações
#                conn.commit()
#                print(f"Venda ID {id_venda} excluída com sucesso!")
#                return True
#
#    except Exception as e:
#        print(f"Erro ao excluir venda: {e}")
#        return False
#    
#def editar_venda(id_venda, nova_quantidade):
#    try:
#        with pool.connection() as conn:
#            with conn.cursor() as cursor:
#                # Obtém a venda antiga
#                query = """
#                SELECT cod_produto, quantidade
#                FROM vendas
#                WHERE id = %s
#                """
#                cursor.execute(query, (id_venda,))
#                cod_produto, quantidade_antiga = cursor.fetchone()
#
#                # Calcula a diferença
#                diferenca = nova_quantidade - quantidade_antiga
#
#                # Atualiza a venda
#                query = """
#                UPDATE vendas
#                SET quantidade = %s
#                WHERE id = %s
#                """
#                cursor.execute(query, (nova_quantidade, id_venda))
#
#                # Atualiza os totais em vendas_produtos
#                query = """
#                UPDATE vendas_produtos
#                SET venda_dia = venda_dia + %s,
#                    venda_semana = venda_semana + %s,
#                    venda_mes = venda_mes + %s,
#                    venda_total = venda_total + %s
#                WHERE cod = %s
#                """
#                cursor.execute(query, (diferenca, diferenca, diferenca, diferenca, cod_produto))
#
#                # Confirma as alterações
#                conn.commit()
#                print(f"Venda ID {id_venda} editada com sucesso!")
#                return True
#
#    except Exception as e:
#        print(f"Erro ao editar venda: {e}")
#        return False