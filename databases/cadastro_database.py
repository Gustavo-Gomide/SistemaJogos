from utilitarios.Aprincipal_database import BancoDados

class DadosUsuario:
    """
    Classe utilitária para operações na tabela de usuários.
    """

    # Estrutura inicial da tabela de usuários
    colunas_usuario = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "nome": "VARCHAR(100) NOT NULL",
        "data_nasc": "DATE NOT NULL",
        "apelido": "VARCHAR(50) NOT NULL UNIQUE",
        "senha": "VARCHAR(100) NOT NULL",
        "tempo_jogo": "INT DEFAULT 0",
        "pontuacao_total": "FLOAT DEFAULT 0"
        # Novos jogos: tempo_jogo_nome, pontuacao_jogo_nome serão adicionados depois
    }

    @classmethod
    def criar_tabela_usuarios(cls):
        """Cria a tabela de usuários no banco de dados."""
        BancoDados.criar_tabela("usuarios", cls.colunas_usuario)

    @classmethod
    def cadastrar_usuario(cls, nome, data_nasc, apelido, senha):
        """Insere um novo usuário na tabela."""
        dados = {
            "nome": nome,
            "data_nasc": data_nasc,  # formato 'YYYY-MM-DD'
            "apelido": apelido,
            "senha": senha,
            "tempo_jogo": 0,
            "pontuacao_total": 0
        }
        BancoDados.inserir_dados("usuarios", dados)

    @classmethod
    def listar_usuarios(cls):
        """Retorna todos os usuários cadastrados."""
        return BancoDados.consultar_dados("usuarios")

    @classmethod
    def atualizar_usuario(cls, apelido, tempo_jogo=None, pontuacao_total=None):
        """Atualiza tempo de jogo e/ou pontuação total de um usuário."""
        dados = {}
        if tempo_jogo is not None:
            dados["tempo_jogo"] = tempo_jogo
        if pontuacao_total is not None:
            dados["pontuacao_total"] = pontuacao_total
        if dados:
            BancoDados.atualizar_dados("usuarios", dados, f"apelido = '{apelido}'")

    @classmethod
    def deletar_usuario(cls, apelido):
        """Remove um usuário pelo apelido."""
        BancoDados.deletar_dados("usuarios", f"apelido = '{apelido}'")

# Para criar a tabela ao rodar este arquivo:
if __name__ == "__main__":
    DadosUsuario.criar_tabela_usuarios()
    # DadosUsuario.cadastrar_usuario("João da Silva", "2000-01-01", "joaosilva", "senha123")
    # print(DadosUsuario.listar_usuarios())