from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Slider, Fontes
from utilitarios.musicas import Musicas

class TelaConfiguracoes(Tela):
    """
    Tela de configurações globais de volume para músicas, efeitos e fundos.
    O usuário pode ajustar o volume e testar o som em cada categoria.
    """

    def __init__(self, navegador):
        super().__init__(
            largura=700,
            altura=500,
            titulo="Configurações de Volume",
            cor_fundo=Cores.preto(),
            navegador=navegador
        )
        self.navegador = navegador

        # Título retrô com sombra dupla e fonte pixelada
        self.adicionar_componente(TextoFormatado(
            x=352, y=62, texto="CONFIGURAÇÕES DE VOLUME",
            tamanho=40, cor_texto=Cores.cinza_escuro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))
        self.adicionar_componente(TextoFormatado(
            x=350, y=60, texto="CONFIGURAÇÕES DE VOLUME",
            tamanho=40, cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(), centralizado=True
        ))

        # Efeitos
        self.adicionar_componente(TextoFormatado(
            x=100, y=150, texto="Efeitos:",
            tamanho=26, cor_texto=Cores.laranja(),
            fonte_nome=Fontes.consolas(), centralizado=False
        ))
        self.slider_efeito = Slider(
            x=210, y=140, largura=300, valor_inicial=navegador.volume_efeito,
            cor_barra=Cores.laranja(), cor_cursor=Cores.verde(), altura=14, raio_cursor=16
        )
        self.adicionar_componente(self.slider_efeito)
        self.adicionar_componente(
            Botao(
                x=530, y=140, largura=130, altura=40, texto="Testar",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(), fonte=Fontes.consolas(), tamanho_fonte=22,
                funcao=self.testar_efeito, raio_borda=14
            )
        )

        # Fundos
        self.adicionar_componente(TextoFormatado(
            x=100, y=250, texto="Fundos:",
            tamanho=26, cor_texto=Cores.azul_royal(),
            fonte_nome=Fontes.consolas(), centralizado=False
        ))
        self.slider_fundo = Slider(
            x=210, y=240, largura=300, valor_inicial=navegador.volume_fundo,
            cor_barra=Cores.azul(), cor_cursor=Cores.menta(), altura=14, raio_cursor=16
        )
        self.adicionar_componente(self.slider_fundo)
        self.adicionar_componente(
            Botao(
                x=530, y=240, largura=130, altura=40, texto="Testar",
                cor_fundo=Cores.azul_royal(), cor_hover=Cores.azul_marinho(),
                cor_texto=Cores.branco(), fonte=Fontes.consolas(), tamanho_fonte=22,
                funcao=self.testar_fundo, raio_borda=14
            )
        )

        # Moldura/linha retrô separando áreas
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=320, texto="─" * 40,
                tamanho=18, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        # Botão para voltar ao menu (centralizado embaixo, estilo arcade)
        self.adicionar_componente(
            Botao(
                x=270, y=370, largura=200, altura=48, texto='Voltar ao Menu',
                cor_fundo=Cores.verde(), cor_hover=Cores.verde_escuro(),
                cor_texto=Cores.preto(), fonte=Fontes.consolas(), tamanho_fonte=24,
                funcao=lambda: self.navegador.ir_para("menu"), raio_borda=16
            )
        )

        # Rodapé retrô com sombra
        self.adicionar_componente(
            TextoFormatado(
                x=352, y=482, texto="Ajuste o volume global dos sons do sistema.",
                tamanho=18, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=480, texto="Ajuste o volume global dos sons do sistema.",
                tamanho=18, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

    def testar_efeito(self):
        """Toca um efeito de teste no volume selecionado."""
        Musicas.tocar_efeito("coins", volume=self.navegador.volume_efeito)

    def testar_fundo(self):
        """Toca uma música de fundo de teste no volume selecionado."""
        Musicas.tocar_fundo("jogo", volume=self.navegador.volume_fundo)

    def atualizar(self):
        """Atualiza os volumes globais do navegador conforme os sliders."""
        self.navegador.volume_efeito = self.slider_efeito.valor
        self.navegador.volume_fundo = self.slider_fundo.valor