from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Fundos, Musicas

class TelaMenuFlappy(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=400, altura=600, titulo="Menu Flappy",
            cor_fundo=Cores.azul_claro(), navegador=navegador
        )
        self.fundo = Fundos.flappy()
        
        # Salva a música anterior (do menu principal)
        Musicas.salvar_musica_anterior()

        # Toca a música do PongPong só se não estiver tocando
        if Musicas.musica_atual() != self.fundo:
            Musicas.tocar_fundo(self.fundo, self.navegador.volume_fundo)

        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=200, y=90, texto="FLAPPY BIRD", tamanho=44, cor_texto=Cores.cinza_escuro(),
            centralizado=True
        ))
        self.adicionar_componente(Botao(
            x=100, y=140, largura=200, altura=60, texto="▶ Jogar",
            cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("jogo flappy"),
            tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=100, y=220, largura=200, altura=60, texto="🏆 Ranking",
            cor_fundo=Cores.amarelo_ouro(), cor_hover=Cores.ocre(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("ranking flappy"),
            tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=100, y=300, largura=200, altura=60, texto="📜 Histórico",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("historico flappy"),
            tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.voltar_para_menu(),
            tamanho_fonte=20, raio_borda=10
        ))