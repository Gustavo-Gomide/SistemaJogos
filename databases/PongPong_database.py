from utilitarios.Aprincipal_database import BancoDados

class PongPongDB:
    """
    Classe utilitária para operações na tabela de partidas do PongPong.
    """

    colunas_pong = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "id_usuario": "INT",  # FK para usuarios.id
        "apelido": "VARCHAR(50) NOT NULL",
        "pontuacao": "INT NOT NULL",
        "venceu": "BOOLEAN NOT NULL",  # True se venceu, False se perdeu
        "tempo_jogado": "INT NOT NULL",  # segundos
        "data_partida": "DATETIME DEFAULT CURRENT_TIMESTAMP",
        "FOREIGN KEY (id_usuario)": "REFERENCES usuarios(id)"
    }

    @classmethod
    def criar_tabela_pong(cls):
        """Cria a tabela de partidas do PongPong."""
        BancoDados.criar_tabela("pong_partidas", cls.colunas_pong)

    @classmethod
    def registrar_partida(cls, id_usuario, apelido, pontuacao, venceu, tempo_jogado):
        """Registra uma partida do PongPong."""
        dados = {
            "id_usuario": id_usuario,
            "apelido": apelido,
            "pontuacao": pontuacao,
            "venceu": venceu,
            "tempo_jogado": tempo_jogado
        }
        BancoDados.inserir_dados("pong_partidas", dados)

    @classmethod
    def estatisticas_usuario(cls, id_usuario):
        """
        Retorna estatísticas do usuário no Pong:
        total de partidas, vitórias, derrotas, tempo total, porcentagem de vitórias.
        """
        partidas = BancoDados.consultar_dados("pong_partidas", f"id_usuario = {id_usuario}")
        if not partidas:
            return {
                "partidas": 0,
                "vitorias": 0,
                "derrotas": 0,
                "tempo_total": 0,
                "porcentagem_vitorias": 0.0
            }
        total = len(partidas)
        vitorias = sum(1 for p in partidas if p[4])  # venceu == True
        derrotas = total - vitorias
        tempo_total = sum(p[5] for p in partidas)
        porcentagem = (vitorias / total) * 100 if total > 0 else 0.0
        return {
            "partidas": total,
            "vitorias": vitorias,
            "derrotas": derrotas,
            "tempo_total": tempo_total,
            "porcentagem_vitorias": porcentagem
        }

    @classmethod
    def historico_usuario(cls, id_usuario):
        """Retorna todas as partidas do usuário, mais novas primeiro."""
        return BancoDados.consultar_dados(
            "pong_partidas",
            f"id_usuario = {id_usuario} ORDER BY data_partida DESC"
        )

    @classmethod
    def historico_todas_partidas(cls):
        """
        Retorna todas as partidas do PongPong, mais novas primeiro.
        """
        return BancoDados.consultar_dados(
            "pong_partidas",
            "1 ORDER BY data_partida DESC"
        )

# Para criar a tabela ao rodar este arquivo:
if __name__ == "__main__":
    PongPongDB.criar_tabela_pong()