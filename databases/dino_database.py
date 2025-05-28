from utilitarios.Aprincipal_database import BancoDados

class DinoDB(BancoDados):
    @classmethod
    def criar_tabela(cls):
        colunas = {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "id_usuario": "INT NULL",
            "apelido": "VARCHAR(50) NOT NULL",
            "pontuacao": "INT NOT NULL",
            "data_partida": "DATETIME DEFAULT CURRENT_TIMESTAMP"
        }
        foreign_keys = [
            "FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE"
        ]
        BancoDados.criar_tabela_avancada("dino_partidas", colunas, foreign_keys)

    @classmethod
    def registrar_partida(cls, id_usuario=None, apelido='', pontuacao=0):
        dados = {
            "id_usuario": id_usuario,
            "apelido": apelido,
            "pontuacao": pontuacao
        }
        BancoDados.inserir_dados("dino_partidas", dados)

    @classmethod
    def ranking(cls):
        return BancoDados.consultar_dados("dino_partidas", "ORDER BY pontuacao DESC LIMIT 10")

    @classmethod
    def historico(cls):
        return BancoDados.consultar_dados("dino_partidas", "ORDER BY data_partida DESC")