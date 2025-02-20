import aiomysql
from fastapi import HTTPException


async def conectar_banco():
    try:
        # Configurações de conexão com o MySQL
        conn = await aiomysql.connect(
            host='localhost',  # Endereço do banco de dados
            port=3306,         # Porta do MySQL
            user='root',       # Usuário do MySQL
            password='',  # Senha do MySQL
            db='pbstock' # Nome do banco de dados
        )
        cursor = await conn.cursor()
        print("conectado ao banco mysql")
        return conn, cursor
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")

async def DataLoginUser(User, Password):
    conn, cursor = await conectar_banco()

    try:
        # Consulta para pegar todos os logins do banco
        await cursor.execute("SELECT * FROM usuarios")
        DataLoginUser = await cursor.fetchall()
        
        print(DataLoginUser)

        for login in DataLoginUser:
            if User == login[1] and Password == login[2]:
                
                # Verifica se o usuário é admin ou colaborador
                if login:
                    return {'status': 'sucess', 'message': 'Bem-vindo, administrador!','redirect': 'admin'}
                #elif login[2] == 'colaborador':
                #    return {'status': 'sucesso', 'message': 'Bem-vindo, colaborador!', 'css_usuario': css_usuario, 'css_senha': css_senha, 'redirect': 'colaborador'}
                
                break
            else:
                
                if(User != login[1] or Password != login[2]):

                    return {'status': 'error', 'message': 'Usuário ou senha incorretos'}
    
    except Exception as e:
        print("Erro ao executar a consulta:", e)
        return {'status': 'error', 'message': str(e)}

    finally:
        await cursor.close()
        conn.close()

async def DataloginSemBanco(User, Password):

    try:
        if (User == 'mateus' or User == 'carlos'):

            if(Password == '123'):
                
                return {'status': 'sucess', 'message': 'Bem-vindo, administrador!','redirect': 'admin', 'user': 'carlos'}
        else:

              return {'status': 'error', 'message': 'Usuário ou senha incorretos'}
    except Exception as e:
        print("Erro ao executar a consulta sem banco de dados:", e)