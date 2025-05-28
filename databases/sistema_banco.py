import hashlib
import random
import string
from utilitarios.Aprincipal_database import BancoDados

class SistemaBanco(BancoDados):
    SQL_SCHEMA_CREATION = [
        """
        CREATE TABLE Clientes
        (
            id_cliente   INT AUTO_INCREMENT PRIMARY KEY,
            nome         VARCHAR(255) NOT NULL,
            cpf          VARCHAR(14)  NOT NULL UNIQUE,
            senha_hash   VARCHAR(255) NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE Contas
        (
            id_conta      INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente    INT         NOT NULL,
            numero_conta  VARCHAR(20) NOT NULL UNIQUE,
            agencia       VARCHAR(10) NOT NULL,
            saldo         DECIMAL(15, 2) DEFAULT 0.00,
            tipo_conta    VARCHAR(50)    DEFAULT 'CORRENTE',
            data_abertura TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente) ON DELETE CASCADE
        ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE Transacoes
        (
            id_transacao     INT AUTO_INCREMENT PRIMARY KEY,
            id_conta_origem  INT,
            id_conta_destino INT,
            tipo_transacao   VARCHAR(50)    NOT NULL,
            valor            DECIMAL(15, 2) NOT NULL,
            data_transacao   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            descricao        VARCHAR(255),
            FOREIGN KEY (id_conta_origem) REFERENCES Contas (id_conta) ON DELETE SET NULL,
            FOREIGN KEY (id_conta_destino) REFERENCES Contas (id_conta) ON DELETE SET NULL
        ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE Chaves_Pix
        (
            id_chave_pix INT AUTO_INCREMENT PRIMARY KEY,
            id_conta     INT          NOT NULL,
            tipo_chave   VARCHAR(50)  NOT NULL,
            valor_chave  VARCHAR(255) NOT NULL UNIQUE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_conta) REFERENCES Contas (id_conta) ON DELETE CASCADE
        ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
    ]

    @classmethod
    def criar_tabelas_no_bd(cls):
        for statement in cls.SQL_SCHEMA_CREATION:
            cls.executar_sql(statement)

    @staticmethod
    def _hash_senha(senha):
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    @classmethod
    def registrar_cliente(cls, nome, cpf, senha):
        if cls.consultar_dados("Clientes", f"WHERE cpf = '{cpf}'"):
            print(f"CPF '{cpf}' já cadastrado.")
            return None
        senha_hashed = cls._hash_senha(senha)
        dados = {"nome": nome, "cpf": cpf, "senha_hash": senha_hashed}
        cls.inserir_dados("Clientes", dados)
        cliente_criado = cls.consultar_dados("Clientes", f"WHERE cpf = '{cpf}'")
        return cliente_criado[0][0] if cliente_criado else None

    @classmethod
    def login_cliente(cls, cpf, senha):
        cliente_data = cls.consultar_dados("Clientes", f"WHERE cpf = '{cpf}'")
        if cliente_data:
            if cliente_data[0][2] == cls._hash_senha(senha):
                return cliente_data[0][0]
            print("Senha incorreta.")
            return None
        print(f"CPF '{cpf}' não encontrado.")
        return None

    @classmethod
    def criar_conta_bancaria(cls, id_cliente, tipo_conta="CORRENTE", saldo_inicial=0.00):
        numero_conta = ''.join(random.choices(string.digits, k=8))
        agencia = "0001"
        while cls.consultar_dados("Contas", f"WHERE numero_conta = '{numero_conta}' AND agencia = '{agencia}'"):
            numero_conta = ''.join(random.choices(string.digits, k=8))
        dados = {
            "id_cliente": id_cliente,
            "numero_conta": numero_conta,
            "agencia": agencia,
            "tipo_conta": tipo_conta.upper(),
            "saldo": saldo_inicial
        }
        cls.inserir_dados("Contas", dados)
        conta_criada = cls.consultar_dados("Contas", f"WHERE numero_conta = '{numero_conta}' AND agencia = '{agencia}'")
        return conta_criada[0][0] if conta_criada else None

    @classmethod
    def consultar_saldo(cls, id_conta):
        resultado = cls.consultar_dados("Contas", f"WHERE id_conta = {id_conta}")
        return resultado[0][4] if resultado else None

    @classmethod
    def realizar_deposito(cls, id_conta_destino, valor, descricao="Depósito em conta"):
        if valor <= 0:
            print("Valor do depósito inválido.")
            return False
        saldo_atual = cls.consultar_saldo(id_conta_destino)
        if saldo_atual is None:
            print("Conta não encontrada.")
            return False
        cls.atualizar_dados("Contas", {"saldo": saldo_atual + valor}, f"id_conta = {id_conta_destino}")
        cls._registrar_transacao(id_conta_destino, None, "DEPOSITO", valor, descricao)
        return True

    @classmethod
    def realizar_saque(cls, id_conta_origem, valor, descricao="Saque em conta"):
        if valor <= 0:
            print("Valor do saque inválido.")
            return False
        saldo_atual = cls.consultar_saldo(id_conta_origem)
        if saldo_atual is None or saldo_atual < valor:
            print("Saldo insuficiente ou conta não encontrada.")
            return False
        cls.atualizar_dados("Contas", {"saldo": saldo_atual - valor}, f"id_conta = {id_conta_origem}")
        cls._registrar_transacao(id_conta_origem, None, "SAQUE", valor, descricao)
        return True

    @classmethod
    def _registrar_transacao(cls, id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao=""):
        dados = {
            "id_conta_origem": id_conta_origem,
            "id_conta_destino": id_conta_destino,
            "tipo_transacao": tipo_transacao,
            "valor": valor,
            "descricao": descricao
        }
        cls.inserir_dados("Transacoes", dados)

    @classmethod
    def cadastrar_chave_pix(cls, id_conta, tipo_chave, valor_chave):
        tipo_chave = tipo_chave.upper()
        if tipo_chave not in ["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]:
            print("Tipo de chave PIX inválido.")
            return None
        if cls.consultar_dados("Chaves_Pix", f"WHERE valor_chave = '{valor_chave}'"):
            print(f"Chave Pix '{valor_chave}' já cadastrada.")
            return None
        dados = {"id_conta": id_conta, "tipo_chave": tipo_chave, "valor_chave": valor_chave}
        cls.inserir_dados("Chaves_Pix", dados)
        chave = cls.consultar_dados("Chaves_Pix", f"WHERE valor_chave = '{valor_chave}'")
        return chave[0][0] if chave else None

    @classmethod
    def consultar_conta_por_chave_pix(cls, valor_chave):
        query = """
            SELECT c.id_conta, c.numero_conta, c.agencia, cl.nome as nome_cliente, cl.cpf as cpf_cliente
            FROM Chaves_Pix cp
            JOIN Contas c ON cp.id_conta = c.id_conta
            JOIN Clientes cl ON c.id_cliente = cl.id_cliente
            WHERE cp.valor_chave = %s
        """
        return cls.consultar_dados("Chaves_Pix", f"WHERE valor_chave = '{valor_chave}'")

    @classmethod
    def realizar_pix(cls, id_conta_origem, chave_pix_destino, valor):
        if valor <= 0:
            print("Valor do PIX inválido.")
            return False
        conta_destino = cls.consultar_conta_por_chave_pix(chave_pix_destino)
        if not conta_destino:
            print("Chave PIX destino não encontrada.")
            return False
        id_conta_destino = conta_destino['id_conta']
        saldo_origem = cls.consultar_saldo(id_conta_origem)
        if saldo_origem is None or saldo_origem < valor:
            print("Saldo insuficiente ou conta origem não encontrada.")
            return False
        cls.atualizar_dados("Contas", {"saldo": saldo_origem - valor}, f"id_conta = {id_conta_origem}")
        saldo_destino = cls.consultar_saldo(id_conta_destino)
        cls.atualizar_dados("Contas", {"saldo": saldo_destino + valor}, f"id_conta = {id_conta_destino}")
        cls._registrar_transacao(id_conta_origem, id_conta_destino, "PIX", valor, f"PIX enviado para {chave_pix_destino}")
        return True

    @classmethod
    def extrato(cls, id_conta):
        query = """
            SELECT t.data_transacao, t.tipo_transacao, t.valor, t.descricao
            FROM Transacoes t
            WHERE t.id_conta_origem = %s OR t.id_conta_destino = %s
            ORDER BY t.data_transacao DESC
        """
        return cls.consultar_dados("Transacoes", f"WHERE id_conta_origem = {id_conta} OR id_conta_destino = {id_conta}")