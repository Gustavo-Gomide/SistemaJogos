from utilitarios.Aprincipal_database import BancoDados
import json

class BancoDadosVelha(BancoDados):
    @staticmethod
    def criar_tabela():
        colunas = {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "id_usuario_x": "INT NULL",
            "jogador_x": "VARCHAR(50) NOT NULL",
            "id_usuario_o": "INT NULL",
            "jogador_o": "VARCHAR(50) NOT NULL",
            "vencedor": "VARCHAR(50) NOT NULL",
            "data": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
        foreign_keys = [
            "FOREIGN KEY (id_usuario_x) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE",
            "FOREIGN KEY (id_usuario_o) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE"
        ]
        BancoDados.criar_tabela_avancada("tb_resultados", colunas, foreign_keys)

    @staticmethod
    def salvar_resultado(jogador_x, jogador_o, vencedor, id_usuario_x=None, id_usuario_o=None):
        """
        Salva o resultado da partida. id_usuario_x e id_usuario_o podem ser None (visitante).
        """
        dados = {
            "id_usuario_x": id_usuario_x,
            "jogador_x": jogador_x,
            "id_usuario_o": id_usuario_o,
            "jogador_o": jogador_o,
            "vencedor": vencedor
        }
        BancoDados.inserir_dados("tb_resultados", dados)

    @staticmethod
    def criar_tabela_historico():
        colunas = {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "jogador_x": "VARCHAR(100)",
            "jogador_o": "VARCHAR(100)",
            "vencedor": "VARCHAR(100)",
            "jogadas": "TEXT",
            "data_hora": "DATETIME DEFAULT CURRENT_TIMESTAMP"
        }
        BancoDados.criar_tabela("historico_partidas", colunas)

    @staticmethod
    def salvar_partida_no_historico(jogador_x, jogador_o, vencedor, jogadas):
        dados = {
            "jogador_x": jogador_x,
            "jogador_o": jogador_o,
            "vencedor": vencedor,
            "jogadas": json.dumps(jogadas)
        }
        try:
            BancoDados.inserir_dados("historico_partidas", dados)
            return True
        except Exception as e:
            print(f"Erro ao salvar partida no histórico: {e}")
            return False

    @staticmethod
    def buscar_historico():
        resultado = BancoDados.consultar_dados(
            "historico_partidas",
            "ORDER BY data_hora DESC",
            colunas="jogador_x, jogador_o, vencedor, data_hora"
        )
        return resultado if resultado else []

    @staticmethod
    def apagar_historico(id_usuario=None):
        """
        Apaga o histórico apenas se houver um usuário logado.
        :param id_usuario: objeto ou id do usuário logado (pode ser string, int, etc.)
        :return: True se apagou, False caso contrário
        """
        if not id_usuario:
            print("Operação negada: nenhum usuário logado.")
            return False
        try:
            BancoDados.deletar_dados("historico_partidas", "1=1")
            return True
        except Exception as e:
            print(f"Erro ao apagar histórico: {e}")
            return False


