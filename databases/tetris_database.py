from utilitarios.Aprincipal_database import BancoDados

class TetrisDB(BancoDados):
    colunas = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "apelido": "VARCHAR(50) NOT NULL",
        "pontuacao": "INT NOT NULL",
        "linhas": "INT NOT NULL",
        "data_partida": "DATETIME DEFAULT CURRENT_TIMESTAMP"
    }

    @classmethod
    def criar_tabela(cls):
        BancoDados.criar_tabela("tetris_partidas", cls.colunas)

    @classmethod
    def registrar_partida(cls, apelido, pontuacao, linhas):
        dados = {
            "apelido": apelido,
            "pontuacao": pontuacao,
            "linhas": linhas
        }
        BancoDados.inserir_dados("tetris_partidas", dados)

    @classmethod
    def ranking(cls):
        return BancoDados.consultar_dados("tetris_partidas", "ORDER BY pontuacao DESC LIMIT 10")

    @classmethod
    def historico(cls):
        return BancoDados.consultar_dados("tetris_partidas", "ORDER BY data_partida DESC")