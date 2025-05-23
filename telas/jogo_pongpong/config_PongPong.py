from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, ScrollArea
from utilitarios.imagens import imagens
import pygame
from telas.jogo_pongpong.jogo_PongPong import TelaJogoPongPong

class TelaConfigPongPong(Tela):
    """
    Tela de configurações globais do PongPong.
    Permite ajustar: cor/imagem das raquetes, bola, fundo e velocidade da bola.
    """

    def __init__(self, navegador=None, editar=None):
        super().__init__(
            largura=700, altura=600, titulo="Configurações PongPong",
            cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.editar = editar

        # Título
        self.adicionar_componente(
            TextoFormatado(
                x=352, y=52, texto="CONFIGURAÇÕES",
                tamanho=38, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=50, texto="CONFIGURAÇÕES",
                tamanho=38, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        if self.editar is None:
            self.tela_principal()
        else:
            self.tela_edicao(self.editar)

    def tela_principal(self):
        self.velocidade = TelaJogoPongPong.velocidade_bola
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=140, texto=f"Velocidade da Bola: {self.velocidade}",
                tamanho=26, cor_texto=Cores.branco(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            Botao(
                x=220, y=180, largura=60, altura=40, texto="-",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.branco(),
                funcao=self.diminuir_velocidade,
                fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=10
            )
        )
        self.adicionar_componente(
            Botao(
                x=420, y=180, largura=60, altura=40, texto="+",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.branco(),
                funcao=self.aumentar_velocidade,
                fonte=Fontes.consolas(), tamanho_fonte=28, raio_borda=10
            )
        )

        # Raquete Esquerda
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=260, texto="Raquete Esquerda",
                tamanho=22, cor_texto=Cores.verde(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            Botao(
                x=220, y=290, largura=120, altura=40,
                texto="Ativa",
                cor_fundo=TelaJogoPongPong.paddle1_cor,
                cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.preto(),
                funcao=None,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem=TelaJogoPongPong.paddle1_imagem
            )
        )
        self.adicionar_componente(
            Botao(
                x=360, y=290, largura=120, altura=40, texto="Editar",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong", "paddle1"),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )

        # Raquete Direita
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=350, texto="Raquete Direita",
                tamanho=22, cor_texto=Cores.vermelho(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            Botao(
                x=220, y=380, largura=120, altura=40,
                texto="Ativa",
                cor_fundo=TelaJogoPongPong.paddle2_cor,
                cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.preto(),
                funcao=None,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem=TelaJogoPongPong.paddle2_imagem
            )
        )
        self.adicionar_componente(
            Botao(
                x=360, y=380, largura=120, altura=40, texto="Editar",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong", "paddle2"),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )

        # Bola
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=440, texto="Bola",
                tamanho=22, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            Botao(
                x=220, y=470, largura=120, altura=40,
                texto="Ativa",
                cor_fundo=TelaJogoPongPong.bola_cor,
                cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.preto(),
                funcao=None,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem=TelaJogoPongPong.bola_imagem
            )
        )
        self.adicionar_componente(
            Botao(
                x=360, y=470, largura=120, altura=40, texto="Editar",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong", "bola"),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )

        # Fundo
        self.adicionar_componente(
            TextoFormatado(
                x=350, y=530, texto="Fundo",
                tamanho=22, cor_texto=Cores.cinza(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            Botao(
                x=220, y=560, largura=120, altura=40,
                texto="Ativo",
                cor_fundo=TelaJogoPongPong.fundo_cor,
                cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.preto(),
                funcao=None,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                imagem=TelaJogoPongPong.fundo_imagem
            )
        )
        self.adicionar_componente(
            Botao(
                x=360, y=560, largura=120, altura=40, texto="Editar",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong", "fundo"),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )

        # Botão para voltar ao menu PongPong
        self.adicionar_componente(
            Botao(
                x=20, y=20, largura=120, altura=38, texto="Voltar",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("menu pong-pong") if self.navegador else self.sair,
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )

    def tela_edicao(self, editar):
        # Abas: Cores e Imagens
        self.adicionar_componente(
            Botao(
                x=180, y=80, largura=160, altura=40, texto="Cores",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong", (editar, "cores")),
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=10
            )
        )
        self.adicionar_componente(
            Botao(
                x=360, y=80, largura=160, altura=40, texto="Imagens",
                cor_fundo=Cores.laranja(), cor_hover=Cores.laranja_escuro(),
                cor_texto=Cores.preto(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong", (editar, "imagens")),
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=10
            )
        )

        # Scroll com opções
        if isinstance(editar, tuple) and editar[1] == "cores":
            scroll = ScrollArea(
                x=120, y=150, largura=460, altura=350, altura_conteudo=0,
                cor_fundo=Cores.cinza_escuro(),
                cor_barra=Cores.cinza()
            )
            for nome in dir(Cores):
                if not nome.startswith("_") and callable(getattr(Cores, nome)):
                    cor = getattr(Cores, nome)()
                    btn = Botao(
                        x=10, y=len(scroll.componentes)*50, largura=440, altura=40,
                        texto=nome.capitalize(),
                        cor_fundo=cor, cor_hover=Cores.cinza(),
                        cor_texto=Cores.preto() if sum(cor) > 400 else Cores.branco(),
                        funcao=lambda c=cor: self.set_cor(editar[0], c, is_cor=True),
                        fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
                    )
                    scroll.adicionar_componente(btn)
            scroll.altura_conteudo = max(350, len(scroll.componentes)*50)
            self.adicionar_componente(scroll)
        elif isinstance(editar, tuple) and editar[1] == "imagens":
            scroll = ScrollArea(
                x=120, y=150, largura=460, altura=350, altura_conteudo=0,
                cor_fundo=Cores.cinza_escuro(), cor_barra=Cores.cinza()
            )
            alvo = editar[0]
            for i, nome in enumerate(imagens.keys()):
                btn = Botao(
                    x=10, y=i*90, largura=440, altura=80,
                    texto=nome,
                    cor_fundo=Cores.cinza(),
                    cor_hover=Cores.cinza_escuro(),
                    cor_texto=Cores.branco(),
                    funcao=lambda n=nome: self.set_cor(alvo, n, is_cor=False),
                    fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10,
                    imagem=nome
                )
                scroll.adicionar_componente(btn)
            scroll.altura_conteudo = max(350, len(imagens)*90)
            self.adicionar_componente(scroll)

        # Botão para voltar à tela principal de configurações
        self.adicionar_componente(
            Botao(
                x=20, y=20, largura=120, altura=38, texto="Voltar",
                cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("configurações pong-pong"),
                fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
            )
        )

    def diminuir_velocidade(self):
        if TelaJogoPongPong.velocidade_bola > 1:
            TelaJogoPongPong.velocidade_bola -= 1
        self.navegador.ir_para("configurações pong-pong")

    def aumentar_velocidade(self):
        TelaJogoPongPong.velocidade_bola += 1
        self.navegador.ir_para("configurações pong-pong")

    def set_cor(self, alvo, valor, is_cor=True):
        # Atualiza cor ou imagem separadamente
        if alvo == "paddle1":
            if is_cor:
                TelaJogoPongPong.paddle1_cor = valor
                TelaJogoPongPong.paddle1_imagem = None  # limpa imagem
            else:
                TelaJogoPongPong.paddle1_imagem = valor
        elif alvo == "paddle2":
            if is_cor:
                TelaJogoPongPong.paddle2_cor = valor
                TelaJogoPongPong.paddle2_imagem = None
            else:
                TelaJogoPongPong.paddle2_imagem = valor
        elif alvo == "bola":
            if is_cor:
                TelaJogoPongPong.bola_cor = valor
                TelaJogoPongPong.bola_imagem = None
            else:
                TelaJogoPongPong.bola_imagem = valor
        elif alvo == "fundo":
            if is_cor:
                TelaJogoPongPong.fundo_cor = valor
                TelaJogoPongPong.fundo_imagem = None
            else:
                TelaJogoPongPong.fundo_imagem = valor
        self.navegador.ir_para("configurações pong-pong")