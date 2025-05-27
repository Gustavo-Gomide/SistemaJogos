from utilitarios.Aprincipal_database import BancoDados

class ForcaDB(BancoDados):
    @classmethod
    def criar_tabela(cls):
        colunas = {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "id_usuario": "INT",
            "apelido": "VARCHAR(50) NOT NULL",
            "pontuacao": "INT NOT NULL",
            "data_partida": "DATETIME DEFAULT CURRENT_TIMESTAMP"
            }
        foreign_keys = [
        "FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE"
        ]
        BancoDados.criar_tabela_avancada("forca_partidas", colunas, foreign_keys)

    @classmethod
    def registrar_partida(cls, apelido, pontuacao, id_usuario=None):
        dados = {
            "apelido": apelido,
            "pontuacao": pontuacao
        }
        if id_usuario is not None:
            dados["id_usuario"] = id_usuario
        BancoDados.inserir_dados("forca_partidas", dados)

    @classmethod
    def ranking(cls):
        return BancoDados.consultar_dados("forca_partidas", "ORDER BY pontuacao DESC LIMIT 10")

    @classmethod
    def historico(cls):
        return BancoDados.consultar_dados("forca_partidas", "ORDER BY data_partida DESC")