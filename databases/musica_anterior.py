from utilitarios.Aprincipal_database import BancoDados


class MusicaAnterior(BancoDados):
    """
    Classe para gerenciar a tabela de músicas anteriores.
    """
    colunas_musica_anterior = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "musica": "VARCHAR(50) NULL"
    }

    @classmethod
    def criar_tabela_musica_anterior(cls):
        """Cria a tabela de músicas anteriores."""
        BancoDados.criar_tabela("musica_anterior", cls.colunas_musica_anterior)
        # Garante que sempre existe uma linha
        if BancoDados.numero_linhas("musica_anterior") == 0:
            BancoDados.inserir_dados("musica_anterior", {"musica": None})

    @classmethod
    def set_musica_anterior(cls, musica):
        # Atualiza sempre a linha 1
        BancoDados.atualizar_dados("musica_anterior", {"musica": musica}, "id=1")

    @classmethod
    def get_musica_anterior(cls):
        resultado = BancoDados.consultar_dados("musica_anterior")
        if resultado and resultado[0][1]:
            return resultado[0][1]
        return None
