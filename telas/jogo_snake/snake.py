import pygame
import random
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Musicas
from databases.Snake_database import SnakeDB
from databases.cadastro_database import DadosUsuario

class TelaJogoSnake(Tela):
    GRID_SIZE = 30
    GRID_WIDTH = 30
    GRID_HEIGHT = 20

    def __init__(self, navegador=None):
        super().__init__(
            largura=self.GRID_WIDTH * self.GRID_SIZE,
            altura=self.GRID_HEIGHT * self.GRID_SIZE,
            titulo="Snake",
            cor_fundo=Cores.preto(),
            navegador=navegador
        )
        self.navegador = navegador
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("consolas", 28)
        self.efeito_ponto = "coins"
        self.efeito_gameover = "fim"
        self.musica_fundo = "snake"
        Musicas.tocar_fundo(self.musica_fundo, volume=0.5)
        self.adicionar_componente(Botao(
            x=10, y=10, largura=120, altura=38, texto="Voltar",
            cor_fundo=Cores.cinza(), cor_hover=Cores.cinza_escuro(),
            cor_texto=Cores.branco(),
            funcao=self.voltar_menu,
            fonte=Fontes.consolas(), tamanho_fonte=20, raio_borda=10
        ))

    def rodar(self):
        self.reset()
        while self.rodando:
            self.clock.tick(12)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direcao != (0, 1):
                        self.direcao = (0, -1)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direcao != (0, -1):
                        self.direcao = (0, 1)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direcao != (1, 0):
                        self.direcao = (-1, 0)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direcao != (-1, 0):
                        self.direcao = (1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        self.voltar_menu()
                        return

            self.move()
            self.renderizar()

    def reset(self):
        self.snake = [(15, 10), (14, 10), (13, 10)]
        self.direcao = (1, 0)
        self.spawn_comida()
        self.pontuacao = 0
        self.rodando = True

    def spawn_comida(self):
        while True:
            self.comida = (
                random.randint(0, self.GRID_WIDTH - 1),
                random.randint(0, self.GRID_HEIGHT - 1)
            )
            if self.comida not in self.snake:
                break

    def move(self):
        head = (self.snake[0][0] + self.direcao[0], self.snake[0][1] + self.direcao[1])
        # Colisão com parede
        if (head[0] < 0 or head[0] >= self.GRID_WIDTH or
            head[1] < 0 or head[1] >= self.GRID_HEIGHT or
            head in self.snake):
            self.game_over()
            return
        self.snake.insert(0, head)
        if head == self.comida:
            self.pontuacao += 1
            Musicas.tocar_efeito(self.efeito_ponto, volume=self.navegador.volume_efeito)
            self.spawn_comida()
        else:
            self.snake.pop()

    def renderizar(self):
        self.tela.fill((0, 0, 0))
        # Desenha cobra
        for pos in self.snake:
            rect = pygame.Rect(pos[0]*self.GRID_SIZE, pos[1]*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
            pygame.draw.rect(self.tela, (0, 255, 0), rect)
        # Desenha comida
        rect = pygame.Rect(self.comida[0]*self.GRID_SIZE, self.comida[1]*self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
        pygame.draw.rect(self.tela, (255, 0, 0), rect)
        # Pontuação
        texto = self.fonte.render(f"Pontos: {self.pontuacao}", True, (255, 255, 255))
        self.tela.blit(texto, (10, self.GRID_HEIGHT * self.GRID_SIZE - 40))
        pygame.display.flip()

    def game_over(self):
        apelido = getattr(self.navegador, "apelido_logado", None) or "Visitante"
        
        # Busca o id do usuário se estiver logado
        id_usuario = None
        if apelido != "Visitante":
            usuarios = DadosUsuario.listar_usuarios()
            for u in usuarios:
                if u[3] == apelido:  # Ajuste o índice conforme sua tabela
                    id_usuario = u[0]
                    break
        
        print(f"Registrando partida: id={id_usuario}, apelido={apelido}, pontos={self.pontuacao}")  # DEBUG
        SnakeDB.registrar_partida(id_usuario, apelido, self.pontuacao)
        DadosUsuario.atualizar_pontuacao_jogo(apelido, "snake", self.pontuacao, tempo=120)
        fonte = pygame.font.SysFont("consolas", 48)
        texto = fonte.render("Game Over!", True, (200, 0, 0))
        self.tela.blit(texto, (60, 160))
        pygame.display.flip()
        pygame.time.wait(1800)
        self.voltar_menu()

    def voltar_menu(self):
        if self.navegador:
            self.navegador.ir_para("menu snake")