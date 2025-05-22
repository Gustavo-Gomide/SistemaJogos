from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, ScrollArea, Fontes
from utilitarios.musicas import fundos, efeitos, Musicas
from utilitarios.imagens import Imagem

class TelaMusicas(Tela):
    """
    Tela visual para testar músicas de fundo e efeitos sonoros do projeto.

    Recursos:
    ---------
    - Alterna entre abas "Fundos" e "Efeitos".
    - Lista rolável de botões para tocar cada música/efeito.
    - Botões de controle: Play, Pausar, Parar.
    - Imagem de fundo e imagens nos botões para visual mais agradável.

    Como usar:
    ----------
    Basta registrar a classe no navegador:
        navegador.registrar_tela("musicas", TelaMusicas)
    """

    def __init__(self, navegador=None):
        super().__init__(
            largura=900, altura=650, titulo="Testar Músicas",
            cor_fundo=Cores.preto(), navegador=navegador,
            imagem_fundo='love'  # Nome da imagem do dicionário de imagens
        )

        self.navegador = navegador
        self.pagina = 'fundos'  # 'fundos' ou 'efeitos'

        # Área rolável para botões de músicas/efeitos
        self.scroll_area = ScrollArea(
            x=120, y=140, largura=460, altura=260,
            altura_conteudo=1000,
            cor_fundo=Cores.cinza_escuro(),
            cor_barra=Cores.menta()
        )

        self.atualizar_componentes()

    def atualizar_componentes(self):
        """Atualiza todos os componentes da tela conforme a aba selecionada."""
        self.componentes = []

        # Botão voltar ao menu (retrô)
        self.adicionar_componente(
            Botao(
                x=20, y=20, largura=160, altura=38, texto='Voltar ao Menu',
                cor_fundo=Cores.vermelho(), cor_hover=Cores.vermelho_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("menu") if self.navegador else self.sair,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=12,
                imagem='geminiai'
            )
        )

        # Título retrô com sombra
        self.adicionar_componente(
            TextoFormatado(
                x=352, y=42, texto='TESTAR MÚSICAS',
                tamanho=34, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=40, texto='TESTAR MÚSICAS',
                tamanho=34, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        # Botões de abas (retrô)
        self.adicionar_componente(
            Botao(
                x=180, y=90, largura=140, altura=38, texto='Fundos',
                cor_fundo=Cores.azul() if self.pagina == 'fundos' else Cores.cinza(),
                cor_hover=Cores.azul_marinho(),
                cor_texto=Cores.branco(), funcao=lambda: self.mudar_pagina('fundos'),
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=10,
                imagem='geminiai'
            )
        )
        self.adicionar_componente(
            Botao(
                x=380, y=90, largura=140, altura=38, texto='Efeitos',
                cor_fundo=Cores.azul() if self.pagina == 'efeitos' else Cores.cinza(),
                cor_hover=Cores.azul_marinho(),
                cor_texto=Cores.branco(), funcao=lambda: self.mudar_pagina('efeitos'),
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=10,
                imagem='geminiai'
            )
        )

        # Prepara a área rolável de botões
        self.scroll_area.componentes = []
        if self.pagina == 'fundos':
            for i, (nome, caminho) in enumerate(fundos.items()):
                btn = Botao(
                    x=0, y=i*55, largura=440, altura=40,
                    texto=f"Tocar: {nome.capitalize()}",
                    cor_fundo=Cores.verde(),
                    cor_hover=Cores.verde_escuro(),
                    cor_texto=Cores.preto(),
                    funcao=lambda n=nome: Musicas.tocar_fundo(n, volume=self.navegador.volume_fundo),
                    fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                    imagem='geminiai'
                )
                self.scroll_area.adicionar_componente(btn)
            self.scroll_area.altura_conteudo = max(260, len(fundos)*55)
        else:
            for i, (nome, caminho) in enumerate(efeitos.items()):
                btn = Botao(
                    x=0, y=i*45, largura=440, altura=35,
                    texto=f"Tocar: {nome.capitalize()}",
                    cor_fundo=Cores.laranja(),
                    cor_hover=Cores.laranja_escuro(),
                    cor_texto=Cores.preto(),
                    funcao=lambda n=nome: Musicas.tocar_efeito(n, volume=self.navegador.volume_efeito),
                    fonte=Fontes.consolas(), tamanho_fonte=18, raio_borda=10,
                    imagem='geminiai'
                )
                self.scroll_area.adicionar_componente(btn)
            self.scroll_area.altura_conteudo = max(260, len(efeitos)*45)
        self.adicionar_componente(self.scroll_area)

        # Botões de controle de música de fundo (retrô)
        self.adicionar_componente(
            Botao(
                x=140, y=430, largura=120, altura=40, texto='Play',
                cor_fundo=Cores.menta(), cor_hover=Cores.verde(),
                cor_texto=Cores.preto(),
                funcao=Musicas.retomar_fundo, fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem='geminiai'
            )
        )
        self.adicionar_componente(
            Botao(
                x=290, y=430, largura=120, altura=40, texto='Pausar',
                cor_fundo=Cores.azul_royal(), cor_hover=Cores.azul_marinho(),
                cor_texto=Cores.branco(),
                funcao=Musicas.pausar_fundo, fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem='geminiai'
            )
        )
        self.adicionar_componente(
            Botao(
                x=440, y=430, largura=120, altura=40, texto='Parar',
                cor_fundo=Cores.vermelho(), cor_hover=Cores.vermelho_escuro(),
                cor_texto=Cores.branco(),
                funcao=Musicas.parar_fundo, fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem='geminiai'
            )
        )

    def mudar_pagina(self, nome):
        """Alterna entre as abas 'fundos' e 'efeitos'."""
        self.pagina = nome
        self.atualizar_componentes()

# Para rodar isolado:
if __name__ == "__main__":
    TelaMusicas().rodar()