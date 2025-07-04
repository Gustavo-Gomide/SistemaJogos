from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
from databases.tetris_database import TetrisDB

class TelaHistoricoTetris(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=600, altura=800, titulo="Histórico Tetris",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=300, y=40, texto="HISTÓRICO TETRIS", tamanho=38, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.scroll_area = ScrollArea(
            x=80, y=100, largura=440, altura=500,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu tetris"),
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))
        self.carregar_historico()

    def carregar_historico(self):
        self.scroll_area.componentes = []
        historico = TetrisDB.historico() or []
        for i, partida in enumerate(historico, start=1):
            apelido = partida[1]
            pontos = partida[2]
            linhas = partida[3]
            data = str(partida[4])[:19]
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=10, y=(i-1)*40, texto=f"{data}", tamanho=20, cor_texto=Cores.cinza(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=180, y=(i-1)*40, texto=f"{apelido}", tamanho=20, cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=320, y=(i-1)*40, texto=f"{pontos}", tamanho=20, cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=420, y=(i-1)*40, texto=f"{linhas} linhas", tamanho=20, cor_texto=Cores.laranja(), fonte_nome=Fontes.consolas()
            ))