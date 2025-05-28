from utilitarios.Aprincipal_database import BancoDados


class Simulador_Banco_BD:
    """
    Classe responsável pela estrutura do banco de dados do simulador bancário.
    """

    # Estrutura da tabela de clientes
    colunas_cliente = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "nome": "VARCHAR(100) NOT NULL",
        "cpf": "VARCHAR(14) NOT NULL UNIQUE",
        "data_nascimento": "DATE NOT NULL",
        "endereco": "VARCHAR(200) NOT NULL"
    }

    # Estrutura da tabela de contas bancárias
    colunas_conta = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "numero": "VARCHAR(20) NOT NULL UNIQUE",
        "saldo": "FLOAT DEFAULT 0",
        "tipo": "VARCHAR(20) NOT NULL",  # ex: "Corrente", "Poupança"
        "id_cliente": "INT",
        "FOREIGN KEY (id_cliente)": "REFERENCES clientes(id) ON DELETE CASCADE"
    }

    @classmethod
    def criar_tabelas(cls):
        BancoDados.criar_tabela("clientes", cls.colunas_cliente)
        BancoDados.criar_tabela("contas", cls.colunas_conta)


class Cliente:
    """
    Classe para manipular dados de clientes.
    """

    @classmethod
    def cadastrar_cliente(cls, nome, cpf, data_nascimento, endereco):
        dados = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": endereco
        }
        BancoDados.inserir_dados("clientes", dados)

    @classmethod
    def listar_clientes(cls):
        return BancoDados.consultar_dados("clientes")

    @classmethod
    def buscar_por_cpf(cls, cpf):
        return BancoDados.consultar_dados("clientes", f"WHERE cpf = '{cpf}'")

    @classmethod
    def deletar_cliente(cls, cpf):
        BancoDados.deletar_dados("clientes", f"cpf = '{cpf}'")


class Conta:
    """
    Classe para manipular dados das contas bancárias.
    """

    @classmethod
    def criar_conta(cls, numero, tipo, id_cliente, saldo=0):
        dados = {
            "numero": numero,
            "tipo": tipo,
            "id_cliente": id_cliente,
            "saldo": saldo
        }
        BancoDados.inserir_dados("contas", dados)

    @classmethod
    def listar_contas(cls):
        # JOIN entre contas e clientes
        query = """
        SELECT contas.id, contas.numero, contas.saldo, contas.tipo,
               clientes.nome, clientes.cpf
        FROM contas
        JOIN clientes ON contas.id_cliente = clientes.id
        """
        return BancoDados.executar_select_customizado(query)

    @classmethod
    def buscar_por_numero(cls, numero):
        return BancoDados.consultar_dados("contas", f"WHERE numero = '{numero}'")

    @classmethod
    def alterar_saldo(cls, numero, novo_saldo):
        BancoDados.atualizar_dados("contas", {"saldo": novo_saldo}, f"numero = '{numero}'")

    @classmethod
    def deletar_conta(cls, numero):
        BancoDados.deletar_dados("contas", f"numero = '{numero}'")


# Para criar as tabelas ao rodar diretamente:
if __name__ == "__main__":
    Simulador_Banco_BD.criar_tabelas()
