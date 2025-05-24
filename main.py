from navegador import Navegador

from telas.gerais.tela_menu import TelaMenu
from telas.gerais.cadastro_login_interface import TelaLoginCadastro
from telas.gerais.tela_musicas import TelaMusicas
from telas.gerais.tela_configuracoes import TelaConfiguracoes
from telas.gerais.tela_rank_global import TelaRankGlobal

from telas.jogo_pongpong.jogo_PongPong import TelaJogoPongPong
from telas.jogo_pongpong.menu_PongPong import TelaMenuPongPong
from telas.jogo_pongpong.config_PongPong import TelaConfigPongPong
from telas.jogo_pongpong.selecao_jogadores import TelaSelecaoJogadores  # Importa a tela de seleção de jogadores
from telas.jogo_pongpong.rank_PongPong import TelaRankPongPong
from telas.jogo_pongpong.historico_PongPong import TelaHistoricoPongPong

from telas.jogo_velha.jogo_da_velha import MenuJogoDaVelhaTela, JogoDaVelhaTela, HistoricoVelhaTela
from telas.jogo_velha.selecao_jogadores import TelaSelecaoJogadoresVelha

from telas.jogo_dino.jogo_dino import TelaJogoDino
from telas.jogo_dino.menu_dino import TelaMenuDino
from telas.jogo_dino.rank_dino import TelaRankDino
from telas.jogo_dino.historico_dino import TelaHistoricoDino

from telas.jogo_tetris.tetris import TelaJogoTetris
from telas.jogo_tetris.menu_tetris import TelaMenuTetris
from telas.jogo_tetris.rank_tetris import TelaRankTetris
from telas.jogo_tetris.historico_tetris import TelaHistoricoTetris


from telas.jogo_flappy_bird.jogo_flappy_bird import TelaJogoFlappy
from telas.jogo_flappy_bird.menu_flappy_bird import TelaMenuFlappy
from telas.jogo_flappy_bird.rank_flappy_bird import TelaRankFlappy
from telas.jogo_flappy_bird.historico_flappy_bird import TelaHistoricoFlappy


from telas.jogo_snake.snake import TelaJogoSnake
from telas.jogo_snake.menu_Snake import TelaMenuSnake
from telas.jogo_snake.rank_Snake import TelaRankSnake
from telas.jogo_snake.historico_Snake import TelaHistoricoSnake


# Importa funções para criar o banco de dados e tabelas
from databases.musica_anterior import MusicaAnterior
from utilitarios.Aprincipal_database import BancoDados
from databases.cadastro_database import DadosUsuario
from databases.PongPong_database import PongPongDB
from databases.velha_database import BancoDadosVelha
from databases.dino_database import DinoDB
from databases.tetris_database import TetrisDB
from databases.flappy_database import FlappyDB
from databases.Snake_database import SnakeDB


# configurações banco de dados
BancoDados.configurar_conexao(
    host="localhost",
    user= "root",
    password= "",
    database= "jogos"
)

# Cria o banco de dados e as tabelas necessárias
# (adicione outras funções aqui se criar mais tabelas no futuro)
MusicaAnterior.criar_tabela_musica_anterior()
BancoDados.criar_database()
DadosUsuario.criar_tabela_usuarios()
PongPongDB.criar_tabela_pong()
BancoDadosVelha.criar_tabela()
BancoDadosVelha.criar_tabela_historico()
DinoDB.criar_tabela()
TetrisDB.criar_tabela()
FlappyDB.criar_tabela()
SnakeDB.criar_tabela()

# Instancia o navegador, responsável por gerenciar as telas
navegador = Navegador()

# Registra as telas disponíveis no sistema
# O nome é a chave usada para navegar entre elas
navegador.registrar_tela("menu", TelaMenu)
navegador.registrar_tela("cadastro", TelaLoginCadastro)
navegador.registrar_tela("musicas", TelaMusicas)
navegador.registrar_tela("configurações", TelaConfiguracoes)
navegador.registrar_tela("ranking global", TelaRankGlobal)

navegador.registrar_tela("menu jogo-da-velha", lambda nav: MenuJogoDaVelhaTela(nav))
navegador.registrar_tela("selecao jogadores velha", lambda nav: TelaSelecaoJogadoresVelha(nav))
navegador.registrar_tela("jogo da velha", lambda nav: JogoDaVelhaTela(nav, banco=BancoDadosVelha))
navegador.registrar_tela("historico velha", lambda nav: HistoricoVelhaTela(nav, banco=BancoDadosVelha))

navegador.registrar_tela("menu pong-pong", TelaMenuPongPong)
navegador.registrar_tela("jogo pong-pong", TelaJogoPongPong)
navegador.registrar_tela("configurações pong-pong", lambda nav, editar=None: TelaConfigPongPong(nav, editar))
navegador.registrar_tela("selecao jogadores pong-pong", TelaSelecaoJogadores)  # Registra a tela de seleção de jogadores
navegador.registrar_tela("ranking pong-pong", TelaRankPongPong)
navegador.registrar_tela("historico pong-pong", TelaHistoricoPongPong)

navegador.registrar_tela("menu dino", TelaMenuDino)
navegador.registrar_tela("jogo dino", TelaJogoDino)
navegador.registrar_tela("ranking dino", TelaRankDino)
navegador.registrar_tela("historico dino", TelaHistoricoDino)

navegador.registrar_tela("menu tetris", TelaMenuTetris)
navegador.registrar_tela("jogo tetris", TelaJogoTetris)
navegador.registrar_tela("ranking tetris", TelaRankTetris)
navegador.registrar_tela("historico tetris", TelaHistoricoTetris)

navegador.registrar_tela("menu flappy", TelaMenuFlappy)
navegador.registrar_tela("jogo flappy", TelaJogoFlappy)
navegador.registrar_tela("ranking flappy", TelaRankFlappy)
navegador.registrar_tela("historico flappy", TelaHistoricoFlappy)

navegador.registrar_tela("menu snake", TelaMenuSnake)
navegador.registrar_tela("jogo snake", TelaJogoSnake)
navegador.registrar_tela("ranking snake", TelaRankSnake)
navegador.registrar_tela("historico snake", TelaHistoricoSnake)
# (adicione outras telas aqui se criar mais jogos ou funcionalidades)

# Toca a música padrão do menu e salva como anterior
from utilitarios.musicas import Musicas
MUSICA_PADRAO = "menu"
if not Musicas.esta_tocando():
    Musicas.tocar_fundo(MUSICA_PADRAO, navegador.volume_fundo)
MusicaAnterior.set_musica_anterior(MUSICA_PADRAO)

# Inicia o sistema exibindo a tela do menu principal
navegador.ir_para("menu")
