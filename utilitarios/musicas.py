import pygame
from pathlib import Path
from databases.musica_anterior import MusicaAnterior

CAMINHO = Path(__file__).parent.parent / 'musicas'

# Dicionários de caminhos para efeitos e músicas de fundo
efeitos = {
    'clique': str(CAMINHO / "efeitos" / "clique.wav"),
    'empate': str(CAMINHO / "efeitos" / "empate.wav"),
    'vitoria': str(CAMINHO / "efeitos" / "vitoria.wav"),
    'coins': str(CAMINHO / "efeitos" / "coins.wav"),
    'correto': str(CAMINHO / "efeitos" / "correto.wav"),
    'incorreto': str(CAMINHO / "efeitos" / "incorreto.wav"),
    'fim': str(CAMINHO / "efeitos" / "fim.wav"),
    'venceu': str(CAMINHO / "efeitos" / "venceu.wav"),
    'perdeu': str(CAMINHO / "efeitos" / "perdeu.wav"),
    'sair': str(CAMINHO / "efeitos" / "sair.wav"),
}

class Efeitos:
    """"
    *** Classe utilitária para controle de efeitos sonoros.***
    ----
    *opcoes de efeitos sonoros disponíveis:*
    - coins
    - correto
    - incorreto
    - fim
    - venceu
    - perdeu
    - sair
    ----
    *exemplo chamada:*
    Efeitos.coins()
    """
    @staticmethod
    def clique():
        return 'clique'
    
    @staticmethod
    def empate():
        return 'empate'
    
    @staticmethod
    def vitoria():
        return 'vitoria'
    
    @staticmethod
    def coins():
        return 'coins'
    
    @staticmethod
    def correto():
        return 'correto'
    
    @staticmethod
    def incorreto():
        return 'incorreto'
    
    @staticmethod
    def fim():
        return 'fim'
    
    @staticmethod
    def venceu():
        return 'venceu'
    
    @staticmethod
    def perdeu():
        return 'perdeu'
    
    @staticmethod
    def sair():
        return 'sair'

fundos = {
    'menu': str(CAMINHO / "fundos" / "menu.mp3"),
    'jogo': str(CAMINHO / "fundos" / "jogo.mp3"),
    'vitoria': str(CAMINHO / "fundos" / "vitoria.mp3"),
    'derrota': str(CAMINHO / "fundos" / "derrota.mp3"),
    'musica_fundo': str(CAMINHO / "fundos" / "musica_fundo.mp3"),
    "tetris": CAMINHO / "fundos" / "tetris.mp3",
    "flappy": CAMINHO / "fundos" / "flappy.mp3",
    "snake": CAMINHO / "fundos" / "snake.mp3",
}

class Fundos:
    """
    *** Classe utilitária para controle de músicas de fundo.***
    ----
    *opcoes de músicas de fundo disponíveis:*
    - menu
    - jogo
    - vitoria
    - derrota
    ----
    *exemplo chamada:*
    Fundos.menu()
    """
    @staticmethod
    def menu():
        return 'menu'
    
    @staticmethod
    def jogo():
        return 'jogo'
    
    @staticmethod
    def vitoria():
        return 'vitoria'
    
    @staticmethod
    def derrota():
        return 'derrota'
    
    @staticmethod
    def musica_fundo():
        return 'musica_fundo'
    
    @staticmethod
    def tetris():
        return 'tetris'

    @staticmethod
    def snake():
        return 'snake'
    
    @staticmethod
    def flappy():
        return 'flappy'

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

    musica_atual_nome = None  # Adicione este atributo de classe

    @staticmethod
    def tocar_fundo(nome: str, volume: float = 0.5, loop: bool = True, teste=False):
        """Toca uma música de fundo pelo nome do dicionário 'fundos'."""
        if not teste:
            if Musicas.musica_atual_nome == nome and Musicas.esta_tocando():
                return  # Já está tocando essa música
        caminho = fundos.get(nome)
        if not caminho:
            print(f"Música de fundo '{nome}' não encontrada.")
            return
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play(0)
            Musicas.musica_atual_nome = nome
            print(f"Música de fundo '{nome}' iniciada.")
        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")

    @staticmethod
    def esta_tocando():
        """Verifica se a música de fundo está tocando."""
        return pygame.mixer.music.get_busy()

    @staticmethod
    def parar_fundo():
        """Para a música de fundo."""
        pygame.mixer.music.stop()
        Musicas.musica_atual_nome = None
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

    @staticmethod
    def musica_atual():
        return Musicas.musica_atual_nome
    
    @staticmethod
    def salvar_musica_anterior():
        """Salva a música anterior no banco de dados."""
        musica_atual = Musicas.musica_atual()
        if musica_atual:
            MusicaAnterior.set_musica_anterior(musica_atual)
        else:
            MusicaAnterior.set_musica_anterior(None)
        print(f"Música '{musica_atual}' salva como anterior.")

# Exemplo de uso:
# Musicas.tocar_fundo('menu')
# Musicas.tocar_efeito('coins')
# Musicas.parar_fundo()