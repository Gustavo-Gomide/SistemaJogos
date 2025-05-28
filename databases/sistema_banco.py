import mysql.connector
from mysql.connector import Error
import hashlib
import random
import string

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '81472529',
    'database': 'meu_banco_digital',
    'port': 3306
}

SQL_SCHEMA_CREATION = [
    "DROP TABLE IF EXISTS Transacoes;",
    "DROP TABLE IF EXISTS Chaves_Pix;",
    "DROP TABLE IF EXISTS Contas;",
    "DROP TABLE IF EXISTS Clientes;",
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


def conectar_bd():
    global DB_CONFIG
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            temp_db_config_connect = DB_CONFIG.copy()
            db_name_to_create_connect = temp_db_config_connect.pop('database')
            conn_server_connect = None
            try:
                conn_server_connect = mysql.connector.connect(**temp_db_config_connect)
                if conn_server_connect.is_connected():
                    cursor_connect = conn_server_connect.cursor()
                    cursor_connect.execute(
                        f"CREATE DATABASE IF NOT EXISTS {db_name_to_create_connect} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    cursor_connect.close()
                    conn_after_create = mysql.connector.connect(**DB_CONFIG)
                    if conn_after_create.is_connected():
                        return conn_after_create
            except Error as server_e_connect:
                print(f"Erro conectar/criar DB: {server_e_connect}")
                return None
            finally:
                if conn_server_connect and conn_server_connect.is_connected():
                    conn_server_connect.close()
        else:
            print(f"Erro ao conectar: {e}")
            return None
    return None


def executar_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    conn_exec = None
    cursor_exec = None
    try:
        conn_exec = conectar_bd()
        if not conn_exec:
            return None
        cursor_exec = conn_exec.cursor(dictionary=True)
        if params:
            cursor_exec.execute(query, params)
        else:
            cursor_exec.execute(query)
        if commit:
            conn_exec.commit()
            return True
        if fetch_one:
            return cursor_exec.fetchone()
        if fetch_all:
            return cursor_exec.fetchall()
        return True
    except Error as e_exec:
        if conn_exec and commit:
            try:
                conn_exec.rollback()
            except Error:
                pass
        print(f"Erro query: {e_exec}")
        return None
    finally:
        if cursor_exec:
            cursor_exec.close()
        if conn_exec and conn_exec.is_connected():
            conn_exec.close()


def criar_tabelas_no_bd():
    global SQL_SCHEMA_CREATION
    conn_crt_tbl = None
    cursor_crt_tbl = None
    try:
        conn_crt_tbl = conectar_bd()
        if not conn_crt_tbl:
            return False
        cursor_crt_tbl = conn_crt_tbl.cursor()
        for statement_group_crt_tbl in SQL_SCHEMA_CREATION:
            for statement_crt_tbl in statement_group_crt_tbl.split(';'):
                statement_stripped_crt_tbl = statement_crt_tbl.strip()
                if statement_stripped_crt_tbl:
                    try:
                        cursor_crt_tbl.execute(statement_stripped_crt_tbl)
                    except Error as e_crt_tbl_inner:
                        if "Unknown table" in str(
                                e_crt_tbl_inner) and "DROP TABLE" in statement_stripped_crt_tbl.upper():
                            pass
                        else:
                            print(f"Erro ao executar: {statement_stripped_crt_tbl[:50]}... Erro: {e_crt_tbl_inner}")
                            raise
        conn_crt_tbl.commit()
        return True
    except Error as e_crt_tbl_outer:
        print(f"Erro criar tabelas: {e_crt_tbl_outer}")
        if conn_crt_tbl:
            try:
                conn_crt_tbl.rollback()
            except Error:
                pass
        return False
    finally:
        if cursor_crt_tbl:
            cursor_crt_tbl.close()
        if conn_crt_tbl and conn_crt_tbl.is_connected():
            conn_crt_tbl.close()


def _hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()


def registrar_cliente(nome, cpf, senha):
    query_verificar_cpf = "SELECT id_cliente FROM Clientes WHERE cpf = %s"
    if executar_query(query_verificar_cpf, (cpf,), fetch_one=True):
        print(f"CPF '{cpf}' já cadastrado.")
        return None
    senha_hashed = _hash_senha(senha)
    query_insert = "INSERT INTO Clientes (nome, cpf, senha_hash) VALUES (%s, %s, %s)"
    params = (nome, cpf, senha_hashed)
    if executar_query(query_insert, params, commit=True):
        cliente_criado = executar_query("SELECT id_cliente FROM Clientes WHERE cpf = %s", (cpf,), fetch_one=True)
        return cliente_criado['id_cliente'] if cliente_criado else None
    return None


def login_cliente(cpf, senha):
    query_select = "SELECT id_cliente, senha_hash FROM Clientes WHERE cpf = %s"
    cliente_data = executar_query(query_select, (cpf,), fetch_one=True)
    if cliente_data:
        if cliente_data['senha_hash'] == _hash_senha(senha):
            return cliente_data['id_cliente']
        print("Senha incorreta.")
        return None
    print(f"CPF '{cpf}' não encontrado.")
    return None


def _gerar_numero_conta_aleatorio():
    return ''.join(random.choices(string.digits, k=8))


def _gerar_agencia_padrao():
    return "0001"


def criar_conta_bancaria(id_cliente, tipo_conta="CORRENTE", saldo_inicial=0.00):
    numero_conta = _gerar_numero_conta_aleatorio()
    agencia = _gerar_agencia_padrao()
    query_verificar_conta = "SELECT id_conta FROM Contas WHERE numero_conta = %s AND agencia = %s"
    while executar_query(query_verificar_conta, (numero_conta, agencia), fetch_one=True):
        numero_conta = _gerar_numero_conta_aleatorio()
    query_insert = "INSERT INTO Contas (id_cliente, numero_conta, agencia, tipo_conta, saldo) VALUES (%s, %s, %s, %s, %s)"
    params = (id_cliente, numero_conta, agencia, tipo_conta.upper(), saldo_inicial)
    if executar_query(query_insert, params, commit=True):
        conta_criada = executar_query("SELECT id_conta FROM Contas WHERE numero_conta = %s AND agencia = %s",
                                      (numero_conta, agencia), fetch_one=True)
        return conta_criada['id_conta'] if conta_criada else None
    return None


def consultar_saldo(id_conta):
    query = "SELECT saldo FROM Contas WHERE id_conta = %s"
    resultado = executar_query(query, (id_conta,), fetch_one=True)
    return resultado['saldo'] if resultado is not None else None


def _registrar_transacao_db(cursor_reg, id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao=""):
    query_insert_transacao = "INSERT INTO Transacoes (id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao) VALUES (%s, %s, %s, %s, %s)"
    params_transacao = (id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao)
    cursor_reg.execute(query_insert_transacao, params_transacao)


def realizar_deposito(id_conta_destino, valor, descricao="Depósito em conta"):
    if not isinstance(valor, (int, float)) or valor <= 0:
        print("Valor do depósito inválido.")
        return False
    conn_dep = None
    cursor_dep = None
    try:
        conn_dep = conectar_bd()
        if not conn_dep: return False
        cursor_dep = conn_dep.cursor()
        cursor_dep.execute("START TRANSACTION")
        query_update_saldo = "UPDATE Contas SET saldo = saldo + %s WHERE id_conta = %s"
        cursor_dep.execute(query_update_saldo, (valor, id_conta_destino))
        if cursor_dep.rowcount == 0:
            cursor_dep.execute("ROLLBACK")
            return False
        _registrar_transacao_db(cursor_dep, None, id_conta_destino, "DEPOSITO", valor, descricao)
        conn_dep.commit()
        return True
    except Error as e_dep:
        if conn_dep: conn_dep.rollback()
        print(f"Erro depósito: {e_dep}")
        return False
    finally:
        if cursor_dep: cursor_dep.close()
        if conn_dep and conn_dep.is_connected(): conn_dep.close()


def realizar_saque(id_conta_origem, valor, descricao="Saque em conta"):
    if not isinstance(valor, (int, float)) or valor <= 0:
        print("Valor do saque inválido.")
        return False
    conn_saq = None
    cursor_saq = None
    try:
        conn_saq = conectar_bd()
        if not conn_saq: return False
        cursor_saq = conn_saq.cursor(dictionary=True)
        cursor_saq.execute("START TRANSACTION")
        query_saldo = "SELECT saldo FROM Contas WHERE id_conta = %s FOR UPDATE"
        cursor_saq.execute(query_saldo, (id_conta_origem,))
        conta = cursor_saq.fetchone()
        if not conta:
            cursor_saq.execute("ROLLBACK")
            return False
        if conta['saldo'] < valor:
            print("Saldo insuficiente.")
            cursor_saq.execute("ROLLBACK")
            return False
        query_update_saldo = "UPDATE Contas SET saldo = saldo - %s WHERE id_conta = %s"
        cursor_saq.execute(query_update_saldo, (valor, id_conta_origem))
        _registrar_transacao_db(cursor_saq, id_conta_origem, None, "SAQUE", valor, descricao)
        conn_saq.commit()
        return True
    except Error as e_saq:
        if conn_saq: conn_saq.rollback()
        print(f"Erro saque: {e_saq}")
        return False
    finally:
        if cursor_saq: cursor_saq.close()
        if conn_saq and conn_saq.is_connected(): conn_saq.close()


def cadastrar_chave_pix(id_conta, tipo_chave, valor_chave):
    tipo_chave = tipo_chave.upper()
    if tipo_chave not in ["CPF", "EMAIL", "TELEFONE", "ALEATORIA"]:
        print("Tipo de chave PIX inválido.")
        return None
    query_verificar_chave = "SELECT id_chave_pix FROM Chaves_Pix WHERE valor_chave = %s"
    if executar_query(query_verificar_chave, (valor_chave,), fetch_one=True):
        print(f"Chave Pix '{valor_chave}' já cadastrada.")
        return None
    query_insert = "INSERT INTO Chaves_Pix (id_conta, tipo_chave, valor_chave) VALUES (%s, %s, %s)"
    if executar_query(query_insert, (id_conta, tipo_chave, valor_chave), commit=True):
        chave = executar_query("SELECT id_chave_pix FROM Chaves_Pix WHERE valor_chave = %s", (valor_chave,),
                               fetch_one=True)
        return chave['id_chave_pix'] if chave else None
    return None


def consultar_conta_por_chave_pix(valor_chave):
    query = "SELECT c.id_conta, c.numero_conta, c.agencia, cl.nome as nome_cliente, cl.cpf as cpf_cliente FROM Chaves_Pix cp JOIN Contas c ON cp.id_conta = c.id_conta JOIN Clientes cl ON c.id_cliente = cl.id_cliente WHERE cp.valor_chave = %s"
    return executar_query(query, (valor_chave,), fetch_one=True)


def realizar_pix(id_conta_origem, chave_pix_destino, valor):
    if not isinstance(valor, (int, float)) or valor <= 0:
        print("Valor do PIX inválido.")
        return False
    conn_pix = None
    cursor_pix = None
    try:
        conn_pix = conectar_bd()
        if not conn_pix: return False
        cursor_pix = conn_pix.cursor(dictionary=True)
        cursor_pix.execute("START TRANSACTION")

        query_origem = "SELECT saldo, id_cliente FROM Contas WHERE id_conta = %s FOR UPDATE"
        cursor_pix.execute(query_origem, (id_conta_origem,))
        conta_origem_data = cursor_pix.fetchone()

        if not conta_origem_data:
            cursor_pix.execute("ROLLBACK")
            return False
        if conta_origem_data['saldo'] < valor:
            print("Saldo insuficiente.")
            cursor_pix.execute("ROLLBACK")
            return False

        cursor_pix.execute("SELECT nome FROM Clientes WHERE id_cliente = %s", (conta_origem_data['id_cliente'],))
        cliente_origem_info = cursor_pix.fetchone()
        nome_cliente_origem = cliente_origem_info['nome'] if cliente_origem_info else "Desconhecido"

        dados_conta_destino_obj = consultar_conta_por_chave_pix(chave_pix_destino)

        if not dados_conta_destino_obj:
            print(f"Chave Pix destino '{chave_pix_destino}' não encontrada.")
            cursor_pix.execute("ROLLBACK")
            return False

        id_conta_destino = dados_conta_destino_obj['id_conta']
        nome_cliente_destino = dados_conta_destino_obj['nome_cliente']

        if id_conta_origem == id_conta_destino:
            print("PIX para mesma conta não permitido.")
            cursor_pix.execute("ROLLBACK")
            return False

        cursor_pix.execute("SELECT id_conta FROM Contas WHERE id_conta = %s FOR UPDATE", (id_conta_destino,))

        query_debitar = "UPDATE Contas SET saldo = saldo - %s WHERE id_conta = %s"
        cursor_pix.execute(query_debitar, (valor, id_conta_origem))
        query_creditar = "UPDATE Contas SET saldo = saldo + %s WHERE id_conta = %s"
        cursor_pix.execute(query_creditar, (valor, id_conta_destino))

        desc_origem = f"PIX Enviado para {nome_cliente_destino} (Chave: {chave_pix_destino})"
        _registrar_transacao_db(cursor_pix, id_conta_origem, id_conta_destino, "PIX_ENVIADO", valor, desc_origem)
        desc_destino = f"PIX Recebido de {nome_cliente_origem}"
        _registrar_transacao_db(cursor_pix, id_conta_origem, id_conta_destino, "PIX_RECEBIDO", valor, desc_destino)

        conn_pix.commit()
        return True
    except Error as e_pix:
        if conn_pix: conn_pix.rollback()
        print(f"Erro PIX: {e_pix}")
        return False
    finally:
        if cursor_pix: cursor_pix.close()
        if conn_pix and conn_pix.is_connected(): conn_pix.close()


def extrato(id_conta):
    query = "SELECT t.data_transacao, t.tipo_transacao, t.valor, t.descricao, co_orig.numero_conta as num_conta_origem, cl_orig.nome as nome_cliente_origem, co_dest.numero_conta as num_conta_destino, cl_dest.nome as nome_cliente_destino FROM Transacoes t LEFT JOIN Contas co_orig ON t.id_conta_origem = co_orig.id_conta LEFT JOIN Clientes cl_orig ON co_orig.id_cliente = cl_orig.id_cliente LEFT JOIN Contas co_dest ON t.id_conta_destino = co_dest.id_conta LEFT JOIN Clientes cl_dest ON co_dest.id_cliente = cl_dest.id_cliente WHERE t.id_conta_origem = %s OR t.id_conta_destino = %s ORDER BY t.data_transacao DESC, t.id_transacao DESC"
    transacoes = executar_query(query, (id_conta, id_conta), fetch_all=True)
    if transacoes:
        print(f"\n--- Extrato Conta ID {id_conta} ---")
        for t in transacoes:
            data_hora = t['data_transacao'].strftime('%d/%m/%Y %H:%M:%S')
            tipo = t['tipo_transacao']
            valor_f = f"{t['valor']:.2f}"
            desc = t['descricao'] or ""
            if tipo == 'DEPOSITO':
                print(f"{data_hora} | {tipo:<15} | + R$ {valor_f:<10} | {desc}")
            elif tipo == 'SAQUE':
                print(f"{data_hora} | {tipo:<15} | - R$ {valor_f:<10} | {desc}")
            elif tipo == 'PIX_ENVIADO':
                dest = t['nome_cliente_destino'] or t['num_conta_destino'] or "N/A"; print(
                    f"{data_hora} | {tipo:<15} | - R$ {valor_f:<10} | Para: {dest} ({desc})")
            elif tipo == 'PIX_RECEBIDO':
                orig = t['nome_cliente_origem'] or t['num_conta_origem'] or "N/A"; print(
                    f"{data_hora} | {tipo:<15} | + R$ {valor_f:<10} | De: {orig} ({desc})")
            elif tipo == 'PAGAMENTO_JOGO':
                print(f"{data_hora} | {tipo:<15} | - R$ {valor_f:<10} | {desc}")
            elif tipo == 'PREMIO_JOGO':
                print(f"{data_hora} | {tipo:<15} | + R$ {valor_f:<10} | {desc}")
            else:
                print(f"{data_hora} | {tipo:<15} |   R$ {valor_f:<10} | {desc}")
        print("--- Fim Extrato ---")
        return transacoes
    print("Nenhuma transação.")
    return []


def pagar_jogo(id_conta_jogador, valor_aposta, nome_jogo="Jogo Padrão"):
    desc_trans = f"Pagamento/Aposta: {nome_jogo}"
    conn_pg = None
    cursor_pg = None
    try:
        conn_pg = conectar_bd()
        if not conn_pg: return False
        cursor_pg = conn_pg.cursor(dictionary=True)
        cursor_pg.execute("START TRANSACTION")
        query_saldo = "SELECT saldo FROM Contas WHERE id_conta = %s FOR UPDATE"
        cursor_pg.execute(query_saldo, (id_conta_jogador,))
        conta = cursor_pg.fetchone()
        if not conta: cursor_pg.execute("ROLLBACK"); return False
        if conta['saldo'] < valor_aposta: print("Saldo insuficiente para jogo."); cursor_pg.execute(
            "ROLLBACK"); return False
        query_update_saldo = "UPDATE Contas SET saldo = saldo - %s WHERE id_conta = %s"
        cursor_pg.execute(query_update_saldo, (valor_aposta, id_conta_jogador))
        _registrar_transacao_db(cursor_pg, id_conta_jogador, None, "PAGAMENTO_JOGO", valor_aposta, desc_trans)
        conn_pg.commit()
        return True
    except Error as e_pg:
        if conn_pg: conn_pg.rollback()
        print(f"Erro pagar jogo: {e_pg}")
        return False
    finally:
        if cursor_pg: cursor_pg.close()
        if conn_pg and conn_pg.is_connected(): conn_pg.close()


def receber_premio_jogo(id_conta_jogador, valor_premio, nome_jogo="Jogo Padrão"):
    desc_trans = f"Prêmio: {nome_jogo}"
    conn_rp = None
    cursor_rp = None
    try:
        conn_rp = conectar_bd()
        if not conn_rp: return False
        cursor_rp = conn_rp.cursor()
        cursor_rp.execute("START TRANSACTION")
        query_update_saldo = "UPDATE Contas SET saldo = saldo + %s WHERE id_conta = %s"
        cursor_rp.execute(query_update_saldo, (valor_premio, id_conta_jogador))
        if cursor_rp.rowcount == 0: cursor_rp.execute("ROLLBACK"); return False
        _registrar_transacao_db(cursor_rp, None, id_conta_jogador, "PREMIO_JOGO", valor_premio, desc_trans)
        conn_rp.commit()
        return True
    except Error as e_rp:
        if conn_rp: conn_rp.rollback()
        print(f"Erro receber prêmio: {e_rp}")
        return False
    finally:
        if cursor_rp: cursor_rp.close()
        if conn_rp and conn_rp.is_connected(): conn_rp.close()


def menu_interativo_simples():
    print("\n--- Bem-vindo ao Banco Digital Unificado ---")
    cliente_logado_id = None
    conta_selecionada_id = None
    while True:
        print("\nOpções:")
        print("1. Registrar Cliente")
        print("2. Login")
        if cliente_logado_id:
            print(f"--- Cliente ID: {cliente_logado_id} ---")
            print("3. Criar Conta")
            print("12. Listar/Selecionar Contas")
            if conta_selecionada_id:
                print(f"--- Conta ID: {conta_selecionada_id} ---")
                print("4. Saldo")
                print("5. Depósito")
                print("6. Saque")
                print("7. Extrato")
                print("8. Cadastrar Chave PIX")
                print("9. Realizar PIX")
                print("10. Pagar Jogo")
                print("11. Receber Prêmio")
            print("13. Logout Cliente")
        print("0. Sair")
        print("99. RODAR CENÁRIO DE TESTES AUTOMÁTICO (APAGA DADOS EXISTENTES)")

        escolha = input("Escolha: ")

        if escolha == '99':
            print("ATENÇÃO: O CENÁRIO DE TESTES IRÁ APAGAR DADOS EXISTENTES E RECRIA A ESTRUTURA.")
            confirm = input("Deseja continuar? (S/N): ").upper()
            if confirm == 'S':
                cenario_de_testes_automatico()
            else:
                print("Cenário de testes cancelado.")
            continue
        try:
            if escolha == '1':
                nome = input("Nome: ");
                cpf = input("CPF: ");
                senha = input("Senha: ")
                novo_id = registrar_cliente(nome, cpf, senha)
                if novo_id: print(f"Cliente ID {novo_id} registrado.")
            elif escolha == '2':
                if cliente_logado_id: print("Já logado."); continue
                cpf = input("CPF: ");
                senha = input("Senha: ")
                cliente_logado_id = login_cliente(cpf, senha)
                if cliente_logado_id: print(f"Login OK. Cliente ID: {cliente_logado_id}. Use opção 12 para contas.")
            elif escolha == '12' and cliente_logado_id:
                contas = executar_query(
                    "SELECT id_conta, tipo_conta, agencia, numero_conta, saldo FROM Contas WHERE id_cliente = %s",
                    (cliente_logado_id,), fetch_all=True)
                if contas:
                    print("\nSuas Contas:")
                    for i, c in enumerate(contas): print(
                        f"  {i + 1}. {c['tipo_conta']} Ag:{c['agencia']} Cc:{c['numero_conta']} Saldo:R${c['saldo']:.2f} [ID:{c['id_conta']}]")
                    sel = int(input("Nº da conta (0 para nenhuma): "))
                    if 0 < sel <= len(contas):
                        conta_selecionada_id = contas[sel - 1]['id_conta']; print(
                            f"Conta ID {conta_selecionada_id} selecionada.")
                    elif sel == 0:
                        conta_selecionada_id = None; print("Nenhuma conta selecionada.")
                    else:
                        print("Seleção inválida.")
                else:
                    print("Nenhuma conta. Crie uma (opção 3)."); conta_selecionada_id = None
            elif escolha == '3' and cliente_logado_id:
                tc = input("Tipo (CORRENTE/POUPANCA): ") or "CORRENTE";
                si_str = input("Saldo inicial (0.00): ") or "0.00"
                si = float(si_str)
                nc_id = criar_conta_bancaria(cliente_logado_id, tc, si)
                if nc_id: print(f"Conta ID {nc_id} criada. Use opção 12.")
            elif escolha == '4' and conta_selecionada_id:
                s = consultar_saldo(conta_selecionada_id)
                if s is not None: print(f"Saldo: R$ {s:.2f}")
            elif escolha == '5' and conta_selecionada_id:
                v = float(input("Valor depósito: R$ "));
                d = input("Descrição: ")
                if realizar_deposito(conta_selecionada_id, v, d or f"Depósito cta {conta_selecionada_id}"): print(
                    "Depósito OK.")
            elif escolha == '6' and conta_selecionada_id:
                v = float(input("Valor saque: R$ "));
                d = input("Descrição: ")
                if realizar_saque(conta_selecionada_id, v, d or f"Saque cta {conta_selecionada_id}"): print("Saque OK.")
            elif escolha == '7' and conta_selecionada_id:
                extrato(conta_selecionada_id)
            elif escolha == '8' and conta_selecionada_id:
                tip = input("Tipo PIX (CPF,EMAIL,TELEFONE,ALEATORIA): ").upper();
                val_c = input(f"Valor chave ({tip}): ")
                if tip == "ALEATORIA" and not val_c: val_c = "rand-" + ''.join(
                    random.choices(string.digits, k=10)); print(f"Chave aleatória: {val_c}")
                cadastrar_chave_pix(conta_selecionada_id, tip, val_c)
            elif escolha == '9' and conta_selecionada_id:
                chave_d = input("Chave PIX destino: ");
                v = float(input("Valor PIX: R$ "))
                if realizar_pix(conta_selecionada_id, chave_d, v): print("PIX OK.")
            elif escolha == '10' and conta_selecionada_id:
                v = float(input("Valor aposta: R$ "));
                nj = input("Nome jogo: ") or "Jogo X"
                if pagar_jogo(conta_selecionada_id, v, nj): print("Pagamento jogo OK.")
            elif escolha == '11' and conta_selecionada_id:
                v = float(input("Valor prêmio: R$ "));
                nj = input("Nome jogo: ") or "Jogo Y"
                if receber_premio_jogo(conta_selecionada_id, v, nj): print("Prêmio creditado OK.")
            elif escolha == '13' and cliente_logado_id:
                print(f"Cliente ID {cliente_logado_id} deslogado.");
                cliente_logado_id = None;
                conta_selecionada_id = None
            elif escolha == '0':
                print("Saindo..."); break
            else:
                if escolha not in ['99']: print("Opção inválida.")
        except ValueError:
            print("Entrada numérica inválida. Tente novamente.")
        except Exception as e_menu:
            print(f"Ocorreu um erro inesperado no menu: {e_menu}")


def cenario_de_testes_automatico():
    print("\n--- CENÁRIO DE TESTES AUTOMÁTICO ---")
    print("Recriando tabelas...")
    if not criar_tabelas_no_bd():
        print("Falha ao recriar tabelas. Abortando testes.")
        return
    print("Tabelas prontas.")

    c1_id = registrar_cliente("Alice Teste", "111.111.111-01", "s1")
    c2_id = registrar_cliente("Beto Teste", "222.222.222-02", "s2")
    if not (c1_id and c2_id): print("Falha registro clientes."); return

    cta_a1_id = criar_conta_bancaria(c1_id, "CORRENTE", 1000.00)
    cta_b1_id = criar_conta_bancaria(c2_id, "POUPANCA", 500.00)
    if not (cta_a1_id and cta_b1_id): print("Falha criar contas."); return

    print(f"Alice (C:{c1_id}, Conta:{cta_a1_id}), Beto (C:{c2_id}, Conta:{cta_b1_id})")

    if realizar_deposito(cta_a1_id, 200.00): print("Depósito Alice OK")
    if realizar_saque(cta_a1_id, 50.00): print("Saque Alice OK")
    print(f"Saldo Alice: {consultar_saldo(cta_a1_id)}")

    if cadastrar_chave_pix(cta_a1_id, "EMAIL", "alice.teste@mail.com"): print("Chave Alice OK")
    if cadastrar_chave_pix(cta_b1_id, "CPF", "222.222.222-02"): print("Chave Beto OK")

    if realizar_pix(cta_a1_id, "222.222.222-02", 100.00):
        print("PIX Alice p/ Beto OK.")
    print(f"Saldo Alice: {consultar_saldo(cta_a1_id)}, Saldo Beto: {consultar_saldo(cta_b1_id)}")

    extrato(cta_a1_id)
    extrato(cta_b1_id)

    if pagar_jogo(cta_a1_id, 25.00, "GameZ"): print("Pagar Jogo Alice OK")
    if receber_premio_jogo(cta_b1_id, 75.00, "SorteGrande"): print("Receber Prêmio Beto OK")
    print(f"Saldo Alice final: {consultar_saldo(cta_a1_id)}, Saldo Beto final: {consultar_saldo(cta_b1_id)}")
    print("--- FIM CENÁRIO DE TESTES ---")


if __name__ == "__main__":
    print("Sistema Bancário Unificado")
    print("AVISO: Se for a primeira execução ou quiser resetar, execute a opção '99' no menu.")
    menu_interativo_simples()
