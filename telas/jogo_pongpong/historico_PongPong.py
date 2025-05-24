from utilitarios.Aprincipal_widgets import Tela, TextoFormatado, Cores, Fontes, Botao, ScrollArea
from databases.PongPong_database import PongPongDB

class TelaHistoricoPongPong(Tela):
    """
    Tela de histórico de partidas do PongPong, com paginação de 5 por página.
    Mostra todas as partidas, dos mais novos para os mais antigos.
    """
    def __init__(self, navegador=None):
        super().__init__(
            largura=900, altura=650, titulo="Histórico PongPong",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.pagina = 0  # Página atual

        self.adicionar_componente(Botao(
            x=20, y=20, largura=100, altura=40, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu pong-pong") if self.navegador else None,
            fonte=Fontes.consolas(), tamanho_fonte=24, raio_borda=12
            )
        )

        # Título
        self.adicionar_componente(TextoFormatado(
            x=450, y=50, texto="HISTÓRICO DE PARTIDAS",
            tamanho=44, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Cabeçalho
        self.adicionar_componente(TextoFormatado(
            x=450, y=120, texto=" Data/Hora     Jogador 1     Jogador 2     Vencedor",
            tamanho=28, cor_texto=Cores.branco(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Área de rolagem para as partidas
        self.scroll_area = ScrollArea(
            x=30, y=160, largura=850, altura=340,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)

        self.carregar_historico()

    def carregar_historico(self):
        self.scroll_area.componentes = []

        # Busca todas as partidas do banco
        partidas = PongPongDB.todas_partidas()
        if partidas is None:
            partidas = []

        partidas_pagina = partidas

        if not partidas_pagina:
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=20, y=40, texto="Nenhuma partida encontrada.",
                tamanho=28, cor_texto=Cores.cinza(), fonte_nome=Fontes.consolas()
            ))
            return

        espacamento = 8
        altura_linha = 36

        print(partidas)

        for i, partida in enumerate(partidas_pagina):
            data = str(partida[9])[:19]
            jogador1 = partida[2] or "Visitante 1"
            jogador2 = partida[4] or "Visitante 2"
            vencedor = partida[7]
            y_linha = (i) * (altura_linha + espacamento)
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=0, y=y_linha, texto=f"{data}", tamanho=24, cor_texto=Cores.amarelo(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=270, y=y_linha, texto=f"{jogador1}", tamanho=24, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=480, y=y_linha, texto=f"{jogador2}", tamanho=24, cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=680, y=y_linha, texto=f"{vencedor}", tamanho=24, cor_texto=Cores.amarelo_ouro(), fonte_nome=Fontes.consolas()
            ))