import pygame
from pathlib import Path

CAMINHO = Path(__file__).parent.parent / 'imagens'

# Dicionário único para todas as imagens do projeto
imagens = {
    'geminiai': str(CAMINHO / "geminiai.jpg"),
    'imagem': str(CAMINHO / "imagem.jpg"),
    'imagem2': str(CAMINHO / "imagem2.jpg"),
    'love': str(CAMINHO / "love.jpg"),
    'mulher_cod': str(CAMINHO / "mulher_cod.jpg")
}

_imagem_cache = {}

class Imagem:
    """
    Componente visual para exibir imagens otimizadas com cache.

    Parâmetros:
    -----------
    - nome (str): Chave da imagem no dicionário 'imagens'.
    - x, y (int): Posição da imagem na tela.
    - largura, altura (int, opcional): Tamanho para redimensionar a imagem.
    - centralizado (bool): Se True, centraliza a imagem no ponto (x, y).

    Métodos:
    --------
    - desenhar(tela): Desenha a imagem na tela.
    """

    def __init__(self, nome, x, y, largura=None, altura=None, centralizado=False):
        self.nome = nome
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.centralizado = centralizado
        self.imagem = self._carregar_imagem()

    def _carregar_imagem(self):
        """
        Carrega a imagem do disco (com cache) e redimensiona se necessário.
        """
        caminho = imagens[self.nome]
        print(f"Tentando carregar imagem: {caminho}")
        try:
            if caminho in _imagem_cache:
                img = _imagem_cache[caminho]
            else:
                img = pygame.image.load(caminho).convert_alpha()
                _imagem_cache[caminho] = img
            if self.largura and self.altura:
                img = pygame.transform.scale(img, (self.largura, self.altura))
            return img
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho}: {e}")
            return pygame.Surface((self.largura or 50, self.altura or 50))  # Imagem vazia

    def desenhar(self, tela):
        """
        Desenha a imagem na tela na posição (x, y).
        Se centralizado=True, centraliza a imagem nesse ponto.
        """
        rect = self.imagem.get_rect()
        if self.centralizado:
            rect.center = (self.x, self.y)
        else:
            rect.topleft = (self.x, self.y)
        tela.blit(self.imagem, rect)

def carregar_imagem(nome, tamanho=None):
    """
    Carrega uma imagem do dicionário 'imagens' pelo nome.
    Se tamanho for informado, redimensiona.
    Retorna um Surface do pygame.
    """
    from utilitarios.imagens import imagens  # Importa o dicionário de imagens
    caminho = imagens.get(nome)
    if not caminho:
        print(f"Imagem '{nome}' não encontrada.")
        return pygame.Surface(tamanho or (50, 50))
    try:
        img = pygame.image.load(caminho).convert_alpha()
        if tamanho:
            img = pygame.transform.scale(img, tamanho)
        return img
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho}: {e}")
        return pygame.Surface(tamanho or (50, 50))