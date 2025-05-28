import pygame
import random
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Efeitos, Musicas
from databases.tetris_database import TetrisDB
from databases.cadastro_database import DadosUsuario


# Definições das peças
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 0, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0)
]

class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TelaJogoTetris(Tela):
    ROWS = 20
    COLS = 10
    BLOCK = 30

    def __init__(self, navegador=None):
        super().__init__(
            largura=self.COLS * self.BLOCK + 200, altura=self.ROWS * self.BLOCK,
            titulo="Tetris", cor_fundo=Cores.preto(), navegador=navegador
        )
        self.navegador = navegador
        self.grid = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.pontuacao = 0
        self.linhas = 0
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.efeito_linha = "correto"
        self.efeito_gameover = "fim"
        self.nova_peca()
        self.fall_time = 0
        self.fall_speed = 500  # ms

        self.adicionar_componente(Botao(
            x=self.COLS * self.BLOCK + 40, y=20, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=self.voltar_menu,
            tamanho_fonte=20, raio_borda=10
        ))

    def nova_peca(self):
        idx = random.randint(0, len(SHAPES) - 1)
        self.peca = Piece(3, 0, [row[:] for row in SHAPES[idx]], COLORS[idx])

    def rodar(self):
        while self.rodando:
            self.clock.tick(60)
            self.fall_time += self.clock.get_time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Musicas.tocar_efeito(Efeitos.clique())
                        self.move(-1)
                    if event.key == pygame.K_RIGHT:
                        Musicas.tocar_efeito(Efeitos.clique())
                        self.move(1)
                    if event.key == pygame.K_DOWN:
                        Musicas.tocar_efeito(Efeitos.clique())
                        self.descida()
                    if event.key == pygame.K_UP:
                        Musicas.tocar_efeito(Efeitos.clique())
                        self.peca.rotate()
                        if self.colide():
                            for _ in range(3): self.peca.rotate()
                    if event.key == pygame.K_ESCAPE:
                        Musicas.tocar_efeito(Efeitos.sair())
                        self.voltar_menu()
                        return

            if self.fall_time > self.fall_speed:
                self.descida()
                self.fall_time = 0

            self.renderizar()

    def move(self, dx):
        self.peca.x += dx
        if self.colide():
            self.peca.x -= dx

    def descida(self):
        self.peca.y += 1
        if self.colide():
            self.peca.y -= 1
            self.fixar()
            self.limpar_linhas()
            self.nova_peca()
            if self.colide():
                self.game_over()

    def colide(self):
        for y, row in enumerate(self.peca.shape):
            for x, val in enumerate(row):
                if val:
                    px = self.peca.x + x
                    py = self.peca.y + y
                    if px < 0 or px >= self.COLS or py >= self.ROWS:
                        return True
                    if py >= 0 and self.grid[py][px]:
                        return True
        return False

    def fixar(self):
        for y, row in enumerate(self.peca.shape):
            for x, val in enumerate(row):
                if val:
                    px = self.peca.x + x
                    py = self.peca.y + y
                    if 0 <= px < self.COLS and 0 <= py < self.ROWS:
                        self.grid[py][px] = self.peca.color

    def limpar_linhas(self):
        linhas_removidas = 0
        for y in range(self.ROWS - 1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.COLS)])
                linhas_removidas += 1
        if linhas_removidas:
            self.linhas += linhas_removidas
            self.pontuacao += (100 * linhas_removidas)
            from utilitarios.musicas import Musicas
            Musicas.tocar_efeito(self.efeito_linha, volume=0.7)

    def renderizar(self):
        self.tela.fill((0, 0, 0))
        # Grade
        for y in range(self.ROWS):
            for x in range(self.COLS):
                rect = pygame.Rect(x * self.BLOCK, y * self.BLOCK, self.BLOCK, self.BLOCK)
                pygame.draw.rect(self.tela, (40, 40, 40), rect, 1)
                if self.grid[y][x]:
                    pygame.draw.rect(self.tela, self.grid[y][x], rect)
        # Peça atual
        for y, row in enumerate(self.peca.shape):
            for x, val in enumerate(row):
                if val:
                    px = self.peca.x + x
                    py = self.peca.y + y
                    if py >= 0:
                        rect = pygame.Rect(px * self.BLOCK, py * self.BLOCK, self.BLOCK, self.BLOCK)
                        pygame.draw.rect(self.tela, self.peca.color, rect)
        # Pontuação e linhas
        texto = self.fonte.render(f"Pontos: {self.pontuacao}", True, (255, 255, 255))
        self.tela.blit(texto, (self.COLS * self.BLOCK + 20, 100))
        texto2 = self.fonte.render(f"Linhas: {self.linhas}", True, (255, 255, 255))
        self.tela.blit(texto2, (self.COLS * self.BLOCK + 20, 150))
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
                TetrisDB.registrar_partida(id_usuario, apelido, self.pontuacao, self.linhas)
                DadosUsuario.atualizar_pontuacao_jogo(apelido, "tetris", self.pontuacao, tempo=120)
        else:
            TetrisDB.registrar_partida(apelido=apelido, pontuacao=self.pontuacao, linhas=self.linhas)
        
        fonte = pygame.font.SysFont("consolas", 48)
        texto = fonte.render("Game Over!", True, (200, 0, 0))
        self.tela.blit(texto, (60, 250))
        pygame.display.flip()
        pygame.time.wait(1800)
        self.voltar_menu()

    def voltar_menu(self):
        if self.navegador:
            self.navegador.ir_para("menu tetris")