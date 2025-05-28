import pygame
import random
import sys
from utilitarios.Aprincipal_widgets import Tela, Botao, Cores, TextoFormatado, Fontes
from utilitarios.musicas import Efeitos, Musicas
from databases.forca_database import ForcaDB
from databases.cadastro_database import DadosUsuario

class TelaJogoForca(Tela):
    GRID_SIZE = 30
    GRID_WIDTH = 30
    GRID_HEIGHT = 20
    MAX_TENTATIVAS = 6

    def __init__(self, navegador=None):
        super().__init__(
            largura=self.GRID_WIDTH * self.GRID_SIZE,
            altura=self.GRID_HEIGHT * self.GRID_SIZE,
            titulo="Forca",
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
        self.reiniciar_jogo()
        self.pontuacao = 0

    def reiniciar_jogo(self):
        self.palavras = ["python", "programacao", "pygame", "forca", "computador"]
        self.palavra_secreta = random.choice(self.palavras).upper()
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas = self.MAX_TENTATIVAS
        self.jogo_ativo = True

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and self.jogo_ativo:
                letra = evento.unicode.upper()
                if letra.isalpha() and len(letra) == 1:
                    if letra in self.palavra_secreta:
                        Musicas.tocar_efeito(Efeitos.correto())
                        self.letras_corretas.add(letra)

                        if all(letra in self.letras_corretas for letra in self.palavra_secreta):
                            self.pontuacao += 1  # ✅ 1 ponto por palavra certa
                            self.jogo_ativo = False
                            Musicas.tocar_efeito(self.efeito_ponto)
                            pygame.time.wait(1000)
                            self.reiniciar_jogo()
                    else:
                        if letra not in self.letras_erradas:
                            Musicas.tocar_efeito(Efeitos.incorreto())
                            self.letras_erradas.add(letra)
                            self.tentativas -= 1
                            if self.tentativas == 0:
                                self.jogo_ativo = False
                                self.game_over()

    def renderizar(self):
        self.tela.fill((0, 0, 0))

        # Forca e boneco
        self.desenhar_forca()

        # Palavra oculta
        palavra_exibida = " ".join([letra if letra in self.letras_corretas else "_" for letra in self.palavra_secreta])
        texto_palavra = self.fonte.render(palavra_exibida, True, (255, 255, 255))
        self.tela.blit(texto_palavra, (60, 350))

        # Letras erradas
        texto_erradas = self.fonte.render(f"Erradas: {' '.join(self.letras_erradas)}", True, (255, 0, 0))
        self.tela.blit(texto_erradas, (60, 400))

        # Tentativas restantes
        texto_tentativas = self.fonte.render(f"Tentativas: {self.tentativas}", True, (255, 255, 0))
        self.tela.blit(texto_tentativas, (60, 440))

        # Pontuação
        texto_pontos = self.fonte.render(f"Pontos: {self.pontuacao}", True, (255, 255, 255))
        self.tela.blit(texto_pontos, (10, self.GRID_HEIGHT * self.GRID_SIZE - 40))

        pygame.display.flip()

    def desenhar_forca(self):
        base_x, base_y = 60, 300

        # Estrutura da forca
        pygame.draw.line(self.tela, Cores.branco(), (base_x, base_y), (base_x + 100, base_y), 3)  # base
        pygame.draw.line(self.tela, Cores.branco(), (base_x + 50, base_y), (base_x + 50, base_y - 150), 3)  # vertical
        pygame.draw.line(self.tela, Cores.branco(), (base_x + 50, base_y - 150), (base_x + 100, base_y - 150),
                         3)  # topo
        pygame.draw.line(self.tela, Cores.branco(), (base_x + 100, base_y - 150), (base_x + 100, base_y - 120),
                         3)  # corda

        erros = len(self.letras_erradas)

        # Cabeça
        if erros > 0:
            pygame.draw.circle(self.tela, Cores.branco(), (base_x + 100, base_y - 100), 10, 2)

        # Corpo
        if erros > 1:
            pygame.draw.line(self.tela, Cores.branco(), (base_x + 100, base_y - 90), (base_x + 100, base_y - 50), 2)

        # Braço esquerdo
        if erros > 2:
            pygame.draw.line(self.tela, Cores.branco(), (base_x + 100, base_y - 80), (base_x + 80, base_y - 70), 2)

        # Braço direito
        if erros > 3:
            pygame.draw.line(self.tela, Cores.branco(), (base_x + 100, base_y - 80), (base_x + 120, base_y - 70), 2)

        # Perna esquerda
        if erros > 4:
            pygame.draw.line(self.tela, Cores.branco(), (base_x + 100, base_y - 50), (base_x + 85, base_y - 30), 2)

        # Perna direita
        if erros > 5:
            pygame.draw.line(self.tela, Cores.branco(), (base_x + 100, base_y - 50), (base_x + 115, base_y - 30), 2)

    def game_over(self):
        Musicas.tocar_efeito(self.efeito_gameover, volume=self.navegador.volume_efeito)
        apelido = getattr(self.navegador, "apelido_logado", None) or "Visitante"
        id_usuario = getattr(self.navegador, "id_logado", None)
        if id_usuario:
            ForcaDB.registrar_partida(apelido, self.pontuacao, id_usuario=id_usuario)
            DadosUsuario.atualizar_pontuacao_jogo(apelido, "forca", self.pontuacao, tempo=120)
        else:
            ForcaDB.registrar_partida(apelido, self.pontuacao)

        # Limpa a tela
        self.tela.fill((0, 0, 0))
        texto = pygame.font.SysFont("consolas", 48).render("Game Over!", True, (200, 0, 0))
        texto_rect = texto.get_rect(center=(self.largura // 2, self.altura // 2))
        self.tela.blit(texto, texto_rect)

        pygame.display.flip()
        pygame.time.wait(2000)
        self.voltar_menu()

    def voltar_menu(self):
        if self.navegador:
            self.navegador.ir_para("menu forca")

    def executar(self):
        while True:
            self.clock.tick(30)
            self.processar_eventos()
            self.renderizar()
