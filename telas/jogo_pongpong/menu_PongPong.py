from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes

class TelaMenuPongPong(Tela):
    """
    Tela de menu inicial do PongPong.
    Permite acessar: Jogar, Ranking, Histórico e Configurações.
    """

    def __init__(self, navegador=None):
        super().__init__(
            largura=700, altura=500, titulo="Menu PongPong",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador

        # Título centralizado com sombra
        self.adicionar_componente(
            TextoFormatado(
                x=352, y=62, texto="PONGPONG",
                tamanho=44, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=60, texto="PONGPONG",
                tamanho=44, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        # Botão Jogar
        self.adicionar_componente(
            Botao(
                x=200, y=160, largura=300, altura=60, texto="▶ Jogar",
                cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("selecao jogadores pong-pong"),
                fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
            )
        )

        # Botão Ranking
        self.adicionar_componente(
            Botao(
                x=200, y=240, largura=300, altura=60, texto="🏆 Ranking",
                cor_fundo=Cores.amarelo_ouro(), cor_hover=Cores.ocre(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("ranking pong-pong") if self.navegador else None,
                fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
            )
        )

        # Botão Histórico
        self.adicionar_componente(
            Botao(
                x=200, y=320, largura=300, altura=60, texto="📜 Histórico",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("historico pong-pong") if self.navegador else None,
                fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
            )
        )

        # Botão Configurações
        self.adicionar_componente(
            Botao(
                x=200, y=400, largura=300, altura=60, texto="⚙️ Configurações",
                cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong") if self.navegador else None,
                fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
            )
        )

        # Botão para voltar ao menu principal
        self.adicionar_componente(
            Botao(
                x=20, y=20, largura=120, altura=38, texto="Voltar",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("menu") if self.navegador else self.sair,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )