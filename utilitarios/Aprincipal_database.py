import re
import mysql.connector as mysql

class BancoDados:
    """
    Classe utilitária para operações com banco de dados MySQL.
    Inclui métodos para criar banco, criar tabela, inserir, consultar, atualizar e deletar dados.
    """

    # Configurações de conexão (ajuste conforme necessário)
    CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'jogos'  # usado apenas quando o banco já existe
    }

    @classmethod
    def criar_database(cls):
        """
        Tenta criar um banco de dados chamado 'jogos'.
        Se já existir, exibe mensagem de erro.
        """
        try:
            conexao = mysql.connect(
                host=cls.CONFIG['host'],
                user=cls.CONFIG['user'],
                password=cls.CONFIG['password']
            )
            cursor = conexao.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS jogos")
            conexao.commit()
            print("✅ Banco de dados 'jogos' criado ou já existente.")
        except mysql.Error as erro:
            print(f"❌ Erro ao criar o banco de dados: {erro}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
                print("🔌 Conexão encerrada.")

    @classmethod
    def conectar(cls):
        """
        Conecta ao banco de dados 'jogos' e retorna a conexão.
        """
        try:
            conexao = mysql.connect(**cls.CONFIG)
            return conexao
        except mysql.Error as erro:
            print(f"❌ Erro ao conectar ao banco de dados: {erro}")
            return None

    @staticmethod
    def fechar_conexao_curso(conexao, cursor):
        """
        Fecha a conexão e o cursor do banco de dados.
        """
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
            print("🔌 Conexão encerrada.")

    @classmethod
    def criar_tabela(cls, nome_tabela, colunas: dict):
        """
        Cria uma tabela no banco de dados 'jogos'.
        :param nome_tabela: Nome da tabela a ser criada.
        :param colunas: Dicionário com os nomes e tipos das colunas.
        """
        conexao = cls.conectar()
        if not conexao:
            return

        cursor = conexao.cursor()
        colunas_str = ", ".join([f"{col} {tipo}" for col, tipo in colunas.items()])
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({colunas_str})")
            conexao.commit()
            print(f"✅ Tabela '{nome_tabela}' criada ou já existente.")
        except mysql.Error as erro:
            print(f"❌ Erro ao criar a tabela '{nome_tabela}': {erro}")
        finally:
            cls.fechar_conexao_curso(conexao, cursor)

    @classmethod
    def inserir_dados(cls, nome_tabela, dados: dict):
        """
        Insere dados em uma tabela.
        :param nome_tabela: Nome da tabela.
        :param dados: Dicionário com os dados a serem inseridos.
        """
        conexao = cls.conectar()
        if not conexao:
            return

        cursor = conexao.cursor()
        colunas = ", ".join(dados.keys())
        valores = ", ".join(["%s"] * len(dados))
        try:
            cursor.execute(
                f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({valores})",
                tuple(dados.values())
            )
            conexao.commit()
            print("✅ Dados inseridos com sucesso.")
        except mysql.Error as erro:
            print(f"❌ Erro ao inserir dados: {erro}")
        finally:
            cls.fechar_conexao_curso(conexao, cursor)

    @classmethod
    def consultar_dados(cls, nome_tabela, condicao=None):
        """
        Consulta dados de uma tabela.
        :param nome_tabela: Nome da tabela.
        :param condicao: Condição para o filtro (opcional).
        :return: Lista de resultados ou None.
        """
        conexao = cls.conectar()
        if not conexao:
            return

        cursor = conexao.cursor()
        try:
            consulta = f"SELECT * FROM {nome_tabela}"
            if condicao:
                consulta += f" WHERE {condicao}"
            cursor.execute(consulta)
            resultados = cursor.fetchall()

            if not resultados:
                print("ℹ️ Nenhum dado encontrado.")
            else:
                return resultados
        except mysql.Error as erro:
            print(f"❌ Erro ao consultar dados: {erro}")
        finally:
            cls.fechar_conexao_curso(conexao, cursor)

    @classmethod
    def atualizar_dados(cls, nome_tabela, dados: dict, condicao):
        """
        Atualiza registros existentes.
        :param nome_tabela: Nome da tabela.
        :param dados: Dicionário com dados para atualizar.
        :param condicao: Condição WHERE para selecionar os registros.
        """
        conexao = cls.conectar()
        if not conexao:
            return

        cursor = conexao.cursor()
        set_str = ", ".join([f"{col} = %s" for col in dados])
        try:
            cursor.execute(
                f"UPDATE {nome_tabela} SET {set_str} WHERE {condicao}",
                tuple(dados.values())
            )
            conexao.commit()
            print("✅ Dados atualizados com sucesso.")
        except mysql.Error as erro:
            print(f"❌ Erro ao atualizar dados: {erro}")
        finally:
            cls.fechar_conexao_curso(conexao, cursor)

    @classmethod
    def deletar_dados(cls, nome_tabela, condicao):
        """
        Deleta registros da tabela.
        :param nome_tabela: Nome da tabela.
        :param condicao: Condição WHERE para deletar.
        """
        conexao = cls.conectar()
        if not conexao:
            return

        cursor = conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM {nome_tabela} WHERE {condicao}")
            conexao.commit()
            print("✅ Dados deletados com sucesso.")
        except mysql.Error as erro:
            print(f"❌ Erro ao deletar dados: {erro}")
        finally:
            cls.fechar_conexao_curso(conexao, cursor)

# Exemplo de uso como script
if __name__ == "__main__":
    BancoDados.criar_database()
