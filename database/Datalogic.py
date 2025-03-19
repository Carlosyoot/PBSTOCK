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

            # Inicializa as variáveis para Produto e Valor Un
            Produto = None
            ValorUn = None

            # Busca Produto e ValorUn na tabela correspondente
            if ID_Produto:
                # Busca na tabela produtos
                cursor.execute("SELECT Produto, ValorUn FROM pbstock.produtos WHERE Cód = %s", (ID_Produto,))
                resultado = cursor.fetchone()
                if resultado:
                    Produto, ValorUn = resultado
                else:
                    raise HTTPException(status_code=404, detail="Produto não encontrado.")
            elif ID_Produto_Evento:
                # Busca na tabela produtos_eventos
                cursor.execute("SELECT Produto, ValorPromocional FROM pbstock.produtos_eventos WHERE Cód = %s", (ID_Produto_Evento,))
                resultado = cursor.fetchone()
                if resultado:
                    Produto, ValorUn = resultado
                else:
                    raise HTTPException(status_code=404, detail="Produto de evento não encontrado.")

            # Query de inserção com os novos campos
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
        raise e  # Re-lança exceções HTTPException
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
        return []  # Retorna uma lista vazia em caso de erro

def DataGetAllLogins():
    try:
        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuários')
            logins = cursor.fetchall()
            
            # Se não houver registros, retorna ['vazio']
            if not logins:
                return ['vazio']
            
            return logins

    except Exception as e:
        print(f"Erro ao buscar logins: {e}")
        return []  # Retorna uma lista vazia em caso de erro

    
def GetProdutos():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Id_produto, Produto, Cód, Quantidade_Disponível , ValorUn, Descrição, Condição FROM produtos"
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Verifica se a consulta retornou dados
                if not data:
                    return []  # Retorna uma lista vazia se não houver dados

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
                
                # Verifica se a consulta retornou dados
                if not data:
                    return []  # Retorna uma lista vazia se não houver dados

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []
    
def GetProdutosVendas():
    """
    Obtém os dados das vendas, incluindo o valor unitário (Valor_un).
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT Produto, Quantidade_vendida, Vendedor, Data, Valor_total, `Valor Un`
                FROM vendas
                """
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Verifica se a consulta retornou dados
                if not data:
                    return []  # Retorna uma lista vazia se não houver dados

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela vendas: {e}")
        return []
    
    
def GetAllEventos():
    """
    Obtém os dados das vendas, incluindo o valor unitário (Valor_un).
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT id_evento, nome, data_inicio, data_fim, descricao
                FROM eventos
                """
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Verifica se a consulta retornou dados
                if not data:
                    return []  # Retorna uma lista vazia se não houver dados

                return data

    except Exception as e:
        print(f"Erro ao obter dados da tabela vendas: {e}")
        return []
    
def GetContagemProduto(id_evento):
    """
    Retorna o número de produtos associados a um evento específico.

    :param id_evento: ID do evento.
    :return: Número de produtos associados ao evento.
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT COUNT(*) 
                    FROM produtos_eventos 
                    WHERE id_evento = %s
                """
                cursor.execute(query, (id_evento,))
                contagem = cursor.fetchone()[0]  # Extrai o valor da contagem
                return contagem
    except Exception as e:
        print(f"Erro ao contar produtos do evento {id_evento}: {e}")
        return 0  # Retorna 0 em caso de erro
    
def inserir_mudanca_card_init():
    """
    Insere um registro na tabela de mudanças com o tipo 'CARD_INIT' e a data/hora atual.

    Args:
        conn: Conexão ativa com o banco de dados.
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:

                tabela = 'card tela'
                tipo_mudanca = 'CARD'
                data_modificacao = datetime.now()  # Data/hora atual

                # Query SQL para inserir o registro
                query = """
                    INSERT INTO log_mudancas (tabela, tipo_mudanca, data_modificacao)
                    VALUES (%s, %s,%s)
                """

                # Executa a query com os valores
                cursor.execute(query, (tabela, tipo_mudanca, data_modificacao))

                # Confirma a transação
                conn.commit()

                print("Registro inserido com sucesso!")
                
                return

    except Exception as e:
        # Em caso de erro, faz rollback e exibe a mensagem de erro
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
        return 0  # Retorna 0 em caso de 
    
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
        return 0  # Retorna 0 em caso de 
    
def VerificarSeProdutoEhEvento(id_produto):
    """
    Verifica se o produto é de um evento.

    :param id_produto: ID do produto.
    :return: True se o produto for de um evento, False caso contrário.
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id_produto_evento FROM produtos_eventos WHERE id_produto_evento = %s"
                cursor.execute(query, (id_produto,))
                data = cursor.fetchone()

                if data:
                    return True  # O produto é de um evento
                else:
                    return False  # O produto não é de um evento

    except Exception as e:
        print(f"Erro ao verificar se o produto é de um evento: {e}")
        return False    
    
    

def UpdateStatus(id_produto, status):
    """
    Atualiza o status de um produto no banco de dados.

    :param id_produto: ID do produto.
    :param status: Novo status do produto (ex: 'Ativo', 'Pausado', 'Esgotado').
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Verifica se o produto é de um evento
                query_verificar_evento = "SELECT id_produto_evento FROM produtos_eventos WHERE id_produto_evento = %s"
                cursor.execute(query_verificar_evento, (id_produto,))
                is_evento = cursor.fetchone() is not None

                # Atualiza o status na tabela correta
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
    """
    Atualiza a quantidade e a quantidade disponível de um produto no banco de dados.
    """
    try:
        print("updatestock", id, quantidade)

        # Obtendo uma conexão do pool de conexões
        with pool.connection() as conn:
            # Criando um cursor para executar a query
            with conn.cursor() as cursor:
                # Definindo a query de atualização
                query = """
                UPDATE pbstock.produtos
                SET Quantidade = %s, 
                Quantidade_Disponível = Quantidade_Disponível + %s
                WHERE Id_produto = %s
                """
                # Executando a query com os parâmetros fornecidos
                cursor.execute(query, (quantidade, quantidade, id))

                # Confirmando as mudanças no banco
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

        # Obtendo uma conexão do pool de conexões
        with pool.connection() as conn:
            # Criando um cursor para executar a query
            with conn.cursor() as cursor:
                # Definindo a query de atualização
                query = """
                UPDATE pbstock.produtos_eventos
                SET Quantidade = %s, 
                Quantidade_Disponível = Quantidade_Disponível + %s
                WHERE id_produto_evento = %s
                """
                # Executando a query com os parâmetros fornecidos
                cursor.execute(query, (quantidade, quantidade, id))

                # Confirmando as mudanças no banco
                conn.commit()

        print("Status atualizado para o produto ID", id)
        return True

    except Exception as e:
        print(f"Erro ao atualizar o estoque: {e}")
        return False
    

def DecrementarEstoque(Quantidade_vendida, cod, filtro):
    """
    Decrementa a quantidade do estoque após a venda, baseado no Cód do produto ou produto de evento.
    Garante que o estoque não fique negativo e define o status como 'Esgotado' se chegar a zero.
    """
    start_time = datetime.now()

    try:
        # Converte a quantidade vendida para inteiro
        Quantidade_vendida = int(Quantidade_vendida)

        # Determina a tabela com base no filtro
        if filtro == 'produto':
            tabela = 'produtos'
        elif filtro == 'produto evento':
            tabela = 'produtos_eventos'
        else:
            raise HTTPException(status_code=400, detail="Filtro inválido. Use 'produto' ou 'produto evento'.")

        # Primeiro, busca a quantidade atual do produto
        query_busca = f"SELECT Quantidade_Disponível FROM pbstock.{tabela} WHERE Cód = %s"

        with pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query_busca, (cod,))
            resultado = cursor.fetchone()

            if not resultado:
                raise HTTPException(status_code=404, detail="Produto não encontrado.")

            quantidade_atual = resultado[0]

            # Verifica se a venda não deixará o estoque negativo
            if Quantidade_vendida > quantidade_atual:
                return "Quantidade insuficiente em estoque."

            # Calcula a nova quantidade
            nova_quantidade = max(quantidade_atual - Quantidade_vendida, 0)
            novo_status = 'Esgotado' if nova_quantidade == 0 else 'Ativo'

            # Atualiza o estoque e o status
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
                # Consulta para buscar produtos da tabela produtos
                query_produtos = """
                    SELECT Produto, Cód FROM produtos
                """
                cursor.execute(query_produtos)
                data_produtos = cursor.fetchall()

                # Consulta para buscar produtos da tabela produtos_eventos
                query_produtos_eventos = """
                    SELECT Produto, Cód FROM produtos_eventos
                """
                cursor.execute(query_produtos_eventos)
                data_produtos_eventos = cursor.fetchall()

                # Combinar os resultados das duas consultas
                combined_data = data_produtos + data_produtos_eventos

                # Formatar os dados no formato "Produto - Cód"
                lista_produtos_cod = [f"{produto} - {cod}" for produto, cod in combined_data]

                return lista_produtos_cod

    except Exception as e:
        print(f"Erro ao obter dados das tabelas Produto e Produtos_Eventos: {e}")
        return []
    
    
def getVendas():
    """
    Obtém a lista de produtos da tabela vendas.
    Retorna uma lista de strings com os nomes dos produtos, sem duplicatas.
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT Produto FROM vendas"
                cursor.execute(query)
                data = cursor.fetchall()
                # Extrai os nomes dos produtos das tuplas e remove duplicatas
                produtos_unicos = list(set([item[0] for item in data]))  # Usa set para remover duplicatas
                return produtos_unicos
    except Exception as e:
        print(f"Erro ao obter dados da tabela Produto: {e}")
        return []  # Retorna uma lista vazia em caso de erro


def GetProdutoNomesCodAtivo():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Consulta para buscar produtos ativos da tabela produtos
                query_produtos = """
                    SELECT Produto, Cód FROM produtos WHERE Condição = 'Ativo'
                """
                cursor.execute(query_produtos)
                data_produtos = cursor.fetchall()

                # Consulta para buscar produtos ativos da tabela produtos_eventos
                query_produtos_eventos = """
                    SELECT Produto, Cód FROM produtos_eventos WHERE Condição = 'Ativo'
                """
                cursor.execute(query_produtos_eventos)
                data_produtos_eventos = cursor.fetchall()

                # Combinar os resultados das duas consultas
                combined_data = data_produtos + data_produtos_eventos

                # Formatar os dados no formato "Produto - Cód"
                lista_produtos_cod = [f"{produto} - {cod}" for produto, cod in combined_data]

                return lista_produtos_cod

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
                # Obtém o ano e mês atuais
                data_atual = datetime.now()
                ano_mes = data_atual.strftime('%Y%m')  # Formato AAAAMM

                # Consulta o último ID gerado no mesmo ano e mês
                query = "SELECT id_evento FROM eventos WHERE id_evento LIKE %s ORDER BY id_evento DESC LIMIT 1"
                cursor.execute(query, (f"EVT{ano_mes}%",))
                ultimo_id = cursor.fetchone()

                if ultimo_id:
                    # Extrai o número sequencial do último ID e incrementa
                    ultimo_sequencial = int(ultimo_id[0][-4:])  # Pega os últimos 4 dígitos
                    novo_sequencial = ultimo_sequencial + 1
                else:
                    # Se não houver IDs no mesmo ano/mês, começa com 0001
                    novo_sequencial = 1

                # Formata o número sequencial com 4 dígitos
                codigo = f"{novo_sequencial:04d}"

                # Retorna o ID completo
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
    """
    Adiciona uma lista de produtos ao evento no banco de dados.

    :param id_evento: ID do evento ao qual os produtos serão vinculados.
    :param produtos: Lista de tuplas contendo os dados dos produtos.
                    Cada tupla deve ter o formato (nome, quantidade, valor, descricao, codigo).
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                for produto in produtos:
                    # Extrai os dados do produto
                    nome_produto = produto[0]  # Nome do produto
                    quantidade = produto[1]    # Quantidade
                    valor = produto[2]         # Valor unitário
                    descricao_produto = produto[3]  # Descrição
                    codigo_produto = produto[4]  # Código do produto

                    # Obtém a data e hora atuais
                    data_atual = datetime.now()

                    # Insere o produto no banco de dados
                    query = """
                        INSERT INTO produtos_eventos (
                            Produto, Cód, Quantidade, ValorPromocional, 
                            Descrição, Data, Quantidade_Disponível, id_evento
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        nome_produto,  # Nome do produto
                        codigo_produto,  # Código do produto (já gerado)    
                        quantidade,       # Quantidade
                        valor,            # Valor promocional
                        descricao_produto,  # Descrição
                        data_atual,       # Data e hora atuais
                        quantidade,       # Quantidade disponível (assumindo que é igual à quantidade)
                        id_evento,        # ID do evento
                    ))
                conn.commit()
    except Exception as e:
        print(f"Erro ao cadastrar produtos: {e}")
        raise  # Re-lança a exceção para ser tratada no chamador

    
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
        
        print('Código que chegou', cod)
        
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Verifica se o código contém "EVT"
                if "EVT" in cod:
                    # Consulta na tabela produtos_eventos
                    query = "SELECT ValorPromocional FROM produtos_eventos WHERE Cód = %s"
                else:
                    # Consulta na tabela produtos
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


def GetCardsInfo(intervalo):
    """
    Retorna os 3 produtos mais vendidos com base no intervalo de data especificado.

    Parâmetros:
        intervalo (str): Define o intervalo de data. Pode ser 'dia', 'semana', 'mes' ou 'total'.
                         Padrão: 'total'.

    Retorno:
        Lista de tuplas contendo (produto, quantidade_total) em ordem decrescente de quantidade.
    """
    start_time = datetime.now()  # Marca o início da execução da função

    try:
        # Inicia a conexão e mede o tempo
        with pool.connection() as conn:
            cursor = conn.cursor()

            # Calcula o tempo de conexão
            connection_time = datetime.now() - start_time

            # Define a coluna a ser usada com base no intervalo
            if intervalo == 'dia':
                coluna = 'venda_dia'
            elif intervalo == 'semana':
                coluna = 'venda_semana'
            elif intervalo == 'mes':
                coluna = 'venda_mes'
            else:  # 'total' ou qualquer outro valor
                coluna = 'venda_total'

            # Prepara e executa a consulta
            query_start_time = datetime.now()
            cursor.execute(f"""
                SELECT produto, {coluna}
                FROM vendas_produtos
                ORDER BY {coluna} DESC
                LIMIT 3
            """)
            query_execution_time = datetime.now() - query_start_time  # Tempo de execução da query

            # Obtém os dados da consulta
            dados = cursor.fetchall()

            # Formata o resultado como uma lista de tuplas (produto, quantidade)
            resultado_formatado = [(produto, quantidade) for produto, quantidade in dados]

            # Calcula o tempo total de execução
            total_execution_time = datetime.now() - start_time
            print(f"Tempo de Conexão: {connection_time.total_seconds():.4f} segundos")
            print(f"Tempo de Execução da Query: {query_execution_time.total_seconds():.4f} segundos")
            print(f"Tempo Total de Execução: {total_execution_time.total_seconds():.4f} segundos")

            return resultado_formatado

    except Exception as e:
        print(f"Erro ao processar os dados getcard: {e}")
        return None
    

def GetRecentSales():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Consulta SQL para buscar as vendas recentes
                query = """
                    SELECT Produto, Quantidade_vendida, Vendedor
                    FROM vendas
                    ORDER BY Data DESC
                    LIMIT 3
                """
                cursor.execute(query)
                results = cursor.fetchall()  # Busca todas as linhas retornadas

                if results:
                    return results  # Retorna as vendas com as três colunas
                else:
                    print("Nenhuma venda recente encontrada.")
                    return []  # Retorna uma lista vazia se não houver vendas

    except Exception as e:
        print(f"Erro ao obter dados das vendas recentes: {e}")
        return []  # Retorna uma lista vazia em caso de erro
    
def UpdateTimes():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Obtém a data atual (apenas a parte da data, sem hora)
                agora = datetime.now().date()

                # Obtém as próximas datas de atualização
                query = """
                SELECT proxima_mudanca_dia, proxima_mudanca_semana, proxima_mudanca_mes
                FROM atualizacao
                LIMIT 1
                """
                cursor.execute(query)
                result = cursor.fetchone()

                # Se o resultado for None ou algum valor vazio, retorna sem fazer nada
                if not result or not all(result):
                    print("Nenhuma data de atualização definida, nada a fazer.")
                    return False

                proxima_dia, proxima_semana, proxima_mes = result

                # Verifica se as variáveis são do tipo datetime.date e já estão no formato correto
                if isinstance(proxima_dia, datetime):
                    proxima_dia = proxima_dia.date()
                if isinstance(proxima_semana, datetime):
                    proxima_semana = proxima_semana.date()
                if isinstance(proxima_mes, datetime):
                    proxima_mes = proxima_mes.date()

                # Verifica se agora é maior ou igual a pelo menos uma das datas de atualização
                if not (agora >= proxima_dia or agora >= proxima_semana or agora >= proxima_mes):
                    print("Nenhuma data de atualização atingida. Saindo da função sem alterações.")
                    return False

                # Verifica se é hora de zerar as vendas do dia
                if agora >= proxima_dia:
                    cursor.execute("UPDATE vendas_produtos SET venda_dia = 0")
                    nova_proxima_dia = agora + timedelta(days=1)
                    cursor.execute("""
                        UPDATE atualizacao
                        SET proxima_mudanca_dia = %s
                    """, (nova_proxima_dia.strftime("%Y-%m-%d"),))
                    print("Vendas do dia zeradas!")

                # Verifica se é hora de zerar as vendas da semana
                if agora >= proxima_semana:
                    cursor.execute("UPDATE vendas_produtos SET venda_semana = 0")
                    # Calcula o início da próxima semana
                    dias_ate_proxima_semana = 7 - agora.weekday()
                    nova_proxima_semana = agora + timedelta(days=dias_ate_proxima_semana)
                    cursor.execute("""
                        UPDATE atualizacao
                        SET proxima_mudanca_semana = %s
                    """, (nova_proxima_semana.strftime("%Y-%m-%d"),))
                    print("Vendas da semana zeradas!")

                # Verifica se é hora de zerar as vendas do mês
                if agora >= proxima_mes:
                    cursor.execute("UPDATE vendas_produtos SET venda_mes = 0")
                    # Calcula o primeiro dia do próximo mês
                    primeiro_dia_proximo_mes = (agora.replace(day=1) + timedelta(days=32)).replace(day=1)
                    cursor.execute("""
                        UPDATE atualizacao
                        SET proxima_mudanca_mes = %s
                    """, (primeiro_dia_proximo_mes.strftime("%Y-%m-%d"),))
                    print("Vendas do mês zeradas!")

                # Confirma as alterações (só vai fazer o commit se for necessário)
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
                # Query para buscar os eventos ativos
                query = "SELECT nome, data_inicio FROM eventos"
                cursor.execute(query)
                data = cursor.fetchall()

                # Se não houver dados, retorna uma lista vazia
                if not data:
                    return []
                
                # Retorna os dados diretamente, sem formatação
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
                # Query para buscar os eventos ativos
                query = "SELECT nome FROM eventos"
                cursor.execute(query)
                data = cursor.fetchall()

                # Se não houver dados, retorna uma lista vazia
                return [evento[0] for evento in data] if data else []

    except Exception as e:
        print(f"Erro ao obter dados da tabela Eventos: {e}")
        return []



def GetItensForaEstoque():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                # Query para buscar os produtos esgotados nas duas tabelas
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

                # Se não houver dados, retorna uma lista vazia
                if not data:
                    return []

                # Retorna os produtos e suas respectivas datas
                return data

    except Exception as e:
        print(f"Erro ao obter dados dos produtos esgotados: {e}")
        return []

    
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