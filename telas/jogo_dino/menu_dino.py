from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Musicas, Fundos

class TelaMenuDino(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=700, altura=400, titulo="Menu Dino",
            cor_fundo=Cores.branco(), navegador=navegador
        )

        self.fundo = Fundos.jogo()
        
        # Salva a música anterior (do menu principal)
        Musicas.salvar_musica_anterior()

        # Toca a música do PongPong só se não estiver tocando
        if Musicas.musica_atual() != self.fundo:
            Musicas.tocar_fundo(self.fundo, self.navegador.volume_fundo)

        self.navegador = navegador
        self.adicionar_componente(TextoFormatado(
            x=350, y=60, texto="DINO", tamanho=44, cor_texto=Cores.cinza_escuro(),
            centralizado=True
        ))
        self.adicionar_componente(Botao(
            x=250, y=140, largura=200, altura=60, texto="▶ Jogar",
            cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("jogo dino"),
            tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=250, y=220, largura=200, altura=60, texto="🏆 Ranking",
            cor_fundo=Cores.amarelo_ouro(), cor_hover=Cores.ocre(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("ranking dino"),
            tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=250, y=300, largura=200, altura=60, texto="📜 Histórico",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.preto(),
            funcao=lambda: self.navegador.ir_para("historico dino"),
            tamanho_fonte=28, raio_borda=16
        ))
        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.voltar_para_menu(),
            tamanho_fonte=20, raio_borda=10
        ))