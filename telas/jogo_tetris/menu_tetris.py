from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Fundos, Musicas

class TelaMenuTetris(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=600, altura=800, titulo="Menu Tetris",
            cor_fundo=Cores.preto(), navegador=navegador, 
        )
        self.navegador = navegador

        # Salva a música anterior (do menu principal)
        Musicas.salvar_musica_anterior()


        # Toca a música do PongPong só se não estiver tocando
        if Musicas.musica_atual() != Fundos.tetris():
            Musicas.tocar_fundo(Fundos.tetris(), self.navegador.volume_fundo)

        self.adicionar_componente(TextoFormatado(
            x=300, y=60, texto="MENU TETRIS", tamanho=44, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.adicionar_componente(Botao(
            x=200, y=200, largura=200, altura=60, texto="▶ Jogar",
            cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("jogo tetris"),
            fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=200, y=300, largura=200, altura=60, texto="🏆 Ranking",
            cor_fundo=Cores.amarelo_ouro(), cor_hover=Cores.ocre(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("ranking tetris"),
            fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=200, y=400, largura=200, altura=60, texto="📜 Histórico",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("historico tetris"),
            fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=self.voltar_para_menu,
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))