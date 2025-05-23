import pygame
import sys
from typing import Callable

pygame.init()

class Fontes:
    """
    Classe utilitária para facilitar o uso de fontes do sistema no pygame.

    Opções de fontes disponíveis (nomes aceitos em pygame.font.SysFont):
    --------------------------------------------------------------------
    - Fontes.arial()             # Arial (ampla compatibilidade)
    - Fontes.verdana()           # Verdana (limpa, ótima para interfaces)
    - Fontes.tahoma()            # Tahoma (sem serifa, moderna)
    - Fontes.calibri()           # Calibri (moderna, padrão do Office)
    - Fontes.consolas()          # Consolas (monoespaçada, ótima para código)
    - Fontes.comic_sans()        # Comic Sans MS (informal, divertida)
    - Fontes.times()             # Times New Roman (tradicional, com serifa)
    - Fontes.courier()           # Courier New (monoespaçada, clássica)
    - Fontes.impact()            # Impact (grossa, para títulos)
    - Fontes.georgia()           # Georgia (com serifa, elegante)
    - Fontes.lucida_console()    # Lucida Console (monoespaçada, legível)
    - Fontes.segoe_ui()          # Segoe UI (padrão do Windows moderno)
    - Fontes.trebuchet()         # Trebuchet MS (sem serifa, moderna)
    - Fontes.lucida_sans()       # Lucida Sans Unicode (sem serifa, clara)
    - Fontes.palatino()          # Palatino Linotype (com serifa, clássica)
    - Fontes.century_gothic()    # Century Gothic (sem serifa, arredondada)
    """

    @staticmethod
    def arial():
        """Fonte Arial (ampla compatibilidade)."""
        return "arial"

    @staticmethod
    def verdana():
        """Fonte Verdana (limpa, ótima para interfaces)."""
        return "verdana"

    @staticmethod
    def tahoma():
        """Fonte Tahoma (sem serifa, moderna)."""
        return "tahoma"

    @staticmethod
    def calibri():
        """Fonte Calibri (moderna, padrão do Office)."""
        return "calibri"

    @staticmethod
    def consolas():
        """Fonte Consolas (monoespaçada, ótima para código)."""
        return "consolas"

    @staticmethod
    def comic_sans():
        """Fonte Comic Sans MS (informal, divertida)."""
        return "comic sans ms"

    @staticmethod
    def times():
        """Fonte Times New Roman (tradicional, com serifa)."""
        return "times new roman"

    @staticmethod
    def courier():
        """Fonte Courier New (monoespaçada, clássica)."""
        return "courier new"

    @staticmethod
    def impact():
        """Fonte Impact (grossa, para títulos)."""
        return "impact"

    @staticmethod
    def georgia():
        """Fonte Georgia (com serifa, elegante)."""
        return "georgia"

    @staticmethod
    def lucida_console():
        """Fonte Lucida Console (monoespaçada, legível)."""
        return "lucida console"

    @staticmethod
    def segoe_ui():
        """Fonte Segoe UI (padrão do Windows moderno)."""
        return "segoe ui"

    @staticmethod
    def trebuchet():
        """Fonte Trebuchet MS (sem serifa, moderna)."""
        return "trebuchet ms"

    @staticmethod
    def lucida_sans():
        """Fonte Lucida Sans Unicode (sem serifa, clara)."""
        return "lucida sans unicode"

    @staticmethod
    def palatino():
        """Fonte Palatino Linotype (com serifa, clássica)."""
        return "palatino linotype"

    @staticmethod
    def century_gothic():
        """Fonte Century Gothic (sem serifa, arredondada)."""
        return "century gothic"


# =========================
# CORES PADRÃO DO SISTEMA
# =========================
class Cores:
    """
    Classe utilitária para cores RGB padrão do sistema, incluindo variações de tons.

    Opções de cores disponíveis:
    ---------------
    # CLARAS
    - Cores.azul_claro()
    - Cores.azul_celeste()
    - Cores.azul_turquesa()
    - Cores.verde()
    - Cores.verde_lima()
    - Cores.verde_agua()
    - Cores.verde_menta()
    - Cores.verde_pastel()
    - Cores.amarelo()
    - Cores.amarelo_ouro()
    - Cores.amarelo_canario()
    - Cores.amarelo_claro()
    - Cores.laranja_claro()
    - Cores.laranja_pastel()
    - Cores.rosa()
    - Cores.rosa_bebe()
    - Cores.rosa_claro()
    - Cores.violeta()
    - Cores.ametista()
    - Cores.lavanda()
    - Cores.bege()
    - Cores.cinza_claro()
    - Cores.prata()
    - Cores.creme()
    - Cores.branco()
    - Cores.azul_aguamarinha()
    - Cores.azul_topazio()
    - Cores.verde_esmeralda()
    - Cores.coral()
    - Cores.salmao()
    - Cores.pessego()
    - Cores.menta()
    - Cores.aguamarinha()
    - Cores.esmeralda()
    - Cores.dourado()
    - Cores.magenta()
    - Cores.ciano()
    - Cores.turquesa()

    # INTERMEDIÁRIAS
    - Cores.vermelho_alaranjado()
    - Cores.amarelo_escuro()
    - Cores.laranja()
    - Cores.marrom_claro()
    - Cores.terracota()
    - Cores.ocre()
    - Cores.cobre()
    - Cores.ouro_velho()
    - Cores.cinza()
    
    # ESCURAS
    - Cores.vermelho()
    - Cores.vermelho_escuro()
    - Cores.vermelho_vinho()
    - Cores.vermelho_tijolo()
    - Cores.azul()
    - Cores.azul_escuro()
    - Cores.azul_marinho()
    - Cores.azul_royal()
    - Cores.verde_escuro()
    - Cores.verde_oliva()
    - Cores.verde_musgo()
    - Cores.laranja_escuro()
    - Cores.rosa_choque()
    - Cores.roxo()
    - Cores.roxo_escuro()
    - Cores.indigo()
    - Cores.purpura()
    - Cores.marrom()
    - Cores.marrom_escuro()
    - Cores.cinza_escuro()
    - Cores.grafite()
    - Cores.chumbo()
    - Cores.carvao()
    - Cores.preto()
    - Cores.azul_petroleo()
    - Cores.azul_safira()
    - Cores.rubi()
    - Cores.safira()

    # Dica: Prefira cores "claras" para textos sobre fundos escuros e cores "escuras" para textos sobre fundos claros.
    """

    # Tons de vermelho
    @staticmethod
    def vermelho(): return (255, 0, 0)
    @staticmethod
    def vermelho_escuro(): return (139, 0, 0)
    @staticmethod
    def vermelho_vinho(): return (128, 0, 32)
    @staticmethod
    def vermelho_tijolo(): return (178, 34, 34)
    @staticmethod
    def vermelho_alaranjado(): return (255, 69, 0)

    # Tons de azul
    @staticmethod
    def azul(): return (0, 0, 255)
    @staticmethod
    def azul_escuro(): return (0, 0, 139)
    @staticmethod
    def azul_marinho(): return (0, 0, 128)
    @staticmethod
    def azul_royal(): return (65, 105, 225)
    @staticmethod
    def azul_claro(): return (173, 216, 230)
    @staticmethod
    def azul_celeste(): return (135, 206, 235)
    @staticmethod
    def azul_turquesa(): return (64, 224, 208)

    # Tons de verde
    @staticmethod
    def verde(): return (0, 255, 0)
    @staticmethod
    def verde_escuro(): return (0, 100, 0)
    @staticmethod
    def verde_oliva(): return (107, 142, 35)
    @staticmethod
    def verde_lima(): return (50, 205, 50)
    @staticmethod
    def verde_musgo(): return (85, 107, 47)
    @staticmethod
    def verde_agua(): return (127, 255, 212)
    @staticmethod
    def verde_menta(): return (152, 255, 152)
    @staticmethod
    def verde_pastel(): return (119, 221, 119)

    # Tons de amarelo
    @staticmethod
    def amarelo(): return (255, 255, 0)
    @staticmethod
    def amarelo_ouro(): return (255, 215, 0)
    @staticmethod
    def amarelo_canario(): return (255, 255, 153)
    @staticmethod
    def amarelo_escuro(): return (204, 204, 0)
    @staticmethod
    def amarelo_claro(): return (255, 255, 102)

    # Tons de laranja
    @staticmethod
    def laranja(): return (255, 140, 0)
    @staticmethod
    def laranja_escuro(): return (255, 69, 0)
    @staticmethod
    def laranja_claro(): return (255, 200, 124)
    @staticmethod
    def laranja_pastel(): return (255, 179, 71)

    # Tons de rosa
    @staticmethod
    def rosa(): return (255, 105, 180)
    @staticmethod
    def rosa_choque(): return (255, 20, 147)
    @staticmethod
    def rosa_bebe(): return (255, 182, 193)
    @staticmethod
    def rosa_claro(): return (255, 192, 203)

    # Tons de roxo/violeta
    @staticmethod
    def roxo(): return (128, 0, 128)
    @staticmethod
    def roxo_escuro(): return (75, 0, 130)
    @staticmethod
    def violeta(): return (238, 130, 238)
    @staticmethod
    def indigo(): return (75, 0, 130)
    @staticmethod
    def ametista(): return (153, 102, 204)
    @staticmethod
    def lavanda(): return (230, 230, 250)
    @staticmethod
    def purpura(): return (128, 0, 128)

    # Tons de marrom
    @staticmethod
    def marrom(): return (139, 69, 19)
    @staticmethod
    def marrom_claro(): return (205, 133, 63)
    @staticmethod
    def marrom_escuro(): return (92, 51, 23)
    @staticmethod
    def bege(): return (245, 245, 220)
    @staticmethod
    def terracota(): return (226, 114, 91)
    @staticmethod
    def ocre(): return (204, 119, 34)
    @staticmethod
    def cobre(): return (184, 115, 51)
    @staticmethod
    def ouro_velho(): return (184, 134, 11)

    # Tons de cinza e neutros
    @staticmethod
    def cinza(): return (100, 100, 100)
    @staticmethod
    def cinza_claro(): return (200, 200, 200)
    @staticmethod
    def cinza_escuro(): return (30, 30, 30)
    @staticmethod
    def grafite(): return (54, 69, 79)
    @staticmethod
    def chumbo(): return (70, 70, 70)
    @staticmethod
    def prata(): return (192, 192, 192)
    @staticmethod
    def carvao(): return (54, 69, 79)
    @staticmethod
    def creme(): return (255, 253, 208)
    @staticmethod
    def branco(): return (255, 255, 255)
    @staticmethod
    def preto(): return (0, 0, 0)

    # Outros tons e especiais
    @staticmethod
    def azul_petroleo(): return (0, 95, 105)
    @staticmethod
    def azul_safira(): return (15, 82, 186)
    @staticmethod
    def azul_aguamarinha(): return (127, 255, 212)
    @staticmethod
    def azul_topazio(): return (48, 176, 222)
    @staticmethod
    def verde_esmeralda(): return (80, 200, 120)
    @staticmethod
    def rubi(): return (224, 17, 95)
    @staticmethod
    def coral(): return (255, 127, 80)
    @staticmethod
    def salmao(): return (250, 128, 114)
    @staticmethod
    def pessego(): return (255, 218, 185)
    @staticmethod
    def menta(): return (152, 255, 152)
    @staticmethod
    def aguamarinha(): return (127, 255, 212)
    @staticmethod
    def esmeralda(): return (80, 200, 120)
    @staticmethod
    def safira(): return (15, 82, 186)
    @staticmethod
    def ametista(): return (153, 102, 204)
    @staticmethod
    def lavanda(): return (230, 230, 250)
    @staticmethod
    def dourado(): return (255, 215, 0)
    @staticmethod
    def magenta(): return (255, 0, 255)
    @staticmethod
    def ciano(): return (0, 255, 255)
    @staticmethod
    def turquesa(): return (64, 224, 208)
    # ...adicione mais conforme desejar...

# =========================
# CLASSE TELA
# =========================
class Tela:
    """
    Classe base para criar uma janela/tela do sistema.

    Como usar:
    -----------
    1. Instancie a tela:
        tela = Tela(largura=800, altura=600, titulo="Minha Tela", cor_fundo=Cores.cinza())
    2. Adicione componentes (Botao, CaixaTexto, TextoFormatado, etc):
        tela.adicionar_componente(meu_botao)
    3. Exiba a tela:
        tela.rodar()

    Parâmetros do construtor:
    ------------------------
    - largura (int): Largura da tela em pixels.
    - altura (int): Altura da tela em pixels.
    - titulo (str): Título da janela.
    - cor_fundo (tuple): Cor de fundo (use Cores).
    - navegador (opcional): Objeto de navegação entre telas.
    - imagem_fundo (opcional): Caminho ou Surface para imagem de fundo.

    Métodos principais:
    -------------------
    - adicionar_componente(componente): Adiciona um componente visual à tela.
    - rodar(): Inicia o loop principal da tela (chame para exibir).
    - sair(): Fecha a aplicação.

    Observação:
    -----------
    Você NÃO precisa se preocupar com eventos do Pygame ou atualização dos componentes.
    Basta adicionar os componentes e chamar tela.rodar().
    """
    def __init__(self, largura=600, altura=600, titulo="Tela", cor_fundo=Cores.preto(), navegador=None, imagem_fundo=None, logo=None):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = cor_fundo
        self.imagem_fundo = imagem_fundo
        self.logo = logo
        self.navegador = navegador
        self.tela_cheia = False
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(titulo)
        self.componentes = []

        # --- NOVO: define o ícone da janela se logo for fornecida ---
        if self.logo:
            if isinstance(self.logo, str):
                from utilitarios.imagens import carregar_imagem
                logo_surface = carregar_imagem(self.logo, (32, 32))  # tamanho ideal para ícone
            else:
                logo_surface = self.logo
            pygame.display.set_icon(logo_surface)

    def adicionar_componente(self, componente):
        """Adiciona um componente visual à tela (botão, texto, caixa de texto, etc)."""
        self.componentes.append(componente)

    def processar_eventos(self):
        """Processa eventos do Pygame e repassa para os componentes."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                # Alterna entre tela cheia e janela
                if self.tela_cheia:
                    self.tela = pygame.display.set_mode((self.largura, self.altura))
                else:
                    self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.FULLSCREEN)
                self.tela_cheia = not self.tela_cheia
            for componente in self.componentes:
                if hasattr(componente, 'processar_evento'):
                    componente.processar_evento(evento)

    def atualizar(self):
        """Atualiza todos os componentes (caso necessário)."""
        for componente in self.componentes:
            if hasattr(componente, 'atualizar'):
                componente.atualizar()

    def renderizar(self):
        """Desenha o fundo e todos os componentes na tela."""
        if self.imagem_fundo:
            if isinstance(self.imagem_fundo, str):
                from utilitarios.imagens import carregar_imagem
                img = carregar_imagem(self.imagem_fundo, (self.largura, self.altura))
            else:
                img = pygame.transform.scale(self.imagem_fundo, (self.largura, self.altura))
            self.tela.blit(img, (0, 0))
        else:
            self.tela.fill(self.cor_fundo)
        for componente in self.componentes:
            if hasattr(componente, 'desenhar'):
                componente.desenhar(self.tela)
        pygame.display.flip()

    def sair(self):
        """Fecha a aplicação."""
        pygame.quit()
        sys.exit()

    def rodar(self):
        """Loop principal da tela. Chame este método para exibir a tela."""
        while True:
            self.processar_eventos()
            self.atualizar()
            self.renderizar()
            pygame.time.Clock().tick(60)

# =========================
# CLASSE BOTÃO
# =========================
class Botao:
    """
    Classe para criar um botão clicável.

    Como usar:
    -----------
    1. Instancie o botão:
        botao = Botao(x=100, y=200, largura=150, altura=50, texto="Clique", funcao=minha_funcao)
    2. Adicione à tela:
        tela.adicionar_componente(botao)

    Parâmetros do construtor:
    ------------------------
    - x, y (int): Posição do canto superior esquerdo.
    - largura, altura (int): Tamanho do botão.
    - texto (str): Texto exibido no botão.
    - funcao (callable): Função chamada ao clicar.
    - cor_fundo, cor_hover, cor_texto (tuple): Cores do botão.
    - raio_borda (int): Arredondamento das bordas.
    - imagem (str ou Surface): Caminho para imagem opcional.
    - fonte (str): Nome da fonte (padrão: "arial").
    - tamanho_fonte (int): Tamanho da fonte (padrão: 36).

    Métodos principais:
    -------------------
    - foi_clicado(): Retorna True se o botão foi clicado no último frame.
      (Útil apenas se quiser lógica extra além da função passada.)

    Observação:
    -----------
    Você NÃO precisa chamar desenhar, processar_evento ou atualizar manualmente.
    O sistema faz isso automaticamente ao adicionar o botão à tela.
    """
    def __init__(self, x=0, y=0, largura=0, altura=0, cor_fundo=Cores.verde(), cor_hover=Cores.verde(), cor_texto=Cores.preto(), texto="botao", raio_borda=5, funcao: Callable|None = None, imagem=None, fonte="arial", tamanho_fonte=36):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.imagem = None
        if imagem:
            from utilitarios.imagens import carregar_imagem
            self.imagem = carregar_imagem(imagem, (largura, altura))
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.texto = texto
        self.fonte = pygame.font.SysFont(fonte, tamanho_fonte)
        self.texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        self.texto_rect = self.texto_surface.get_rect(center=self.rect.center)
        self.clicado = False
        self.raio_borda = raio_borda
        self.funcao = funcao

    def desenhar(self, tela, mouse_pos=None):
        """Desenha o botão na tela."""
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        cor = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor_fundo
        pygame.draw.rect(tela, cor, self.rect, border_radius=self.raio_borda)
        if self.imagem:
            tela.blit(self.imagem, self.rect)
        pygame.draw.rect(tela, self.cor_texto, self.rect, 2, border_radius=self.raio_borda)
        tela.blit(self.texto_surface, self.texto_rect)

    def processar_evento(self, evento):
        """
        Detecta clique e executa a função associada.
        Chame este método no loop de eventos da tela.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.clicado = True
                print(f"Botão '{self.texto}' clicado!")
                if self.funcao:
                    self.funcao()

    def atualizar(self):
        """
        Reseta o estado de clique a cada frame.
        Chame este método no loop de atualização da tela.
        """
        self.clicado = False

    def foi_clicado(self):
        """
        Retorna True se o botão foi clicado no último frame.
        Útil para lógica baseada em clique.
        """
        return self.clicado

# =========================
# CLASSE CAIXA DE TEXTO
# =========================
class CaixaTexto:
    """
    Caixa de texto para entrada de dados pelo usuário.

    Como usar:
    -----------
    1. Instancie a caixa:
        caixa = CaixaTexto(x=100, y=300, largura=200, altura=40, placeholder="Digite aqui")
    2. Adicione à tela:
        tela.adicionar_componente(caixa)
    3. Leia o texto digitado:
        texto = caixa.texto

    Parâmetros do construtor:
    ------------------------
    - x, y (int): Posição do canto superior esquerdo.
    - largura, altura (int): Tamanho da caixa.
    - placeholder (str): Texto de dica exibido quando vazio.
    - cor_fundo, cor_borda, cor_texto (tuple): Cores.
    - fonte (str): Nome da fonte (padrão: "arial").
    - tamanho_fonte (int): Tamanho da fonte (padrão: 36).
    - raio_borda (int): Arredondamento das bordas.

    Métodos principais:
    -------------------
    - texto (str): Atributo que contém o texto digitado.

    Observação:
    -----------
    Você NÃO precisa chamar desenhar ou processar_evento manualmente.
    O sistema faz isso automaticamente ao adicionar a caixa à tela.
    """
    def __init__(self, x=0, y=0, largura=0, altura=0, cor_fundo=Cores.preto(), cor_borda=Cores.preto(), cor_texto=Cores.preto(), fonte="arial", placeholder="", raio_borda=5, tamanho_fonte=36):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda
        self.cor_texto = cor_texto
        self.placeholder = placeholder
        self.texto = ""
        self.ativo = False
        self.fonte = pygame.font.SysFont(fonte, tamanho_fonte)
        self.raio_borda = raio_borda

    def desenhar(self, tela):
        """Desenha a caixa de texto na tela."""
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=self.raio_borda)
        pygame.draw.rect(tela, self.cor_borda, self.rect, 2, border_radius=self.raio_borda)
        if self.texto == "" and not self.ativo:
            texto_surface = self.fonte.render(self.placeholder, True, (150, 150, 150))
        else:
            texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        tela.blit(texto_surface, (self.rect.x + 10, self.rect.y + 10))

    def processar_evento(self, evento):
        """
        Processa eventos de clique e teclado para entrada de texto.
        Chame este método no loop de eventos da tela.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.ativo = self.rect.collidepoint(evento.pos)
        if evento.type == pygame.KEYDOWN and self.ativo:
            if evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif evento.key == pygame.K_RETURN:
                print(f"Texto digitado: {self.texto}")
                self.ativo = False
            else:
                self.texto += evento.unicode

# =========================
# CLASSE TEXTO FORMATADO
# =========================
class TextoFormatado:
    """
    Exibe um texto customizado na tela.

    Como usar:
    -----------
    1. Instancie o texto:
        txt = TextoFormatado(x=100, y=50, texto="Bem-vindo!", cor_texto=Cores.branco(), tamanho=36)
    2. Adicione à tela:
        tela.adicionar_componente(txt)
    3. Para atualizar o texto:
        txt.atualizar_texto("Novo texto")

    Parâmetros do construtor:
    ------------------------
    - x, y (int): Posição do texto.
    - texto (str): Texto exibido.
    - cor_texto (tuple): Cor do texto.
    - tamanho (int): Tamanho da fonte.
    - fonte_nome (str): Caminho para fonte customizada (opcional).
    - centralizado (bool): Centraliza o texto na posição (x, y).

    Métodos principais:
    -------------------
    - atualizar_texto(novo_texto): Atualiza o texto exibido.

    Observação:
    -----------
    Você NÃO precisa chamar desenhar manualmente.
    O sistema faz isso automaticamente ao adicionar o texto à tela.
    """
    def __init__(self, x=0, y=0, texto="", cor_texto=Cores.preto(), tamanho=36, fonte_nome='arial', centralizado=False):
        self.x = x
        self.y = y
        self.texto = texto
        self.cor_texto = cor_texto
        self.tamanho = tamanho
        self.centralizado = centralizado
        self.fonte = pygame.font.SysFont(fonte_nome, tamanho)
        self.texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        self.texto_rect = self.texto_surface.get_rect()
        if self.centralizado:
            self.texto_rect.center = (x, y)
        else:
            self.texto_rect.topleft = (x, y)

    def atualizar_texto(self, novo_texto):
        """
        Atualiza o texto exibido.
        Use para mudar o texto dinamicamente.
        """
        self.texto = novo_texto
        self.texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        if self.centralizado:
            self.texto_rect = self.texto_surface.get_rect(center=(self.x, self.y))
        else:
            self.texto_rect = self.texto_surface.get_rect(topleft=(self.x, self.y))

    def desenhar(self, tela):
        """Desenha o texto na tela."""
        tela.blit(self.texto_surface, self.texto_rect)


class ScrollArea:
    """
    Área de rolagem vertical para componentes, com barra customizável.

    Parâmetros:
    -----------
    - x, y (int): Posição do canto superior esquerdo.
    - largura, altura (int): Tamanho da área visível.
    - altura_conteudo (int): Altura total do conteúdo rolável.
    - cor_fundo (tuple): Cor de fundo da área.
    - cor_barra (tuple): Cor da barra de rolagem.
    - largura_barra (int): Largura da barra de rolagem.
    - scroll_velocidade (int): Pixels rolados por evento de scroll.

    Personalização:
    ---------------
    - Altere cor_fundo, cor_barra, largura_barra e scroll_velocidade para customizar o visual e comportamento.
    - Adicione qualquer componente visual (Botao, CaixaTexto, Painel, etc).

    Métodos principais:
    -------------------
    - adicionar_componente(componente): Adiciona um componente à área rolável.
    """
    def __init__(self, x, y, largura, altura, altura_conteudo, cor_fundo, cor_barra, largura_barra=10, scroll_velocidade=20):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.altura_conteudo = altura_conteudo
        self.scroll_y = 0
        self.scroll_velocidade = scroll_velocidade
        self.cor_fundo = cor_fundo
        self.cor_barra = cor_barra
        self.largura_barra = largura_barra
        self.componentes = []

    def adicionar_componente(self, componente):
        """Adiciona um componente à área rolável."""
        self.componentes.append(componente)

    def processar_evento(self, evento):
        """
        Processa eventos de rolagem do mouse e repassa eventos de mouse para os componentes internos.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                if evento.button == 4:  # scroll up
                    self.scroll_y = max(0, self.scroll_y - self.scroll_velocidade)
                elif evento.button == 5:  # scroll down
                    max_scroll = max(0, self.altura_conteudo - self.rect.height)
                    self.scroll_y = min(max_scroll, self.scroll_y + self.scroll_velocidade)

        # Repasse eventos de mouse para componentes, ajustando a posição do mouse
        if evento.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            mouse_x, mouse_y = evento.pos
            if self.rect.collidepoint(mouse_x, mouse_y):
                rel_x = mouse_x - self.rect.x
                rel_y = mouse_y - self.rect.y + self.scroll_y
                novo_evento = evento
                if hasattr(evento, 'dict'):
                    novo_evento = pygame.event.Event(evento.type, {**evento.dict, 'pos': (rel_x, rel_y)})
                for componente in self.componentes:
                    if hasattr(componente, 'processar_evento'):
                        componente.processar_evento(novo_evento)

    def desenhar(self, tela):
        """
        Desenha a área de rolagem, seus componentes e a barra de rolagem.
        """
        area_visivel = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        area_visivel.fill(self.cor_fundo)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_mouse = (mouse_x - self.rect.x, mouse_y - self.rect.y)

        for componente in self.componentes:
            if hasattr(componente, "desenhar"):
                # Suporte a Painel ou componentes com .rect/.texto_rect
                if hasattr(componente, "rect"):
                    y_original = componente.rect.y
                    componente.rect.y = y_original - self.scroll_y
                    if hasattr(componente, "texto_rect"):
                        componente.texto_rect.centery = componente.rect.centery
                    if -componente.rect.height <= componente.rect.y <= self.rect.height:
                        componente.desenhar(area_visivel, mouse_pos=rel_mouse)
                    componente.rect.y = y_original
                elif hasattr(componente, "texto_rect"):
                    y_original = componente.texto_rect.y
                    componente.texto_rect.y = y_original - self.scroll_y
                    if -50 <= componente.texto_rect.y <= self.rect.height:
                        componente.desenhar(area_visivel)
                    componente.texto_rect.y = y_original
                elif hasattr(componente, "componentes"):
                    # Suporte a Painel: desenha todos os filhos
                    for sub in componente.componentes:
                        if hasattr(sub, "desenhar"):
                            sub.desenhar(area_visivel)

        # Desenha barra de rolagem
        if self.altura_conteudo > self.rect.height:
            proporcao = self.rect.height / self.altura_conteudo
            altura_barra = int(self.rect.height * proporcao)
            y_barra = int((self.scroll_y / self.altura_conteudo) * self.rect.height)
            pygame.draw.rect(area_visivel, self.cor_barra, (self.rect.width - self.largura_barra, y_barra, self.largura_barra, altura_barra))

        tela.blit(area_visivel, self.rect.topleft)


class Paginador:
    """
    Área paginada para exibir listas longas de componentes ou páginas (Painel).

    Parâmetros:
    -----------
    - x, y (int): Posição do canto superior esquerdo.
    - largura, altura (int): Tamanho da área visível.
    - itens_por_pagina (int): Quantos componentes aparecem por página.
    - texto_anterior (str): Texto do botão anterior (default: "< Anterior").
    - texto_proxima (str): Texto do botão próxima (default: "Próxima >").
    - estilo_btn (dict): Dicionário com parâmetros extras para os botões (cor, fonte, etc).

    Personalização:
    ---------------
    - Altere texto_anterior/texto_proxima para mudar o texto dos botões.
    - Use estilo_btn para customizar cor, fonte, tamanho, etc dos botões.
    - Adicione Painel, Botao, CaixaTexto, etc como páginas.

    Métodos principais:
    -------------------
    - adicionar_componente(componente): Adiciona um componente ou Painel à lista paginada.
    """
    def __init__(self, x, y, largura, altura, itens_por_pagina=1, texto_anterior="< Anterior", texto_proxima="Próxima >", estilo_btn=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.itens_por_pagina = itens_por_pagina
        self.pagina_atual = 0
        self.componentes = []

        # Personalização dos botões
        estilo_btn = estilo_btn or {}
        btn_kwargs = dict(
            cor_fundo=estilo_btn.get("cor_fundo", Cores.cinza()),
            cor_hover=estilo_btn.get("cor_hover", Cores.cinza_escuro()),
            cor_texto=estilo_btn.get("cor_texto", Cores.branco()),
            fonte=estilo_btn.get("fonte", "arial"),
            tamanho_fonte=estilo_btn.get("tamanho_fonte", 22),
            raio_borda=estilo_btn.get("raio_borda", 8)
        )

        # Botões de navegação
        self.botao_anterior = Botao(
            x, y + altura + 10, 120, 45, texto=texto_anterior, funcao=self.ir_para_anterior, **btn_kwargs
        )
        self.botao_proxima = Botao(
            x + largura - 120, y + altura + 10, 120, 45, texto=texto_proxima, funcao=self.ir_para_proxima, **btn_kwargs
        )

    def adicionar_componente(self, componente):
        """Adiciona um componente (ou Painel) à lista paginada."""
        self.componentes.append(componente)

    def ir_para_anterior(self):
        """Vai para a página anterior, se possível."""
        if self.pagina_atual > 0:
            self.pagina_atual -= 1

    def ir_para_proxima(self):
        """Vai para a próxima página, se possível."""
        max_pagina = (len(self.componentes) - 1) // self.itens_por_pagina
        if self.pagina_atual < max_pagina:
            self.pagina_atual += 1

    def desenhar(self, tela):
        """
        Desenha o componente/painel da página atual e os botões de navegação.
        """
        inicio = self.pagina_atual * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        visiveis = self.componentes[inicio:fim]

        for componente in visiveis:
            if hasattr(componente, "desenhar"):
                componente.desenhar(tela)

        self.botao_anterior.desenhar(tela)
        self.botao_proxima.desenhar(tela)

    def processar_evento(self, evento):
        """
        Processa eventos dos botões de navegação e do componente/painel da página atual.
        """
        # Só repassa o evento para o painel (ou componente) da página atual
        if self.componentes:
            pagina_atual = self.componentes[self.pagina_atual]
            if hasattr(pagina_atual, "processar_evento"):
                pagina_atual.processar_evento(evento)
        # Repasse também para os botões de navegação do paginador
        self.botao_anterior.processar_evento(evento)
        self.botao_proxima.processar_evento(evento)


class Painel:
    """
    Container para agrupar componentes em uma página do Paginador ou ScrollArea.

    Parâmetros:
    -----------
    - componentes (list): Lista de componentes visuais (Botao, CaixaTexto, TextoFormatado, etc).

    Personalização:
    ---------------
    - Adicione/remova componentes facilmente.
    - Pode ser usado como página do Paginador ou como item de ScrollArea.

    Métodos principais:
    -------------------
    - desenhar(tela): Desenha todos os componentes do painel.
    - processar_evento(evento): Repassa eventos para todos os componentes.
    """
    def __init__(self, componentes=None):
        self.componentes = componentes or []

    def adicionar_componente(self, componente):
        """Adiciona um componente ao painel."""
        self.componentes.append(componente)

    def desenhar(self, tela):
        for componente in self.componentes:
            if hasattr(componente, "desenhar"):
                componente.desenhar(tela)

    def processar_evento(self, evento):
        for componente in self.componentes:
            if hasattr(componente, "processar_evento"):
                componente.processar_evento(evento)


class Slider:
    """
    Slider (barra deslizante) para seleção de valores numéricos, ideal para controle de volume, brilho, etc.

    Como usar:
    ----------
    1. Instancie o slider:
        slider = Slider(x=100, y=200, largura=300, valor_inicial=0.5)
    2. Adicione à tela:
        tela.adicionar_componente(slider)
    3. Leia o valor selecionado:
        valor = slider.valor  # entre 0.0 e 1.0 por padrão

    Parâmetros do construtor:
    ------------------------
    - x, y (int): Posição do canto superior esquerdo.
    - largura (int): Comprimento da barra.
    - valor_inicial (float): Valor inicial do slider (entre 0.0 e 1.0).
    - cor_barra (tuple): Cor da barra de fundo.
    - cor_cursor (tuple): Cor do cursor/deslizador.
    - altura (int): Altura da barra (opcional, padrão 12).
    - raio_cursor (int): Raio do cursor (opcional, padrão 14).

    Métodos principais:
    -------------------
    - valor (float): Valor atual do slider (0.0 a 1.0).
    - desenhar(tela): Desenha o slider na tela.
    - processar_evento(evento): Processa eventos de mouse para interação.
    """

    def __init__(self, x, y, largura, valor_inicial=0.5, cor_barra=(180, 180, 180), cor_cursor=(60, 120, 255), altura=12, raio_cursor=14):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.valor = max(0.0, min(1.0, valor_inicial))
        self.cor_barra = cor_barra
        self.cor_cursor = cor_cursor
        self.raio_cursor = raio_cursor
        self.arrastando = False

    def desenhar(self, tela):
        """Desenha a barra e o cursor do slider."""
        # Barra de fundo
        barra_rect = pygame.Rect(self.x, self.y + self.altura // 2 - self.altura // 2, self.largura, self.altura)
        pygame.draw.rect(tela, self.cor_barra, barra_rect, border_radius=self.altura // 2)

        # Cursor
        cursor_x = int(self.x + self.valor * self.largura)
        cursor_y = self.y + self.altura // 2
        pygame.draw.circle(tela, self.cor_cursor, (cursor_x, cursor_y), self.raio_cursor)

        # Valor numérico (opcional, para debug)
        fonte = pygame.font.SysFont("arial", 18)
        valor_txt = fonte.render(f"{int(self.valor * 100)}%", True, (50, 50, 50))
        tela.blit(valor_txt, (self.x + self.largura + 20, self.y + self.altura // 2 - 12))

    def processar_evento(self, evento):
        """Processa eventos de mouse para arrastar o cursor."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos
            cursor_x = int(self.x + self.valor * self.largura)
            cursor_y = self.y + self.altura // 2
            # Verifica se clicou no cursor
            if (mx - cursor_x) ** 2 + (my - cursor_y) ** 2 <= self.raio_cursor ** 2:
                self.arrastando = True
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.arrastando = False
        elif evento.type == pygame.MOUSEMOTION and self.arrastando:
            mx = evento.pos[0]
            # Atualiza valor conforme posição do mouse
            novo_valor = (mx - self.x) / self.largura
            self.valor = max(0.0, min(1.0, novo_valor))


class Retangulo:
    """
    Componente gráfico de retângulo, ideal para representar raquetes ou barras verticais/horizontais.

    Como usar:
    ----------
    1. Instancie o retângulo:
        raquete = Retangulo(x=0, y=100, largura=15, altura=100, cor=Cores.verde())
    2. Adicione à tela ou use diretamente em jogos:
        raquete.desenhar(tela)

    Parâmetros:
    -----------
    - x, y (int): Posição do canto superior esquerdo.
    - largura, altura (int): Tamanho do retângulo.
    - cor (tuple): Cor de fundo (use Cores).
    - imagem (str, opcional): Caminho ou nome da imagem para desenhar por cima da cor.

    Métodos principais:
    -------------------
    - desenhar(tela): Desenha o retângulo na tela.
    - atualizar(limite_superior, limite_inferior): Move o retângulo verticalmente, respeitando limites.
    - set_dy(dy): Define a velocidade vertical.
    """
    def __init__(self, x, y, largura, altura, cor, imagem=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.imagem = None
        if imagem:
            from utilitarios.imagens import carregar_imagem
            self.imagem = carregar_imagem(imagem, (largura, altura))
        self.dy = 0  # Velocidade vertical

    def desenhar(self, tela):
        """
        Desenha o retângulo na tela.
        Sempre desenha a cor de fundo e, se existir, uma imagem por cima.
        """
        rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(tela, self.cor, rect, border_radius=8)
        if self.imagem:
            tela.blit(self.imagem, rect)
        pygame.draw.rect(tela, (0, 0, 0), rect, 2, border_radius=8)  # Borda preta

    def atualizar(self, limite_superior, limite_inferior):
        """
        Move o retângulo verticalmente, impedindo que ultrapasse os limites da tela.
        """
        self.y += self.dy
        self.y = max(limite_superior, min(limite_inferior - self.altura, self.y))

    def set_dy(self, dy):
        """
        Define a velocidade vertical do retângulo.
        """
        self.dy = dy

class Circulo:
    """
    Componente gráfico de círculo, ideal para representar bolas ou elementos circulares.

    Como usar:
    ----------
    1. Instancie o círculo:
        bola = Circulo(x=300, y=200, raio=12, cor=Cores.amarelo_ouro())
    2. Adicione à tela ou use diretamente em jogos:
        bola.desenhar(tela)

    Parâmetros:
    -----------
    - x, y (int): Centro do círculo.
    - raio (int): Raio do círculo.
    - cor (tuple): Cor de fundo (use Cores).
    - imagem (str, opcional): Caminho ou nome da imagem para desenhar por cima da cor.

    Métodos principais:
    -------------------
    - desenhar(tela): Desenha o círculo na tela, com máscara para não ultrapassar o formato.
    - atualizar(): Move o círculo conforme sua velocidade.
    - set_direcao(dx, dy): Define a velocidade horizontal e vertical.
    """
    def __init__(self, x, y, raio, cor, imagem=None):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.imagem = None
        if imagem:
            from utilitarios.imagens import carregar_imagem
            self.imagem = carregar_imagem(imagem, (raio*2, raio*2))
        self.dx = 0  # Velocidade horizontal
        self.dy = 0  # Velocidade vertical

    def desenhar(self, tela):
        """
        Desenha o círculo na tela.
        Sempre desenha a cor de fundo e, se existir, uma imagem por cima (recortada para não ultrapassar o círculo).
        """
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        if self.imagem:
            # Cria uma superfície temporária com canal alpha
            temp = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
            temp.blit(self.imagem, (0, 0))
            # Máscara circular para "overflow: hidden"
            mask = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255,255,255,255), (self.raio, self.raio), self.raio)
            temp.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            tela.blit(temp, (int(self.x)-self.raio, int(self.y)-self.raio))
        pygame.draw.circle(tela, (0, 0, 0), (int(self.x), int(self.y)), self.raio, 2)  # Borda preta

    def atualizar(self):
        """
        Move o círculo conforme sua velocidade.
        """
        self.x += self.dx
        self.y += self.dy

    def set_direcao(self, dx, dy):
        """
        Define a velocidade horizontal (dx) e vertical (dy) do círculo.
        """
        self.dx = dx
        self.dy = dy
