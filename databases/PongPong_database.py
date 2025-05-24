from utilitarios.Aprincipal_database import BancoDados

class PongPongDB:
    """
    Classe utilitária para operações na tabela de partidas do PongPong.
    """

    colunas_pong = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "id_usuario_j1": "INT",
        "apelido_j1": "VARCHAR(50) NOT NULL",
        "id_usuario_j2": "INT NULL",
        "apelido_j2": "VARCHAR(50) NULL",
        "pontuacao_j1": "INT NOT NULL",
        "pontuacao_j2": "INT NULL",
        "vencedor": "VARCHAR(50) NOT NULL",
        "tempo_jogado": "INT NOT NULL",
        "data_partida": "DATETIME DEFAULT CURRENT_TIMESTAMP",
        "FOREIGN KEY (id_usuario_j1)": "REFERENCES usuarios(id)",
        "FOREIGN KEY (id_usuario_j2)": "REFERENCES usuarios(id)"
    }

    @classmethod
    def criar_tabela_pong(cls):
        """Cria a tabela de partidas do PongPong."""
        BancoDados.criar_tabela("pong_partidas", cls.colunas_pong)

    @classmethod
    def registrar_partida(cls, id_usuario_j1, apelido_j1, id_usuario_j2=None, apelido_j2=None, pontuacao_j1=0, pontuacao_j2=None, vencedor="", tempo_jogado=0):
        """Registra uma partida do PongPong."""
        dados = {
            "id_usuario_j1": id_usuario_j1,
            "apelido_j1": apelido_j1,
            "id_usuario_j2": id_usuario_j2,
            "apelido_j2": apelido_j2,
            "pontuacao_j1": pontuacao_j1,
            "pontuacao_j2": pontuacao_j2,
            "vencedor": vencedor,
            "tempo_jogado": tempo_jogado
        }
        BancoDados.inserir_dados("pong_partidas", dados)

    @classmethod
    def query_personalizada(cls, where=None, order=None, limit=None):
        """
        Retorna partidas conforme a query personalizada.
        Exemplo: where="apelido_j1='fulano'", order="data_partida DESC", limit=10
        """
        condicao = ""
        if where:
            condicao += f" WHERE {where}"
        if order:
            condicao += f" ORDER BY {order}"
        if limit:
            condicao += f" LIMIT {limit}"
        print("pong_partidas", condicao if condicao else None)
        return BancoDados.consultar_dados("pong_partidas", condicao if condicao else None)

    @classmethod
    def todas_partidas(cls):
        """Retorna todas as partidas para histórico geral."""
        return cls.query_personalizada(order="data_partida DESC")

    @classmethod
    def partidas_usuario(cls, apelido):
        """Retorna todas as partidas de um usuário (como J1 ou J2)."""
        return cls.query_personalizada(where=f"apelido_j1='{apelido}' OR apelido_j2='{apelido}'", order="data_partida DESC")

    @classmethod
    def ranking(cls):
        """
        Retorna dados sumarizados para ranking.
        Exemplo: SELECT apelido_j1, COUNT(*) as jogos, SUM(vencedor=apelido_j1) as vitorias, ...
        (Você pode implementar uma query SQL customizada aqui se quiser ranking direto do banco)
        """
        # Exemplo simples: retorna todas as partidas para processamento em Python
        return cls.todas_partidas()

    @classmethod
    def estatisticas_usuario(cls, id_usuario):
        """
        Retorna um dicionário com estatísticas do usuário:
        vitorias, derrotas, porcentagem_vitorias.
        """
        partidas = cls.query_personalizada(where=f" id_usuario_j1={id_usuario} OR id_usuario_j2={id_usuario}")
        vitorias = 0
        derrotas = 0
        for partida in partidas or []:
            vencedor = partida[7]
            apelido_j1 = partida[2]
            apelido_j2 = partida[4]
            if (partida[1] == id_usuario and vencedor == apelido_j1) or (partida[3] == id_usuario and vencedor == apelido_j2):
                vitorias += 1
            elif (partida[1] == id_usuario or partida[3] == id_usuario):
                derrotas += 1
        total = vitorias + derrotas
        porcentagem = (vitorias / total * 100) if total > 0 else 0.0
        return {
            "vitorias": vitorias,
            "derrotas": derrotas,
            "porcentagem_vitorias": porcentagem
        }

# Para criar a tabela ao rodar este arquivo:
if __name__ == "__main__":
    PongPongDB.criar_tabela_pong()