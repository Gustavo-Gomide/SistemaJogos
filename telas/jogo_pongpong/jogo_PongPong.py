from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, Retangulo, Circulo
from utilitarios.imagens import carregar_imagem
from utilitarios.musicas import Musicas  # Adicione este import
from databases.PongPong_database import PongPongDB
import pygame
import time

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

    # Efeitos sonoros e música
    efeito_gol = 'fim'         # Nome do efeito para gol
    efeito_parede = 'correto'  # Nome do efeito para parede
    efeito_raquete = 'coins'   # Nome do efeito para raquete
    musica_fundo = 'jogo'      # Nome da música de fundo

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
                funcao=lambda: (Musicas.parar_fundo(), self.navegador.ir_para("menu pong-pong")) if self.navegador else self.sair,
                fonte=Fontes.consolas(), tamanho_fonte=22, raio_borda=12
            )
        )

        self.atualizar_fundo()
        self.resetar_jogo()
        # Use o volume global do navegador, se existir, senão 0.4
        Musicas.tocar_fundo(
            self.musica_fundo,
            volume=getattr(self.navegador, "volume_fundo", 0.4)
        )

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
        self.tempo_inicio = time.time()

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
            Musicas.tocar_efeito(
                self.efeito_parede,
                volume=getattr(self.navegador, "volume_efeito", 0.6)
            )

        # Colisão com raquetes
        if (self.ball.x - self.ball.raio <= self.paddle1.x + self.paddle1.largura and
            self.paddle1.y < self.ball.y < self.paddle1.y + self.paddle1.altura):
            self.ball.dx = abs(self.ball.dx)
            self.ball.x = self.paddle1.x + self.paddle1.largura + self.ball.raio
            Musicas.tocar_efeito(
                self.efeito_raquete,
                volume=getattr(self.navegador, "volume_efeito", 0.7)
            )

        if (self.ball.x + self.ball.raio >= self.paddle2.x and
            self.paddle2.y < self.ball.y < self.paddle2.y + self.paddle2.altura):
            self.ball.dx = -abs(self.ball.dx)
            self.ball.x = self.paddle2.x - self.ball.raio
            Musicas.tocar_efeito(
                self.efeito_raquete,
                volume=getattr(self.navegador, "volume_efeito", 0.7)
            )

        # Pontuação
        if self.ball.x < 0:
            self.score2 += 1
            self.ball.x = self.largura // 2
            self.ball.y = self.altura // 2
            v = self.velocidade_bola
            self.ball.set_direcao(v, v)
            Musicas.tocar_efeito(
                self.efeito_gol,
                volume=getattr(self.navegador, "volume_efeito", 0.8)
            )
        if self.ball.x > self.largura:
            self.score1 += 1
            self.ball.x = self.largura // 2
            self.ball.y = self.altura // 2
            v = self.velocidade_bola
            self.ball.set_direcao(-v, v)
            Musicas.tocar_efeito(
                self.efeito_gol,
                volume=getattr(self.navegador, "volume_efeito", 0.8)
            )

        # Lógica de vitória (quem faz 5 pontos)
        if self.score1 >= 5 or self.score2 >= 5:
            vencedor = self.navegador.apelido_logado if self.score1 >= 5 else self.navegador.jgd_2
            self.mostrar_vencedor(vencedor)

    def mostrar_vencedor(self, vencedor):
        import time
        tempo_jogado = int(time.time() - getattr(self, "tempo_inicio", time.time()))

        # Jogador 1 (esquerda)
        if self.navegador.id_logado:
            PongPongDB.registrar_partida(
                id_usuario=self.navegador.id_logado,
                apelido=self.navegador.apelido_logado,
                pontuacao=self.score1,
                venceu=(vencedor == self.navegador.apelido_logado),
                tempo_jogado=tempo_jogado
            )
        # Jogador 2 (direita)
        if self.navegador.jgd_2_id:
            PongPongDB.registrar_partida(
                id_usuario=self.navegador.jgd_2_id,
                apelido=self.navegador.jgd_2,
                pontuacao=self.score2,
                venceu=(vencedor == self.navegador.jgd_2),
                tempo_jogado=tempo_jogado
            )

        rodando = True
        clock = pygame.time.Clock()
        fonte = pygame.font.SysFont("consolas", 44, bold=True)
        fonte_btn = pygame.font.SysFont("consolas", 28, bold=True)
        texto = f"{vencedor} venceu!"
        texto_render = fonte.render(texto, True, Cores.amarelo_ouro())

        # Botões
        btn_jogar = pygame.Rect(self.largura // 2 - 180, self.altura // 2 + 40, 160, 50)
        btn_menu = pygame.Rect(self.largura // 2 + 20, self.altura // 2 + 40, 160, 50)

        while rodando:
            self.tela.fill(Cores.preto())
            # Fundo opcional
            if TelaJogoPongPong.fundo_surface:
                self.tela.blit(TelaJogoPongPong.fundo_surface, (0, 0))
            # Mensagem
            self.tela.blit(texto_render, (self.largura // 2 - texto_render.get_width() // 2, self.altura // 2 - 60))

            # Botão Jogar Novamente
            pygame.draw.rect(self.tela, Cores.verde(), btn_jogar, border_radius=10)
            txt_jogar = fonte_btn.render("Jogar Novamente", True, Cores.preto())
            self.tela.blit(txt_jogar, (btn_jogar.x + (btn_jogar.width - txt_jogar.get_width()) // 2, btn_jogar.y + 10))

            # Botão Voltar ao Menu
            pygame.draw.rect(self.tela, Cores.azul(), btn_menu, border_radius=10)
            txt_menu = fonte_btn.render("Voltar ao Menu", True, Cores.branco())
            self.tela.blit(txt_menu, (btn_menu.x + (btn_menu.width - txt_menu.get_width()) // 2, btn_menu.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_jogar.collidepoint(event.pos):
                        self.resetar_jogo()
                        return  # Sai do método e volta ao jogo
                    if btn_menu.collidepoint(event.pos):
                        self.navegador.ir_para("menu pong-pong")
                        return
            clock.tick(30)

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

        # Nome dos jogadores ao lado do placar, com sombra para contraste
        nome1 = self.navegador.apelido_logado or "Visitante 1"
        nome2 = self.navegador.jgd_2 or "Visitante 2"
        fonte_nome = pygame.font.SysFont("consolas", 22, bold=True)
        # Sombra
        nome1_sombra = fonte_nome.render(nome1, True, Cores.preto())
        nome2_sombra = fonte_nome.render(nome2, True, Cores.preto())
        tela.blit(nome1_sombra, (self.largura // 4 - nome1_sombra.get_width() // 2 + 2, 60 + 2))
        tela.blit(nome2_sombra, (3 * self.largura // 4 - nome2_sombra.get_width() // 2 + 2, 60 + 2))
        # Nome
        nome1_render = fonte_nome.render(nome1, True, Cores.verde())
        nome2_render = fonte_nome.render(nome2, True, Cores.azul())
        tela.blit(nome1_render, (self.largura // 4 - nome1_render.get_width() // 2, 60))
        tela.blit(nome2_render, (3 * self.largura // 4 - nome2_render.get_width() // 2, 60))

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