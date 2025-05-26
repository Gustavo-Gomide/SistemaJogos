import pygame
import random
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from databases.dino_database import DinoDB
from databases.cadastro_database import DadosUsuario

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((44, 47))
        self.image.fill((120, 120, 120))
        pygame.draw.rect(self.image, (60, 60, 60), (0, 0, 44, 47), 3)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 300
        self.vel_y = 0
        self.pulando = False

    def update(self):
        if self.pulando:
            self.vel_y += 1
            self.rect.y += self.vel_y
            if self.rect.y >= 300:
                self.rect.y = 300
                self.pulando = False
                self.vel_y = 0

    def pular(self):
        if not self.pulando:
            self.pulando = True
            self.vel_y = -18

class Cacto(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((34, 139, 34))
        pygame.draw.rect(self.image, (0, 100, 0), (0, 0, 20, 40), 3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 307

    def update(self):
        self.rect.x -= 10
        if self.rect.x < -20:
            self.kill()

class TelaJogoDino(Tela):
    def __init__(self, navegador=None):
        super().__init__(
            largura=700, altura=400, titulo="Dino",
            cor_fundo=Cores.branco(), navegador=navegador
        )
        self.navegador = navegador
        self.dino = Dino()
        self.cactos = pygame.sprite.Group()
        self.tudo = pygame.sprite.Group(self.dino)
        self.pontuacao = 0
        self.rodando = True
        self.fonte = pygame.font.SysFont("consolas", 32)
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0

        self.adicionar_componente(Botao(
            x=20, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=self.voltar_menu,
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))

    def voltar_menu(self):
        if self.navegador:
            self.navegador.ir_para("menu dino")

    def rodar(self):
        while self.rodando:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.dino.pular()
                    if event.key == pygame.K_ESCAPE:
                        self.voltar_menu()
                        return

            # Spawn cactos
            self.spawn_timer += 1
            if self.spawn_timer > 60 + random.randint(0, 40):
                cacto = Cacto(700)
                self.cactos.add(cacto)
                self.tudo.add(cacto)
                self.spawn_timer = 0

            self.tudo.update()

            # Colisão
            if pygame.sprite.spritecollideany(self.dino, self.cactos):
                self.game_over()
                return

            self.pontuacao += 1

            self.renderizar()

    def renderizar(self):
        self.tela.fill((255, 255, 255))
        pygame.draw.line(self.tela, (120, 120, 120), (0, 350), (700, 350), 3)
        self.tudo.draw(self.tela)
        texto = self.fonte.render(f"Pontos: {self.pontuacao}", True, (0, 0, 0))
        self.tela.blit(texto, (500, 20))
        pygame.display.flip()

    def game_over(self):
        apelido = getattr(self.navegador, "apelido_logado", None) or "Visitante"
        
        # Get user id if logged in
        id_usuario = None
        if apelido != "Visitante":
            usuarios = DadosUsuario.listar_usuarios()
            for u in usuarios:
                if u[3] == apelido:  # Assuming apelido is at index 3
                    id_usuario = u[0]  # Assuming id is at index 0
                    break
        
        # Register game with id_usuario
        DinoDB.registrar_partida(id_usuario, apelido, self.pontuacao)
        DadosUsuario.atualizar_pontuacao_jogo(apelido, "dino", self.pontuacao, tempo=120)
        
        fonte = pygame.font.SysFont("consolas", 48)
        texto = fonte.render("Game Over!", True, (200, 0, 0))
        self.tela.blit(texto, (220, 120))
        pygame.display.flip()
        pygame.time.wait(1800)
        self.voltar_menu()