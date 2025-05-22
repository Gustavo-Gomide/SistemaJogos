# navegador.py

class Navegador:
    """
    Classe responsável por gerenciar a navegação entre telas do sistema.

    Como usar:
    ----------
    1. Instancie o navegador:
        navegador = Navegador()
    2. Registre as telas disponíveis:
        navegador.registrar_tela("menu", TelaMenu)
        navegador.registrar_tela("cadastro", TelaCadastro)
        navegador.registrar_tela("musicas", TelaMusicas)
    3. Para trocar de tela:
        navegador.ir_para("menu")

    Atributos:
    ----------
    - telas (dict): Dicionário que armazena as telas registradas.
    - tela_atual: Referência para a tela atualmente exibida.
    - apelido_logado: Armazena o apelido do usuário logado (pode ser acessado por qualquer tela).

    Métodos:
    --------
    - registrar_tela(nome, funcao_construtora): Registra uma tela no sistema.
    - ir_para(nome): Troca para a tela registrada com o nome informado.
    """

    def __init__(self):
        # Dicionário de telas registradas: {"nome": função construtora}
        self.telas = {}
        # Tela atualmente exibida
        self.tela_atual = None
        # Apelido do usuário logado (pode ser usado por todas as telas)
        self.apelido_logado = None
        self.id_logado = None  # ID do usuário logado (pode ser usado por todas as telas)
        self.volume_efeito = 0.7   # Volume global para efeitos (0.0 a 1.0)
        self.volume_fundo = 0.5    # Volume global para fundos/músicas (0.0 a 1.0)

    def registrar_tela(self, nome, funcao_construtora):
        """
        Registra uma tela no sistema.

        Parâmetros:
        -----------
        - nome (str): Nome identificador da tela (ex: "menu", "cadastro").
        - funcao_construtora (callable): Função ou classe que retorna a tela (deve aceitar o navegador como argumento).
        """
        self.telas[nome] = funcao_construtora

    def ir_para(self, nome):
        """
        Troca para a tela registrada com o nome informado.

        Parâmetros:
        -----------
        - nome (str): Nome da tela para exibir.

        Observação:
        -----------
        A tela recebe o próprio navegador como argumento, permitindo acessar atributos globais (como apelido_logado).
        """
        if nome in self.telas:
            tela = self.telas[nome](self)  # Passa o próprio navegador para a tela
            self.tela_atual = tela
            tela.rodar()
        else:
            print(f"Tela '{nome}' não encontrada.")
