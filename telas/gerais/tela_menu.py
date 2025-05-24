from utilitarios.musicas import Efeitos
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
import os

def limpar_tela():
    """Limpa o terminal (útil para debug)."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class TelaMenu(Tela):
    """
    Tela principal do menu do sistema.

    Parâmetros:
    -----------
    - navegador: objeto Navegador, responsável pela navegação entre telas.

    Como usar:
    ----------
    Basta registrar a classe no navegador:
        navegador.registrar_tela("menu", TelaMenu)

    O Navegador irá instanciar e rodar a tela automaticamente.
    """

    def __init__(self, navegador):
        # Não precisa tocar música aqui, pois será restaurada ao voltar
        super().__init__(
            largura=900,
            altura=700,
            titulo="Menu Principal",
            cor_fundo=Cores.preto(),
            imagem_fundo='imagem',  # Use uma imagem de fundo pixelada se quiser
            navegador=navegador,
            logo='mulher_cod',
            som_fundo=None,  # Removido para não tocar música automaticamente
            efeito_saida=Efeitos.sair()
        )


        nome_exibicao = navegador.apelido_logado if navegador.apelido_logado else "visitante"

        # Título centralizado - visual retrô, grande, com sombra (ajustado para caber)
        self.adicionar_componente(
            TextoFormatado(
                x=452, y=54, texto='MENU PRINCIPAL',
                tamanho=44, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=450, y=50, texto='MENU PRINCIPAL',
                tamanho=44, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        # Botões laterais ajustados para não sair da tela
        botoes = [
            {
                "texto": "🎵 Músicas",
                "x": 40, "y": 140, "largura": 200, "altura": 60,
                "cor": Cores.azul_royal(),
                "cor_hover": Cores.azul_marinho(),
                "cor_texto": Cores.branco(),
                "fonte": Fontes.consolas(),
                "tamanho_fonte": 20,
                "funcao": lambda: self.navegador.ir_para("musicas"),
                "som": Efeitos.clique()
            },
            {
                "texto": "⚙️ Configurações",
                "x": 40, "y": 220, "largura": 200, "altura": 60,
                "cor": Cores.verde(),
                "cor_hover": Cores.verde_escuro(),
                "cor_texto": Cores.preto(),
                "fonte": Fontes.consolas(),
                "tamanho_fonte": 20,
                "funcao": lambda: self.navegador.ir_para("configurações"),
                "som": Efeitos.clique()
            },
            {
                "texto": "👤 Cadastro/Login",
                "x": 40, "y": 300, "largura": 200, "altura": 60,
                "cor": Cores.laranja(),
                "cor_hover": Cores.laranja_escuro(),
                "cor_texto": Cores.preto(),
                "fonte": Fontes.consolas(),
                "tamanho_fonte": 20,
                "funcao": lambda: self.navegador.ir_para("cadastro"),
                "som": Efeitos.clique()
            },
            {
                "texto": "🏆 Ranking Global",
                "x": 40, "y": 380, "largura": 200, "altura": 60,
                "cor": Cores.amarelo_ouro(),
                "cor_hover": Cores.ocre(),
                "cor_texto": Cores.preto(),
                "fonte": Fontes.consolas(),
                "tamanho_fonte": 20,
                "funcao": lambda: self.navegador.ir_para("ranking global"),
                "som": Efeitos.clique()
            },
            {
                "texto": "⏻ Sair",
                "x": 40, "y": 460, "largura": 200, "altura": 60,
                "cor": Cores.vermelho_vinho(),
                "cor_hover": Cores.vermelho_escuro(),
                "cor_texto": Cores.branco(),
                "fonte": Fontes.consolas(),
                "tamanho_fonte": 20,
                "funcao": self.sair,
                "som": Efeitos.clique()
            }
        ]

        for btn in botoes:
            botao = Botao(
                x=btn["x"], y=btn["y"], largura=btn["largura"], altura=btn["altura"],
                texto=btn["texto"],
                cor_fundo=btn["cor"],
                cor_hover=btn["cor_hover"],
                cor_texto=btn["cor_texto"],
                tamanho_fonte=btn["tamanho_fonte"],
                funcao=btn["funcao"],
                fonte=btn["fonte"],
                raio_borda=14,
                som=Efeitos.clique(),
                volume=self.navegador.volume_efeito
            )
            self.adicionar_componente(botao)

        # ScrollArea central para jogos disponíveis
        self.scroll_area_jogos = ScrollArea(
            x=270, y=140, largura=580, altura=420,
            altura_conteudo=420,  # será ajustado conforme a quantidade de jogos
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.menta()
        )

        # Exemplo de jogos disponíveis (substitua pelos seus jogos reais)
        jogos_disponiveis = [
            {"nome": "Pong Vintage", "acao": lambda: self.navegador.ir_para("menu pong-pong")},
            {"nome": "Jogo da Velha Vintage", "acao": lambda: self.navegador.ir_para("menu jogo-da-velha")},
            {"nome": "Dino", "acao": lambda: self.navegador.ir_para("menu dino")},
            {"nome": "Tetris", "acao": lambda: self.navegador.ir_para("menu tetris")},
            {"nome": "Flappy Bird", "acao": lambda: self.navegador.ir_para("menu flappy")},
            {"nome": "Snake", "acao": lambda: self.navegador.ir_para("menu snake")},
            # Adicione mais jogos conforme necessário
        ]

        for i, jogo in enumerate(jogos_disponiveis):
            btn_jogo = Botao(
                x=20, y=i*70, largura=540, altura=60,
                texto=f"▶ {jogo['nome']}",
                cor_fundo=Cores.preto(),
                cor_hover=Cores.ciano(),
                cor_texto=Cores.amarelo_ouro(),
                tamanho_fonte=28,
                funcao=jogo["acao"],
                fonte=Fontes.consolas(),
                raio_borda=16
            )
            self.scroll_area_jogos.adicionar_componente(btn_jogo)
        self.scroll_area_jogos.altura_conteudo = max(420, len(jogos_disponiveis)*70)
        self.adicionar_componente(self.scroll_area_jogos)

        # Exibe o nome do usuário logado no canto superior direito, com destaque e sombra (ajustado)
        if navegador.apelido_logado:
            nome_exibicao = f"{navegador.apelido_logado} (ID: {navegador.id_logado})"
        else:
            nome_exibicao = "visitante"

        self.adicionar_componente(
            TextoFormatado(
                x=802, y=37, texto=nome_exibicao,
                tamanho=18, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=800, y=35, texto=nome_exibicao,
                tamanho=18, cor_texto=Cores.menta(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        # Rodapé retrô, centralizado, com sombra (ajustado)
        self.adicionar_componente(
            TextoFormatado(
                x=452, y=672, texto="Bem-vindo ao sistema de jogos retrô!",
                tamanho=18, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=450, y=670, texto="Bem-vindo ao sistema de jogos retrô!",
                tamanho=18, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

    # Não há necessidade de sobrescrever o método rodar(), pois já está implementado na classe Tela.
