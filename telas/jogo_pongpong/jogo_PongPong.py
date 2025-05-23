from calendar import c
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, Retangulo, Circulo
from utilitarios.imagens import carregar_imagem
import pygame

class TelaJogoPongPong(Tela):
    """
    Tela do jogo PongPong (Pong clássico).
    """

    # Parâmetros globais ajustáveis
    paddle1_cor = Cores.verde()
    paddle1_imagem = None
    paddle2_cor = Cores.vermelho()
    paddle2_imagem = None
    bola_cor = Cores.amarelo_ouro()
    bola_imagem = None
    fundo_cor = Cores.preto()
    fundo_imagem = None
    velocidade_bola = 1  # <--- Ajustável

    fundo_surface = None  # Surface pronto para desenhar

    def __init__(self, navegador=None):
        super().__init__(
            largura=900, altura=650, titulo="PongPong",
            cor_fundo=TelaJogoPongPong.fundo_cor, navegador=navegador,
            imagem_fundo=TelaJogoPongPong.fundo_imagem
        )
        self.navegador = navegador

        # Título retrô com sombra
        self.adicionar_componente(
            TextoFormatado(
                x=452, y=62, texto="PONGPONG",
                tamanho=44, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=450, y=60, texto="PONGPONG",
                tamanho=44, cor_texto=Cores.amarelo_ouro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )

        # Botão para voltar ao menu
        self.adicionar_componente(
            Botao(
                x=30, y=590, largura=180, altura=45, texto='Voltar ao Menu',
                cor_fundo=Cores.azul(), cor_hover=Cores.azul_escuro(),
                cor_texto=Cores.branco(),
                funcao=lambda: self.navegador.ir_para("menu pong-pong") if self.navegador else self.sair,
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=12
            )
        )

        self.atualizar_fundo()
        self.resetar_jogo()

    def resetar_jogo(self):
        self.paddle_height = 100
        self.paddle_width = 15
        self.ball_radius = 12

        self.paddle1 = Retangulo(
            0, self.altura // 2 - self.paddle_height // 2,
            self.paddle_width, self.paddle_height,
            TelaJogoPongPong.paddle1_cor, TelaJogoPongPong.paddle1_imagem
        )
        self.paddle2 = Retangulo(
            self.largura - self.paddle_width, self.altura // 2 - self.paddle_height // 2,
            self.paddle_width, self.paddle_height,
            TelaJogoPongPong.paddle2_cor, TelaJogoPongPong.paddle2_imagem
        )
        self.ball = Circulo(
            self.largura // 2, self.altura // 2, self.ball_radius,
            TelaJogoPongPong.bola_cor, TelaJogoPongPong.bola_imagem
        )

        v = self.velocidade_bola
        self.ball.set_direcao(v, v)
        self.score1 = 0
        self.score2 = 0

    def atualizar(self):
        # Movimento dos jogadores
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle1.set_dy(-7)
        elif keys[pygame.K_s]:
            self.paddle1.set_dy(7)
        else:
            self.paddle1.set_dy(0)

        if keys[pygame.K_UP]:
            self.paddle2.set_dy(-7)
        elif keys[pygame.K_DOWN]:
            self.paddle2.set_dy(7)
        else:
            self.paddle2.set_dy(0)

        # Atualiza raquetes
        self.paddle1.atualizar(0, self.altura)
        self.paddle2.atualizar(0, self.altura)
        # Atualiza bola
        self.ball.atualizar()

        # Colisão com topo/baixo
        if self.ball.y - self.ball.raio <= 0 or self.ball.y + self.ball.raio >= self.altura:
            self.ball.dy *= -1

        # Colisão com raquetes
        if (self.ball.x - self.ball.raio <= self.paddle1.x + self.paddle1.largura and
            self.paddle1.y < self.ball.y < self.paddle1.y + self.paddle1.altura):
            self.ball.dx = abs(self.ball.dx)
            self.ball.x = self.paddle1.x + self.paddle1.largura + self.ball.raio

        if (self.ball.x + self.ball.raio >= self.paddle2.x and
            self.paddle2.y < self.ball.y < self.paddle2.y + self.paddle2.altura):
            self.ball.dx = -abs(self.ball.dx)
            self.ball.x = self.paddle2.x - self.ball.raio

        # Pontuação
        if self.ball.x < 0:
            self.score2 += 1
            self.ball.x = self.largura // 2
            self.ball.y = self.altura // 2
            v = self.velocidade_bola
            self.ball.set_direcao(v, v)
        if self.ball.x > self.largura:
            self.score1 += 1
            self.ball.x = self.largura // 2
            self.ball.y = self.altura // 2
            v = self.velocidade_bola
            self.ball.set_direcao(-v, v)

    def renderizar(self):
        # Fundo: sempre desenha cor, depois imagem se existir
        if TelaJogoPongPong.fundo_cor:
            self.tela.fill(TelaJogoPongPong.fundo_cor)
        if TelaJogoPongPong.fundo_surface:
            self.tela.blit(TelaJogoPongPong.fundo_surface, (0, 0))

        for componente in self.componentes:
            if hasattr(componente, 'desenhar'):
                componente.desenhar(self.tela)

        tela = self.tela

        # Linha central branca grossa
        pygame.draw.rect(tela, Cores.branco(), (self.largura // 2 - 5, 0, 10, self.altura), border_radius=4)

        # Desenha as raquetes e a bola usando as classes
        self.paddle1.desenhar(tela)
        self.paddle2.desenhar(tela)
        self.ball.desenhar(tela)

        # Placar
        fonte = pygame.font.SysFont("consolas", 36, bold=True)
        placar1 = fonte.render(f"{self.score1}", True, Cores.verde())
        placar2 = fonte.render(f"{self.score2}", True, Cores.vermelho())
        tela.blit(placar1, (self.largura // 4 - placar1.get_width() // 2, 20))
        tela.blit(placar2, (3 * self.largura // 4 - placar2.get_width() // 2, 20))

        pygame.display.flip()

    def eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                self.resetar_jogo()
        super().eventos(eventos)

    def atualizar_fundo(self):
        if TelaJogoPongPong.fundo_imagem:
            TelaJogoPongPong.fundo_surface = carregar_imagem(
                TelaJogoPongPong.fundo_imagem, (self.largura, self.altura)
            )
        else:
            TelaJogoPongPong.fundo_surface = None