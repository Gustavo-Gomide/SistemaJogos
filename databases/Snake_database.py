from utilitarios.Aprincipal_database import BancoDados

class SnakeDB(BancoDados):
    colunas = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "apelido": "VARCHAR(50) NOT NULL",
        "pontuacao": "INT NOT NULL",
        "data_partida": "DATETIME DEFAULT CURRENT_TIMESTAMP"
    }

    @classmethod
    def criar_tabela(cls):
        BancoDados.criar_tabela("snake_partidas", cls.colunas)

    @classmethod
    def registrar_partida(cls, apelido, pontuacao):
        dados = {
            "apelido": apelido,
            "pontuacao": pontuacao
        }
        BancoDados.inserir_dados("snake_partidas", dados)

    @classmethod
    def ranking(cls):
        return BancoDados.consultar_dados("snake_partidas", "ORDER BY pontuacao DESC LIMIT 10")

    @classmethod
    def historico(cls):
        return BancoDados.consultar_dados("snake_partidas", "ORDER BY data_partida DESC")