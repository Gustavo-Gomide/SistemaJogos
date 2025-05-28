from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes, Retangulo, Circulo
from utilitarios.imagens import carregar_imagem
from utilitarios.musicas import Efeitos, Musicas
from databases.PongPong_database import PongPongDB
from databases.cadastro_database import DadosUsuario
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
    fundo_cor = Cores.azul_petroleo()
    fundo_imagem = None
    velocidade_bola = 5  # <--- Ajustável
    tempo_espera_bola = 5  # segundos (ajustável)

    # Efeitos sonoros e música
    efeito_gol = 'fim'         # Nome do efeito para gol
    efeito_parede = 'correto'  # Nome do efeito para parede
    efeito_raquete = 'coins'   # Nome do efeito para raquete

    fundo_surface = None  # Surface pronto para desenhar

    def __init__(self, navegador=None):
        super().__init__(
            largura=900, altura=650, titulo="PongPong",
            cor_fundo=TelaJogoPongPong.fundo_cor, navegador=navegador,
            imagem_fundo=TelaJogoPongPong.fundo_imagem
        )
        self.navegador = navegador

        self.som_fim = Efeitos.venceu()

        # Título retrô com sombra
        self.adicionar_componente(
            TextoFormatado(
                x=452, y=62, texto="PONG  PONG",
                tamanho=44, cor_texto=Cores.cinza_escuro(),
                fonte_nome=Fontes.consolas(), centralizado=True
            )
        )
        self.adicionar_componente(
            TextoFormatado(
                x=450, y=60, texto="PONG  PONG",
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
        self.tempo_inicio = time.time()
        self.vel_bola_temp = self.velocidade_bola
        self.tempo_reinicio = time.time()

    def atualizar(self):
        # Pausa após gol ou início
        if self.vel_bola_temp != 0:
            self.velocidade_bola = 0
            if time.time() - self.tempo_reinicio >= self.tempo_espera_bola:
                self.velocidade_bola = self.vel_bola_temp
            else:
                return  # Não atualiza o jogo enquanto pausado

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
            self.vel_bola_temp = self.velocidade_bola
            self.tempo_reinicio = time.time()
            return  # Sai do método para pausar imediatamente

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
            self.vel_bola_temp = self.velocidade_bola
            self.tempo_reinicio = time.time()
            return  # Sai do método para pausar imediatamente

        # Lógica de vitória (quem faz 5 pontos)
        if self.score1 >= 2 or self.score2 >= 2:
            vencedor = self.navegador.apelido_logado if self.score1 >= 2 else self.navegador.jgd_2
            self.mostrar_vencedor(vencedor)

    def mostrar_vencedor(self, vencedor):
        Musicas.tocar_efeito(self.som_fim)
        import time
        tempo_jogado = int(time.time() - getattr(self, "tempo_inicio", time.time()))

        # Jogador 1
        if getattr(self.navegador, "id_logado", None):
            id_j1 = self.navegador.id_logado
            apelido_j1 = self.navegador.apelido_logado
            DadosUsuario.atualizar_pontuacao_jogo(apelido_j1, "pong-pong", self.score1, tempo=tempo_jogado)
        else:
            id_j1 = None
            apelido_j1 = "Visitante 1"

        # Jogador 2
        if getattr(self.navegador, "jgd_2_id", None):
            id_j2 = self.navegador.jgd_2_id
            apelido_j2 = self.navegador.jgd_2
            DadosUsuario.atualizar_pontuacao_jogo(apelido_j2, "pong-pong", self.score2, tempo=tempo_jogado)
        else:
            id_j2 = None
            apelido_j2 = "Visitante 2"

        # Registro completo da partida
        PongPongDB.registrar_partida(
            id_usuario_j1=id_j1,
            apelido_j1=apelido_j1,
            id_usuario_j2=id_j2,
            apelido_j2=apelido_j2,
            pontuacao_j1=self.score1,
            pontuacao_j2=self.score2,
            vencedor=vencedor,
            tempo_jogado=tempo_jogado
        )

        # Componentes da tela de fim de jogo
        componentes = []
        
        # Texto do vencedor
        componentes.append(TextoFormatado(
            x=self.largura//2,
            y=self.altura//2 - 60,
            texto=f"{vencedor} venceu!",
            tamanho=44,
            cor_texto=Cores.amarelo_ouro(),
            fonte_nome=Fontes.consolas(),
            centralizado=True
        ))
        
        # Botão Jogar Novamente
        componentes.append(Botao(
            x=self.largura//2 - 230,
            y=self.altura//2 + 40,
            largura=250,
            altura=50,
            texto="Jogar Novamente",
            cor_fundo=Cores.verde(),
            cor_hover=Cores.verde_escuro(),
            cor_texto=Cores.preto(),
            funcao=self.resetar_jogo,
            fonte=Fontes.consolas(),
            tamanho_fonte=28,
            raio_borda=10
        ))
        
        # Botão Voltar ao Menu
        componentes.append(Botao(
            x=self.largura//2 + 30,
            y=self.altura//2 + 40,
            largura=250,
            altura=50,
            texto="Voltar ao Menu",
            cor_fundo=Cores.azul(),
            cor_hover=Cores.azul_escuro(),
            cor_texto=Cores.branco(),
            funcao=lambda: self.navegador.ir_para("menu pong-pong"),
            fonte=Fontes.consolas(),
            tamanho_fonte=28,
            raio_borda=10
        ))

        rodando = True
        clock = pygame.time.Clock()

        while rodando:
            # Fundo
            self.tela.fill(Cores.preto())
            if TelaJogoPongPong.fundo_surface:
                self.tela.blit(TelaJogoPongPong.fundo_surface, (0, 0))
            
            # Desenha componentes
            for componente in componentes:
                componente.desenhar(self.tela)
            
            pygame.display.flip()

            # Processa eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    return
                
                # Repassa eventos para os componentes
                for componente in componentes:
                    if hasattr(componente, 'processar_evento'):
                        componente.processar_evento(evento)
                        if not rodando:  # Se algum botão foi clicado
                            break
            
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