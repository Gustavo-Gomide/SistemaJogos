from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes

class TelaMenuSnake(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=600, altura=400, titulo="Menu Snake",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=300, y=60, texto="SNAKE", tamanho=44, cor_texto=Cores.verde(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.adicionar_componente(Botao(
            x=200, y=140, largura=200, altura=60, texto="▶ Jogar",
            cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("jogo snake"),
            fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=200, y=220, largura=200, altura=60, texto="🏆 Ranking",
            cor_fundo=Cores.amarelo_ouro(), cor_hover=Cores.ocre(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("ranking snake"),
            fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=200, y=300, largura=200, altura=60, texto="📜 Histórico",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("historico snake"),
            fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu"),
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))