import pygame
import random
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Efeitos, Musicas
from databases.flappy_database import FlappyDB
from databases.cadastro_database import DadosUsuario

class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((34, 24))
        self.image.fill((255, 255, 0))
        pygame.draw.ellipse(self.image, (200, 200, 0), (0, 0, 34, 24))
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 250
        self.vel_y = 0

    def update(self):
        self.vel_y += 0.3
        self.rect.y += self.vel_y
        if self.rect.y > 470:
            self.rect.y = 470
            self.vel_y = 0

    def pular(self):
        self.vel_y = -5

class Cano(pygame.sprite.Sprite):
    def __init__(self, x, y, invertido=False):
        super().__init__()
        self.image = pygame.Surface((52, 320))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect()
        if invertido:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.x = x
            self.rect.y = y - 320
        else:
            self.rect.x = x
            self.rect.y = y

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -52:
            self.kill()

class TelaJogoFlappy(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=400, altura=600, titulo="Flappy Bird",
            cor_fundo=Cores.azul_claro(), navegador=navegador
        )
        self.navegador = navegador
        self.passaro = Passaro()
        self.canos = pygame.sprite.Group()
        self.tudo = pygame.sprite.Group(self.passaro)
        self.pontuacao = 0
        self.rodando = True
        self.fonte = pygame.font.SysFont("consolas", 32)
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0
        self.efeito_ponto = Efeitos.correto()
        self.efeito_pulo = Efeitos.coins()
        self.efeito_gameover = Efeitos.empate()

        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=self.voltar_menu,
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))

    def voltar_menu(self):
        if self.navegador:
            self.navegador.ir_para("menu flappy")

    def rodar(self):
        while self.rodando:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.passaro.pular()
                        Musicas.tocar_efeito(Efeitos.coins())
                    if event.key == pygame.K_ESCAPE:
                        self.voltar_menu()
                        return

            # Spawn canos
            self.spawn_timer += 1
            if self.spawn_timer > 90:
                altura = random.randint(120, 400)
                cano_top = Cano(400, altura, invertido=True)
                cano_bot = Cano(400, altura + 150)
                self.canos.add(cano_top, cano_bot)
                self.tudo.add(cano_top, cano_bot)
                self.spawn_timer = 0

            self.tudo.update()

            # Colisão
            if pygame.sprite.spritecollideany(self.passaro, self.canos) or self.passaro.rect.y >= 576:
                self.game_over()
                return

            # Pontuação
            for cano in self.canos:
                if cano.rect.right < self.passaro.rect.left and not hasattr(cano, "pontuado"):
                    setattr(cano, "pontuado", True)
                    self.pontuacao += 0.5  # Cada par de canos conta 1 ponto
                    if self.pontuacao % 1 == 0:
                        Musicas.tocar_efeito(self.efeito_ponto, volume=0.7)

            self.renderizar()

    def renderizar(self):
        self.tela.fill((135, 206, 250))
        self.tudo.draw(self.tela)
        texto = self.fonte.render(f"Pontos: {int(self.pontuacao)}", True, (0, 0, 0))
        self.tela.blit(texto, (0, 20))
        pygame.display.flip()

    def game_over(self):
        Musicas.tocar_efeito(self.efeito_gameover, volume=0.8)
        apelido = getattr(self.navegador, "apelido_logado", None) or "Visitante"
        
        # Get user id if logged in
        id_usuario = None
        if apelido != "Visitante":
            usuarios = DadosUsuario.listar_usuarios()
            if usuarios:
                for u in usuarios:
                    if u[3] == apelido:  # Assuming apelido is at index 3
                        id_usuario = u[0]  # Assuming id is at index 0
                        break
        
                # Register game with id_usuario
                FlappyDB.registrar_partida(id_usuario, apelido, int(self.pontuacao))
                DadosUsuario.atualizar_pontuacao_jogo(apelido, "flappy", self.pontuacao, tempo=120)
        else:
            FlappyDB.registrar_partida(apelido=apelido, pontuacao=self.pontuacao)
    
        fonte = pygame.font.SysFont("consolas", 48)
        texto = fonte.render("Game Over!", True, (200, 0, 0))
        self.tela.blit(texto, (60, 250))
        pygame.display.flip()
        pygame.time.wait(1800)
        self.voltar_menu()