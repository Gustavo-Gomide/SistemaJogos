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
        "pontuacao_total": "FLOAT DEFAULT 0",
        "tempo_jogo_tetris": "INT DEFAULT 0",
        "pontuacao_tetris": "INT DEFAULT 0",
        "tempo_jogo_flappy": "INT DEFAULT 0",
        "pontuacao_flappy": "INT DEFAULT 0",
        "tempo_jogo_dino": "INT DEFAULT 0",
        "pontuacao_dino": "INT DEFAULT 0",
        "tempo_jogo_snake": "INT DEFAULT 0",
        "pontuacao_snake": "INT DEFAULT 0",
        "tempo_jogo_pong": "INT DEFAULT 0",
        "pontuacao_pong": "INT DEFAULT 0",
        "tempo_jogo_velha": "INT DEFAULT 0",
        "pontuacao_velha": "INT DEFAULT 0",
        "tempo_jogo_forca": "INT DEFAULT 0",
        "pontuacao_forca": "INT DEFAULT 0"
    }

    @classmethod
    def criar_tabela_usuarios(cls):
        BancoDados.criar_tabela("usuarios", cls.colunas_usuario)

    @classmethod
    def ranking_global(cls, limite=20):
        return BancoDados.consultar_dados(
            "usuarios",
            f"ORDER BY pontuacao_total DESC LIMIT {limite}",
            colunas=["nome", "tempo_jogo", "pontuacao_total"]
        )

    @classmethod
    def cadastrar_usuario(cls, nome, data_nasc, apelido, senha):
        """Insere um novo usuário na tabela."""
        dados = {
            "nome": nome,
            "data_nasc": data_nasc,  # formato 'YYYY-MM-DD'
            "apelido": apelido,
            "senha": senha,
            "tempo_jogo": 0,
            "pontuacao_total": 0,
            "tempo_jogo_tetris": 0,
            "pontuacao_tetris": 0,
            "tempo_jogo_flappy": 0,
            "pontuacao_flappy": 0,
            "tempo_jogo_dino": 0,
            "pontuacao_dino": 0,
            "tempo_jogo_snake": 0,
            "pontuacao_snake": 0,
            "tempo_jogo_pong": 0,
            "pontuacao_pong": 0,
            "tempo_jogo_velha": 0,
            "pontuacao_velha": 0,
            "pontuacao_forca": 0
        }
        BancoDados.inserir_dados("usuarios", dados)

    @classmethod
    def listar_usuarios(cls):
        """Retorna todos os usuários cadastrados."""
        return BancoDados.consultar_dados("usuarios")

    @classmethod
    def atualizar_pontuacao_jogo(cls, apelido, jogo, pontuacao, tempo=0, soma=True):
        """
        Atualiza a pontuação e tempo de um jogo específico para o usuário.
        jogo: string, ex: 'tetris', 'flappy', 'dino', 'snake', 'pong', 'velha'
        pontuacao: int (pontuação a adicionar ou definir)
        tempo: int (tempo a adicionar ou definir, em segundos)
        soma: se True, soma ao valor atual; se False, define o valor.
        """
        col_pontuacao = f"pontuacao_{jogo}"
        col_tempo = f"tempo_jogo_{jogo}"

        # Busca valores atuais
        usuario = BancoDados.consultar_dados("usuarios", f"WHERE apelido = '{apelido}'", colunas=[col_pontuacao, col_tempo])
        if usuario and len(usuario) > 0:
            atual_pontuacao = usuario[0][0] or 0
            atual_tempo = usuario[0][1] or 0
        else:
            atual_pontuacao = 0
            atual_tempo = 0

        novo_pontuacao = atual_pontuacao + pontuacao if soma else pontuacao
        novo_tempo = atual_tempo + tempo if soma else tempo

        # Atualiza as colunas do jogo
        BancoDados.atualizar_dados(
            "usuarios",
            {col_pontuacao: novo_pontuacao, col_tempo: novo_tempo},
            f"apelido = '{apelido}'"
        )

        # Atualiza os totais
        cls.atualizar_totais(apelido)

    @classmethod
    def atualizar_totais(cls, apelido):
        """Atualiza tempo_jogo e pontuacao_total somando todas as colunas de jogos."""
        usuario = BancoDados.consultar_dados(
            "usuarios",
            f"WHERE apelido = '{apelido}'",
            colunas=[
                "tempo_jogo_tetris", "tempo_jogo_flappy", "tempo_jogo_dino", "tempo_jogo_snake", "tempo_jogo_pong", "tempo_jogo_velha",
                "pontuacao_tetris", "pontuacao_flappy", "pontuacao_dino", "pontuacao_snake", "pontuacao_pong", "pontuacao_velha", "pontuacao_forca"
            ]
        )
        if usuario and len(usuario) > 0:
            tempo_total = sum([usuario[0][i] or 0 for i in range(6)])
            pontos_total = sum([usuario[0][i] or 0 for i in range(6, 12)])
            BancoDados.atualizar_dados(
                "usuarios",
                {"tempo_jogo": tempo_total, "pontuacao_total": pontos_total},
                f"apelido = '{apelido}'"
            )

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