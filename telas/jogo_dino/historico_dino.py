from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
from databases.dino_database import DinoDB

class TelaHistoricoDino(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=700, altura=400, titulo="Histórico Dino",
            cor_fundo=Cores.branco(), navegador=navegador
        )
        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=350, y=40, texto="HISTÓRICO DINO", tamanho=38, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.scroll_area = ScrollArea(
            x=120, y=100, largura=460, altura=220,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.amarelo_ouro()
        )
        self.adicionar_componente(self.scroll_area)
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu dino"),
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))
        self.carregar_historico()

    def carregar_historico(self):
        self.scroll_area.componentes = []
        historico = DinoDB.historico() or []
        # Show all games, including visitors
        for i, partida in enumerate(historico, start=1):
            id_usuario = partida[1]
            apelido = partida[2]
            pontos = partida[3]
            data = str(partida[4])[:19]
            
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=10, y=(i-1)*40, texto=f"{data}", tamanho=20,
                cor_texto=Cores.cinza(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=220, y=(i-1)*40, texto=f"{apelido}", tamanho=20,
                cor_texto=Cores.verde(), fonte_nome=Fontes.consolas()
            ))
            self.scroll_area.adicionar_componente(TextoFormatado(
                x=400, y=(i-1)*40, texto=f"{pontos}", tamanho=20,
                cor_texto=Cores.azul(), fonte_nome=Fontes.consolas()
            ))