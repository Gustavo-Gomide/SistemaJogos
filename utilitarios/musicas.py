import pygame
from pathlib import Path

CAMINHO = Path(__file__).parent.parent / 'musicas'

# Dicionários de caminhos para efeitos e músicas de fundo
efeitos = {
    'coins': str(CAMINHO / "efeitos" / "coins.wav"),
    'correto': str(CAMINHO / "efeitos" / "correto.wav"),
    'incorreto': str(CAMINHO / "efeitos" / "incorreto.wav"),
    'fim': str(CAMINHO / "efeitos" / "fim.wav"),
    'venceu': str(CAMINHO / "efeitos" / "venceu.wav"),
    'perdeu': str(CAMINHO / "efeitos" / "perdeu.wav"),
    'sair': str(CAMINHO / "efeitos" / "sair.wav")
}

fundos = {
    'menu': str(CAMINHO / "fundos" / "menu.mp3"),
    'jogo': str(CAMINHO / "fundos" / "jogo.mp3"),
    'vitoria': str(CAMINHO / "fundos" / "vitoria.mp3"),
    'derrota': str(CAMINHO / "fundos" / "derrota.mp3")
}

class Musicas:
    """
    Classe utilitária para controle de músicas de fundo e efeitos sonoros.

    Métodos:
    --------
    - tocar_fundo(nome, volume=0.5): Toca uma música de fundo em loop.
    - parar_fundo(): Para a música de fundo.
    - pausar_fundo(): Pausa a música de fundo.
    - retomar_fundo(): Retoma a música de fundo pausada.
    - tocar_efeito(nome, volume=0.7): Toca um efeito sonoro sem interromper a música de fundo.
    """

    @staticmethod
    def tocar_fundo(nome: str, volume: float = 0.5):
        """Toca uma música de fundo pelo nome do dicionário 'fundos'."""
        caminho = fundos.get(nome)
        if not caminho:
            print(f"Música de fundo '{nome}' não encontrada.")
            return
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            print(f"Música de fundo '{nome}' iniciada.")
        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")

    @staticmethod
    def parar_fundo():
        """Para a música de fundo."""
        pygame.mixer.music.stop()
        print("Música de fundo parada.")

    @staticmethod
    def pausar_fundo():
        """Pausa a música de fundo."""
        pygame.mixer.music.pause()
        print("Música de fundo pausada.")

    @staticmethod
    def retomar_fundo():
        """Retoma a música de fundo."""
        pygame.mixer.music.unpause()
        print("Música de fundo retomada.")

    @staticmethod
    def tocar_efeito(nome: str, volume: float = 0.7):
        """Toca um efeito sonoro pelo nome do dicionário 'efeitos'."""
        caminho = efeitos.get(nome)
        if not caminho:
            print(f"Efeito sonoro '{nome}' não encontrado.")
            return
        canal_efeitos = pygame.mixer.Channel(1)
        try:
            som = pygame.mixer.Sound(caminho)
            som.set_volume(volume)
            canal_efeitos.play(som)
            print(f"Efeito sonoro '{nome}' tocado.")
        except Exception as e:
            print(f"Erro ao carregar efeito sonoro: {caminho} ({e})")

# Exemplo de uso:
# Musicas.tocar_fundo('menu')
# Musicas.tocar_efeito('coins')
# Musicas.parar_fundo()