# banco_classes.py (Versão Refatorada com Classes e JOIN)

import mysql.connector
from mysql.connector import Error
import hashlib
import random
import string
from datetime import datetime # Para usar com datas de criação/transação
from utilitarios.Aprincipal_database import BancoDados

class SistemaBanco(BancoDados):
    @classmethod
    def criar_tabelas_banco(cls):
        """Cria todas as tabelas necessárias para o sistema bancário"""
        tabelas_sql = [
            """
            CREATE TABLE IF NOT EXISTS Clientes (
                id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cpf VARCHAR(14) NOT NULL UNIQUE,
                senha_hash VARCHAR(255) NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS Contas (
                id_conta INT AUTO_INCREMENT PRIMARY KEY,
                id_cliente INT NOT NULL,
                numero_conta VARCHAR(20) NOT NULL UNIQUE,
                agencia VARCHAR(10) NOT NULL,
                saldo DECIMAL(15, 2) DEFAULT 0.00,
                tipo_conta VARCHAR(50) DEFAULT 'CORRENTE',
                data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS Transacoes (
                id_transacao INT AUTO_INCREMENT PRIMARY KEY,
                id_conta_origem INT,
                id_conta_destino INT,
                tipo_transacao VARCHAR(50) NOT NULL,
                valor DECIMAL(15, 2) NOT NULL,
                data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                descricao VARCHAR(255),
                FOREIGN KEY (id_conta_origem) REFERENCES Contas(id_conta) ON DELETE SET NULL,
                FOREIGN KEY (id_conta_destino) REFERENCES Contas(id_conta) ON DELETE SET NULL
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS Chaves_Pix (
                id_chave_pix INT AUTO_INCREMENT PRIMARY KEY,
                id_conta INT NOT NULL,
                tipo_chave VARCHAR(50) NOT NULL,
                valor_chave VARCHAR(255) NOT NULL UNIQUE,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_conta) REFERENCES Contas(id_conta) ON DELETE CASCADE
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            """
        ]
        
        for sql in tabelas_sql:
            cls.executar_sql(sql)

# --- Configuração do Banco de Dados ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Changed from 'seu_usuario_mysql'
    'password': '',  # Changed from 'sua_senha_mysql'
    'database': 'jogos',
    'port': 3306
}

# --- Comandos SQL para Criação do Esquema (Permanece Global) ---
SQL_SCHEMA_CREATION = [
    """
    CREATE TABLE IF NOT EXISTS Clientes (
        id_cliente INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        cpf VARCHAR(14) NOT NULL UNIQUE,
        senha_hash VARCHAR(255) NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """,
    """
    CREATE TABLE IF NOT EXISTS Contas (
        id_conta INT AUTO_INCREMENT PRIMARY KEY,
        id_cliente INT NOT NULL,
        numero_conta VARCHAR(20) NOT NULL UNIQUE,
        agencia VARCHAR(10) NOT NULL,
        saldo DECIMAL(15, 2) DEFAULT 0.00,
        tipo_conta VARCHAR(50) DEFAULT 'CORRENTE',
        data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE
    ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """,
    """
    CREATE TABLE IF NOT EXISTS Transacoes (
        id_transacao INT AUTO_INCREMENT PRIMARY KEY,
        id_conta_origem INT,
        id_conta_destino INT,
        tipo_transacao VARCHAR(50) NOT NULL,
        valor DECIMAL(15, 2) NOT NULL,
        data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        descricao VARCHAR(255),
        FOREIGN KEY (id_conta_origem) REFERENCES Contas(id_conta) ON DELETE SET NULL,
        FOREIGN KEY (id_conta_destino) REFERENCES Contas(id_conta) ON DELETE SET NULL
    ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """,
    """
    CREATE TABLE IF NOT EXISTS Chaves_Pix (
        id_chave_pix INT AUTO_INCREMENT PRIMARY KEY,
        id_conta INT NOT NULL,
        tipo_chave VARCHAR(50) NOT NULL,
        valor_chave VARCHAR(255) NOT NULL UNIQUE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_conta) REFERENCES Contas(id_conta) ON DELETE CASCADE
    ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """
]

# --- Funções Utilitárias de Banco de Dados (Podem ser movidas para uma classe DBManager no futuro) ---
def conectar_bd():
    """Estabelece conexão com o BD, tentando criar o database se não existir."""
    global DB_CONFIG
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            temp_cfg = DB_CONFIG.copy()
            db_name = temp_cfg.pop('database')
            conn_server = None
            try:
                conn_server = mysql.connector.connect(**temp_cfg)
                cursor = conn_server.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                cursor.close()
                return mysql.connector.connect(**DB_CONFIG)
            except Error as server_e:
                print(f"!! Erro BD (conectar_bd - criar DB): {server_e}")
                return None
            finally:
                if conn_server and conn_server.is_connected():
                    conn_server.close()
        else:
            print(f"!! Erro BD (conectar_bd): {e}")
            return None
    return None

def executar_query(query, params=None, fetch_one=False, fetch_all=False, commit=False, get_last_id=False):
    """Executa uma query SQL genérica."""
    conn = None
    cursor = None
    last_id = None
    try:
        conn = conectar_bd()
        if not conn:
            return None
        
        # Para INSERT com get_last_id, não usamos dictionary=True inicialmente
        # ou o lastrowid pode não funcionar como esperado em todas as configs.
        # Mas para SELECTS, dictionary=True é útil.
        cursor = conn.cursor(dictionary=(not get_last_id and (fetch_one or fetch_all)))
        
        cursor.execute(query, params or ())
        
        if commit:
            conn.commit()
            if get_last_id:
                last_id = cursor.lastrowid
                # Se lastrowid for 0 ou None, tenta buscar o ID de outra forma (exemplo, não ideal para todos os casos)
                # Isso é mais relevante para tabelas com AUTO_INCREMENT explícito e quando a query é um INSERT.
                # Para robustez, o método de obter o último ID pode variar.
        
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        if get_last_id:
            return last_id
        return True # Sucesso para commit sem fetch, ou DDL.
    except Error as e:
        if conn and commit:
            try: conn.rollback()
            except Error: pass
        print(f"!! Erro Query: {query[:100]}... -> {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def criar_tabelas_db_inicial():
    """Cria/Recria as tabelas do banco de dados."""
    global SQL_SCHEMA_CREATION
    conn = None
    cursor = None
    try:
        conn = conectar_bd()
        if not conn:
            print("!! Falha ao conectar ao BD para criar tabelas.")
            return False
        cursor = conn.cursor()
        print("-> Iniciando criação/recriação das tabelas...")
        for stmt_group in SQL_SCHEMA_CREATION:
            for stmt in stmt_group.split(';'):
                stmt_s = stmt.strip()
                if stmt_s:
                    try:
                        cursor.execute(stmt_s)
                    except Error as e_inner:
                        if "Unknown table" in str(e_inner) and "DROP TABLE" in stmt_s.upper():
                            pass # OK, tabela não existia para ser dropada
                        else:
                            print(f"!! Erro SQL (criar_tabelas): {stmt_s[:70]}... Erro: {e_inner}")
                            raise # Relança para ser pego pelo except externo
        conn.commit()
        print("-> Tabelas criadas/recriadas com sucesso!")
        return True
    except Error as e_outer:
        print(f"!! Erro geral na criação de tabelas: {e_outer}")
        if conn:
            try: conn.rollback()
            except Error: pass
        return False
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

# --- Classes do Domínio ---

class Cliente:
    """Representa um cliente do banco."""
    def __init__(self, id_cliente, nome, cpf, data_criacao=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.data_criacao = data_criacao or datetime.now()
        self.contas = [] # Lista de objetos Conta associados

    def __str__(self):
        return f"Cliente(ID: {self.id_cliente}, Nome: {self.nome}, CPF: {self.cpf})"

    def adicionar_conta(self, conta_obj):
        """Adiciona um objeto Conta à lista de contas do cliente."""
        if isinstance(conta_obj, Conta):
            self.contas.append(conta_obj)
        else:
            print("!! Tentativa de adicionar objeto inválido como conta.")

class Conta:
    """Representa uma conta bancária."""
    def __init__(self, id_cliente, agencia="001", tipo_conta="pf", saldo=0.00, data_abertura=datetime.now()):
        self.id_cliente = id_cliente # ID do cliente dono da conta
        self.agencia = agencia
        self.tipo_conta = tipo_conta.upper()
        self.saldo = float(saldo) # Garante que saldo seja float
        self.data_abertura = data_abertura or datetime.now()

    def __str__(self):
        return f"Conta(ID: {self.id_conta}, N°: {self.agencia}-{self.numero_conta}, Tipo: {self.tipo_conta}, Saldo: R${self.saldo:.2f})"

    def _registrar_transacao_conta(self, cursor, id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao=""):
        """Registra uma transação. Usado internamente por métodos que já têm um cursor e transação abertos."""
        sql = "INSERT INTO Transacoes (id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao))
    
    def depositar(self, valor, descricao="Depósito"):
        """Realiza um depósito nesta conta."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("!! Valor de depósito inválido.")
            return False
        
        conn = None
        cursor = None
        try:
            conn = conectar_bd()
            if not conn: return False
            cursor = conn.cursor()
            cursor.execute("START TRANSACTION")
            
            sql_update = "UPDATE Contas SET saldo = saldo + %s WHERE id_conta = %s"
            cursor.execute(sql_update, (valor, self.id_conta))
            if cursor.rowcount == 0:
                print(f"!! Conta ID {self.id_conta} não encontrada para depósito.")
                cursor.execute("ROLLBACK")
                return False
            
            self._registrar_transacao_conta(cursor, None, self.id_conta, "DEPOSITO", valor, descricao)
            conn.commit()
            self.saldo += float(valor) # Atualiza o saldo no objeto
            print(f"-> Depósito de R${valor:.2f} na conta {self.numero_conta} realizado.")
            return True
        except Error as e:
            if conn: conn.rollback()
            print(f"!! Erro ao depositar na conta {self.numero_conta}: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def sacar(self, valor, descricao="Saque"):
        """Realiza um saque desta conta."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("!! Valor de saque inválido.")
            return False

        conn = None
        cursor = None
        try:
            conn = conectar_bd()
            if not conn: return False
            cursor = conn.cursor(dictionary=True) # Para ler o saldo
            cursor.execute("START TRANSACTION")

            # Re-consulta o saldo com FOR UPDATE para travar a linha
            sql_saldo = "SELECT saldo FROM Contas WHERE id_conta = %s FOR UPDATE"
            cursor.execute(sql_saldo, (self.id_conta,))
            conta_db = cursor.fetchone()

            if not conta_db:
                print(f"!! Conta ID {self.id_conta} não encontrada para saque.")
                cursor.execute("ROLLBACK")
                return False
            
            saldo_atual_db = float(conta_db['saldo'])
            if saldo_atual_db < valor:
                print(f"!! Saldo insuficiente (R${saldo_atual_db:.2f}) para sacar R${valor:.2f} da conta {self.numero_conta}.")
                cursor.execute("ROLLBACK")
                return False

            sql_update = "UPDATE Contas SET saldo = saldo - %s WHERE id_conta = %s"
            cursor.execute(sql_update, (valor, self.id_conta))
            
            self._registrar_transacao_conta(cursor, self.id_conta, None, "SAQUE", valor, descricao)
            conn.commit()
            self.saldo -= float(valor) # Atualiza o saldo no objeto
            print(f"-> Saque de R${valor:.2f} da conta {self.numero_conta} realizado.")
            return True
        except Error as e:
            if conn: conn.rollback()
            print(f"!! Erro ao sacar da conta {self.numero_conta}: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def consultar_saldo_db(self):
        """Consulta e atualiza o saldo do objeto Conta a partir do banco de dados."""
        saldo_db = executar_query("SELECT saldo FROM Contas WHERE id_conta = %s", (self.id_conta,), fetch_one=True)
        if saldo_db is not None:
            self.saldo = float(saldo_db['saldo'])
            return self.saldo
        return None # Ou lançar uma exceção

    def obter_extrato_db(self):
        """Busca o extrato de transações desta conta no banco de dados."""
        query = """
            SELECT data_transacao, tipo_transacao, valor, descricao
            FROM Transacoes 
            WHERE id_conta_origem = %s OR id_conta_destino = %s
            ORDER BY data_transacao DESC, id_transacao DESC
        """
        transacoes = executar_query(query, (self.id_conta, self.id_conta), fetch_all=True)
        return transacoes or []

    def cadastrar_chave_pix_db(self, tipo_chave, valor_chave):
        """Cadastra uma chave PIX para esta conta."""
        tipo_chave = tipo_chave.upper()
        if tipo_chave not in ["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]:
            print("!! Tipo de chave PIX inválido.")
            return False
        
        # Verifica se a chave PIX já existe globalmente
        if executar_query("SELECT id_chave_pix FROM Chaves_Pix WHERE valor_chave = %s", (valor_chave,), fetch_one=True):
            print(f"!! Chave Pix '{valor_chave}' já cadastrada no sistema.")
            return False
            
        sql = "INSERT INTO Chaves_Pix (id_conta, tipo_chave, valor_chave) VALUES (%s, %s, %s)"
        if executar_query(sql, (self.id_conta, tipo_chave, valor_chave), commit=True):
            print(f"-> Chave PIX '{valor_chave}' ({tipo_chave}) cadastrada para conta {self.numero_conta}.")
            return True
        print(f"!! Falha ao cadastrar chave PIX para conta {self.numero_conta}.")
        return False

    def consultar_saldo(self, id_conta):
        """
        Consulta o saldo da conta pelo id_conta.
        Retorna o saldo como float ou None se não encontrar.
        """
        sql = "SELECT saldo FROM Contas WHERE id_conta = %s"
        resultado = executar_query(sql, (id_conta,), fetch_one=True)
        if resultado and 'saldo' in resultado:
            return float(resultado['saldo'])
        return None

class SistemaBancario:
    """Classe principal para gerenciar as operações do banco."""
    def __init__(self):
        self.clientes_carregados = {} # Cache simples de clientes carregados {id_cliente: ClienteObj}
        self.cliente_atual = None

    def _hash_senha(self, senha):
        """Helper para gerar hash de senha."""
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def _gerar_numero_conta_unico(self, agencia):
        """Gera um número de conta único para uma agência."""
        while True:
            num_conta = ''.join(random.choices(string.digits, k=8))
            if not executar_query("SELECT id_conta FROM Contas WHERE numero_conta = %s AND agencia = %s", (num_conta, agencia), fetch_one=True):
                return num_conta

    def registrar_cliente(self, nome, cpf, senha):
        """Registra um novo cliente."""
        if executar_query("SELECT id_cliente FROM Clientes WHERE cpf = %s", (cpf,), fetch_one=True):
            print(f"!! CPF '{cpf}' já cadastrado.")
            return None
        
        senha_hashed = self._hash_senha(senha)
        sql = "INSERT INTO Clientes (nome, cpf, senha_hash) VALUES (%s, %s, %s)"
        
        id_novo_cliente = executar_query(sql, (nome, cpf, senha_hashed), commit=True, get_last_id=True)

        if id_novo_cliente:
            print(f"-> Cliente '{nome}' registrado com ID: {id_novo_cliente}.")
            # Retorna um objeto Cliente
            return Cliente(id_cliente=id_novo_cliente, nome=nome, cpf=cpf)
        
        print(f"!! Falha ao registrar cliente '{nome}'.")
        return None

    def login_cliente(self, cpf, senha):
        """Autentica um cliente."""
        sql = "SELECT id_cliente, nome, cpf, senha_hash, data_criacao FROM Clientes WHERE cpf = %s"
        cliente_data = executar_query(sql, (cpf,), fetch_one=True)
        
        if cliente_data and cliente_data['senha_hash'] == self._hash_senha(senha):
            cliente_obj = Cliente(
                id_cliente=cliente_data['id_cliente'],
                nome=cliente_data['nome'],
                cpf=cliente_data['cpf'],
                data_criacao=cliente_data['data_criacao']
            )
            self.clientes_carregados[cliente_obj.id_cliente] = cliente_obj # Cache
            print(f"-> Login bem-sucedido para {cliente_obj.nome}.")
            self.cliente_atual = cliente_obj
            return cliente_obj
        
        print(f"!! Falha no login para CPF '{cpf}'. Senha incorreta ou CPF não encontrado.")
        return None

    def criar_conta_bancaria(self, cliente_obj, tipo_conta, saldo_inicial=0.00):
        """Cria uma conta para um objeto Cliente."""
        if not isinstance(cliente_obj, Cliente) or cliente_obj.id_cliente is None:
            print("!! Cliente inválido para criação de conta.")
            return None

        agencia = "0001" # Agência padrão
        numero_conta = self._gerar_numero_conta_unico(agencia)
        tipo_conta_upper = tipo_conta.upper()

        sql = "INSERT INTO Contas (id_cliente, numero_conta, agencia, tipo_conta, saldo) VALUES (%s, %s, %s, %s, %s)"
        params = (cliente_obj.id_cliente, numero_conta, agencia, tipo_conta_upper, float(saldo_inicial))
        
        id_nova_conta = executar_query(sql, params, commit=True, get_last_id=True)

        if id_nova_conta:
            conta_obj = Conta(
                id_conta=id_nova_conta,
                id_cliente=cliente_obj.id_cliente,
                numero_conta=numero_conta,
                agencia=agencia,
                tipo_conta=tipo_conta_upper,
                saldo=saldo_inicial
            )
            cliente_obj.adicionar_conta(conta_obj) # Associa ao objeto cliente
            print(f"-> Conta {conta_obj.tipo_conta} N°{conta_obj.numero_conta} criada para {cliente_obj.nome}.")
            return conta_obj
        
        print(f"!! Falha ao criar conta para {cliente_obj.nome}.")
        return None
        
    def carregar_contas_do_cliente(self, cliente_obj):
        """Carrega todas as contas de um cliente do BD e as adiciona ao objeto Cliente."""
        if not isinstance(cliente_obj, Cliente): return
        
        sql = "SELECT id_conta, numero_conta, agencia, tipo_conta, saldo, data_abertura FROM Contas WHERE id_cliente = %s"
        contas_data = executar_query(sql, (cliente_obj.id_cliente,), fetch_all=True)
        
        cliente_obj.contas = [] # Limpa contas existentes no objeto antes de recarregar
        if contas_data:
            for c_data in contas_data:
                conta_obj = Conta(**c_data) # Cria objeto Conta com dados do BD
                cliente_obj.adicionar_conta(conta_obj)
        # print(f"-> Contas de {cliente_obj.nome} carregadas: {len(cliente_obj.contas)} conta(s).")

    def obter_conta_por_id(self, id_conta, cliente_obj=None):
        """Busca uma conta pelo ID. Se cliente_obj for fornecido, busca nas contas já carregadas dele."""
        if cliente_obj and isinstance(cliente_obj, Cliente):
            for conta in cliente_obj.contas:
                if conta.id_conta == id_conta:
                    return conta
        
        # Se não encontrou no cache do cliente ou cliente não fornecido, busca no BD
        conta_data = executar_query("SELECT * FROM Contas WHERE id_conta = %s", (id_conta,), fetch_one=True)
        if conta_data:
            return Conta(**conta_data)
        return None

    def realizar_pix(self, conta_origem_obj, chave_pix_destino, valor):
        """Realiza uma transferência PIX."""
        if not isinstance(conta_origem_obj, Conta):
            print("!! Conta de origem inválida para PIX.")
            return False
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("!! Valor de PIX inválido.")
            return False

        conn = None
        cursor = None
        try:
            conn = conectar_bd()
            if not conn: return False
            cursor = conn.cursor(dictionary=True)
            cursor.execute("START TRANSACTION")

            # 1. Verifica saldo e bloqueia conta de origem
            sql_origem = "SELECT saldo FROM Contas WHERE id_conta = %s FOR UPDATE"
            cursor.execute(sql_origem, (conta_origem_obj.id_conta,))
            origem_db = cursor.fetchone()
            if not origem_db or float(origem_db['saldo']) < valor:
                print(f"!! Saldo insuficiente ou conta origem ({conta_origem_obj.numero_conta}) não encontrada para PIX.")
                cursor.execute("ROLLBACK")
                return False
            
            # 2. Encontra conta de destino pela chave PIX e bloqueia
            # Este JOIN é um exemplo de como buscar dados relacionados.
            sql_destino = """
                SELECT c.id_conta, c.id_cliente, cl.nome as nome_cliente_destino
                FROM Chaves_Pix cp
                JOIN Contas c ON cp.id_conta = c.id_conta
                JOIN Clientes cl ON c.id_cliente = cl.id_cliente
                WHERE cp.valor_chave = %s 
                FOR UPDATE OF c; 
            """ 
            # "FOR UPDATE OF c" é mais específico para travar apenas linhas da tabela Contas via 'c'
            # Se o MySQL não suportar "OF c", usar "FOR UPDATE" geral na query.
            cursor.execute(sql_destino, (chave_pix_destino,))
            destino_data = cursor.fetchone()
            
            if not destino_data:
                print(f"!! Chave PIX de destino '{chave_pix_destino}' não encontrada.")
                cursor.execute("ROLLBACK")
                return False
            
            id_conta_destino = destino_data['id_conta']
            nome_cliente_destino = destino_data['nome_cliente_destino']

            if conta_origem_obj.id_conta == id_conta_destino:
                print("!! PIX para a mesma conta não é permitido.")
                cursor.execute("ROLLBACK")
                return False

            # 3. Debitar da conta de origem
            cursor.execute("UPDATE Contas SET saldo = saldo - %s WHERE id_conta = %s", (valor, conta_origem_obj.id_conta))
            # 4. Creditar na conta de destino
            cursor.execute("UPDATE Contas SET saldo = saldo + %s WHERE id_conta = %s", (valor, id_conta_destino))

            # 5. Registrar transações
            nome_cliente_origem = "Desconhecido"
            cliente_origem_obj_info = executar_query("SELECT nome FROM Clientes WHERE id_cliente = %s", (conta_origem_obj.id_cliente,), fetch_one=True, commit=False) # commit=False pois estamos numa transação
            if cliente_origem_obj_info: nome_cliente_origem = cliente_origem_obj_info['nome']

            desc_origem = f"PIX Enviado para {nome_cliente_destino} (Chave: {chave_pix_destino})"
            conta_origem_obj._registrar_transacao_conta(cursor, conta_origem_obj.id_conta, id_conta_destino, "PIX_ENVIADO", valor, desc_origem)
            
            desc_destino = f"PIX Recebido de {nome_cliente_origem}"
            conta_origem_obj._registrar_transacao_conta(cursor, conta_origem_obj.id_conta, id_conta_destino, "PIX_RECEBIDO", valor, desc_destino) # O registro da transação para o destino é feito no contexto do cursor

            conn.commit()
            conta_origem_obj.saldo -= float(valor) # Atualiza saldo do objeto origem
            print(f"-> PIX de R${valor:.2f} da conta {conta_origem_obj.numero_conta} para {nome_cliente_destino} realizado.")
            return True
        except Error as e:
            if conn: conn.rollback()
            print(f"!! Erro ao realizar PIX: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
            
    def pagar_jogo(self, conta_obj, valor_aposta, nome_jogo="Jogo Padrão"):
        """Debita valor de aposta da conta."""
        if not isinstance(conta_obj, Conta): return False
        print(f"-> Tentando pagar R${valor_aposta:.2f} para '{nome_jogo}' da conta {conta_obj.numero_conta}...")
        return conta_obj.sacar(valor_aposta, descricao=f"Pagamento Jogo: {nome_jogo}") # Reutiliza sacar

    def receber_premio_jogo(self, conta_obj, valor_premio, nome_jogo="Jogo Padrão"):
        """Credita prêmio na conta."""
        if not isinstance(conta_obj, Conta): return False
        print(f"-> Tentando creditar R${valor_premio:.2f} do '{nome_jogo}' na conta {conta_obj.numero_conta}...")
        return conta_obj.depositar(valor_premio, descricao=f"Prêmio Jogo: {nome_jogo}") # Reutiliza depositar

    def obter_detalhes_conta_com_cliente(self, id_conta):
        """
        DEMONSTRAÇÃO DE JOIN: Obtém detalhes da conta e do nome/CPF do cliente proprietário.
        Retorna um dicionário com os dados combinados ou None.
        """
        sql = """
            SELECT 
                co.id_conta, co.numero_conta, co.agencia, co.saldo, co.tipo_conta, co.data_abertura,
                cl.id_cliente, cl.nome AS nome_cliente, cl.cpf AS cpf_cliente
            FROM Contas co
            JOIN Clientes cl ON co.id_cliente = cl.id_cliente
            WHERE co.id_conta = %s
        """
        dados_combinados = executar_query(sql, (id_conta,), fetch_one=True)

    def consultar_saldo(self, id_conta_atual):
        """
        Consulta o saldo da conta pelo id_conta.
        Retorna o saldo como float ou None se não encontrar.
        """
        sql = "SELECT saldo FROM Contas WHERE id_conta = %s"
        resultado = executar_query(sql, (id_conta_atual,), fetch_one=True)
        if resultado and 'saldo' in resultado:
            return float(resultado['saldo'])
        return None
    
        if dados_combinados:
            print(f"-> Detalhes da Conta ID {id_conta} (com JOIN):")
            print(f"   Conta: {dados_combinados['agencia']}-{dados_combinados['numero_conta']}, Saldo: R${float(dados_combinados['saldo']):.2f}")
            print(f"   Cliente: {dados_combinados['nome_cliente']} (CPF: {dados_combinados['cpf_cliente']})")
            return dados_combinados
        else:
            print(f"!! Nenhum detalhe encontrado para conta ID {id_conta} com JOIN.")
            return None


# --- Bloco Principal e Menu Interativo (Adaptado para Classes) ---
def menu_interativo_classes():
    banco = SistemaBancario() # Instancia o sistema bancário
    cliente_logado_obj = None # Armazena o objeto Cliente logado
    conta_selecionada_obj = None # Armazena o objeto Conta selecionada

    while True:
        print("\n--- GeminiBank (Orientado a Objetos) ---")
        if cliente_logado_obj:
            print(f"Logado como: {cliente_logado_obj.nome} (ID: {cliente_logado_obj.id_cliente})")
            if conta_selecionada_obj:
                print(f"Operando na Conta: {conta_selecionada_obj.numero_conta} (Saldo: R${conta_selecionada_obj.saldo:.2f})")
        else:
            print("Nenhum cliente logado.")

        print("\n1. Registrar Novo Cliente")
        print("2. Login Cliente")
        if cliente_logado_obj:
            print("3. Criar Nova Conta Bancária")
            print("4. Listar/Selecionar Minhas Contas")
            if conta_selecionada_obj:
                print("5. Consultar Saldo da Conta Selecionada")
                print("6. Realizar Depósito na Conta Selecionada")
                print("7. Realizar Saque da Conta Selecionada")
                print("8. Ver Extrato da Conta Selecionada")
                print("9. Cadastrar Chave PIX para Conta Selecionada")
                print("10. Realizar PIX da Conta Selecionada")
                print("11. Pagar Jogo (Conta Selecionada)")
                print("12. Receber Prêmio (Conta Selecionada)")
                print("13. Ver Detalhes da Conta com JOIN (Demo)")
            print("14. Logout")
        print("0. Sair")
        print("99. (Admin) Recriar Tabelas do Banco")

        escolha = input("Escolha uma opção: ")

        if escolha == '99':
            confirm = input("!! ATENÇÃO: Isso apagará todos os dados. Continuar (S/N)? ").upper()
            if confirm == 'S':
                criar_tabelas_db_inicial()
        
        elif escolha == '1':
            nome = input("Nome completo: ")
            cpf = input("CPF (XXX.XXX.XXX-XX): ")
            senha = input("Senha: ")
            banco.registrar_cliente(nome, cpf, senha)

        elif escolha == '2':
            if cliente_logado_obj: print("!! Já existe um cliente logado. Faça logout primeiro."); continue
            cpf = input("CPF: ")
            senha = input("Senha: ")
            cliente_logado_obj = banco.login_cliente(cpf, senha)
            if cliente_logado_obj:
                banco.carregar_contas_do_cliente(cliente_logado_obj) # Carrega contas ao logar
                conta_selecionada_obj = None # Reseta seleção de conta
            else:
                print("!! Falha no login.")
        
        elif escolha == '0':
            print("Saindo do sistema...")
            break

        # Opções que requerem cliente logado
        elif cliente_logado_obj:
            if escolha == '3':
                tipo = input("Tipo da conta (CORRENTE/POUPANCA): ")
                saldo_str = input("Saldo inicial (ex: 100.00, default 0): ") or "0.00"
                try:
                    saldo = float(saldo_str)
                    nova_conta = banco.criar_conta_bancaria(cliente_logado_obj, tipo, saldo)
                    if nova_conta: # Atualiza a lista de contas do cliente no objeto
                        banco.carregar_contas_do_cliente(cliente_logado_obj)
                except ValueError:
                    print("!! Saldo inicial inválido.")
            
            elif escolha == '4': # Listar/Selecionar Contas
                if not cliente_logado_obj.contas:
                    banco.carregar_contas_do_cliente(cliente_logado_obj) # Tenta carregar se estiver vazia
                if not cliente_logado_obj.contas:
                    print("-> Você não possui contas. Crie uma primeiro (opção 3).")
                else:
                    print("\nSuas Contas:")
                    for i, conta_obj_iter in enumerate(cliente_logado_obj.contas):
                        print(f"  {i+1}. {conta_obj_iter}")
                    try:
                        sel_idx = int(input("Digite o número da conta para selecionar (0 para nenhuma): "))
                        if 0 < sel_idx <= len(cliente_logado_obj.contas):
                            conta_selecionada_obj = cliente_logado_obj.contas[sel_idx-1]
                            # Garante que o saldo do objeto está atualizado com o BD
                            conta_selecionada_obj.consultar_saldo_db() 
                            print(f"-> Conta {conta_selecionada_obj.numero_conta} selecionada.")
                        elif sel_idx == 0:
                            conta_selecionada_obj = None
                            print("-> Nenhuma conta selecionada.")
                        else:
                            print("!! Seleção inválida.")
                    except ValueError:
                        print("!! Entrada inválida.")
            
            elif escolha == '14': # Logout
                print(f"-> {cliente_logado_obj.nome} deslogado.")
                cliente_logado_obj = None
                conta_selecionada_obj = None

            # Opções que requerem conta selecionada
            elif conta_selecionada_obj:
                if escolha == '5': # Consultar Saldo
                    saldo_atualizado = conta_selecionada_obj.consultar_saldo_db()
                    if saldo_atualizado is not None:
                        print(f"-> Saldo da conta {conta_selecionada_obj.numero_conta}: R${saldo_atualizado:.2f}")
                    else:
                        print(f"!! Não foi possível obter o saldo da conta {conta_selecionada_obj.numero_conta}.")
                
                elif escolha == '6': # Depósito
                    try:
                        valor = float(input("Valor do depósito: R$ "))
                        desc = input("Descrição (opcional): ")
                        conta_selecionada_obj.depositar(valor, desc)
                    except ValueError:
                        print("!! Valor inválido para depósito.")
                
                elif escolha == '7': # Saque
                    try:
                        valor = float(input("Valor do saque: R$ "))
                        desc = input("Descrição (opcional): ")
                        conta_selecionada_obj.sacar(valor, desc)
                    except ValueError:
                        print("!! Valor inválido para saque.")

                elif escolha == '8': # Extrato
                    print(f"\n--- Extrato da Conta {conta_selecionada_obj.numero_conta} ---")
                    transacoes = conta_selecionada_obj.obter_extrato_db()
                    if transacoes:
                        for t in transacoes:
                            print(f"  {t['data_transacao']} | {t['tipo_transacao']:<15} | R${float(t['valor']):9.2f} | {t['descricao'] or ''}")
                    else:
                        print("  Nenhuma transação encontrada.")
                    print("------------------------------------")

                elif escolha == '9': # Cadastrar Chave PIX
                    tipo_c = input("Tipo da chave (CPF, EMAIL, TELEFONE, ALEATORIA): ")
                    valor_c = input("Valor da chave: ")
                    conta_selecionada_obj.cadastrar_chave_pix_db(tipo_c, valor_c)
                
                elif escolha == '10': # Realizar PIX
                    chave_dest = input("Chave PIX de destino: ")
                    try:
                        valor = float(input("Valor do PIX: R$ "))
                        banco.realizar_pix(conta_selecionada_obj, chave_dest, valor)
                    except ValueError:
                        print("!! Valor inválido para PIX.")
                
                elif escolha == '11': # Pagar Jogo
                    try:
                        valor = float(input("Valor da aposta/pagamento: R$ "))
                        nome_jogo = input("Nome do Jogo (opcional): ") or "Jogo Padrão"
                        banco.pagar_jogo(conta_selecionada_obj, valor, nome_jogo)
                    except ValueError:
                        print("!! Valor inválido para pagamento do jogo.")

                elif escolha == '12': # Receber Prêmio
                    try:
                        valor = float(input("Valor do prêmio: R$ "))
                        nome_jogo = input("Nome do Jogo (opcional): ") or "Prêmio Padrão"
                        banco.receber_premio_jogo(conta_selecionada_obj, valor, nome_jogo)
                    except ValueError:
                        print("!! Valor inválido para prêmio do jogo.")
                
                elif escolha == '13': # Demo JOIN
                    banco.obter_detalhes_conta_com_cliente(conta_selecionada_obj.id_conta)

                else:
                    if escolha not in ['1','2','3','4','14','0','99']: # Evita msg de opção inválida para opções válidas sem conta
                        print("!! Opção inválida ou requer uma ação diferente primeiro.")
            
            elif escolha not in ['1','2','3','4','14','0','99']: # Se não há conta selecionada e a opção requer uma
                 print("!! Selecione uma conta primeiro (opção 4).")
        
        elif escolha not in ['1','2','0','99']: # Se não há cliente logado e a opção requer login
            print("!! Faça login primeiro (opção 2).")


if __name__ == "__main__":
    print("Sistema Bancário Orientado a Objetos")
    # Recomenda-se rodar a opção 99 do menu para (re)criar as tabelas na primeira vez.
    menu_interativo_classes()