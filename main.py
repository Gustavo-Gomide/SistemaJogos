# NAVEGADOR DE TELAS PARA O JOGO
# Importa as classes necessárias para o navegador de telas
from navegador import Navegador

# Importa as telas do sistema 
from telas.gerais.tela_menu import TelaMenu
from telas.gerais.cadastro_login_interface import TelaLoginCadastro
from telas.gerais.tela_musicas import TelaMusicas
from telas.gerais.tela_configuracoes import TelaConfiguracoes
from telas.gerais.tela_rank_global import TelaRankGlobal

# Importa as telas dos jogos
# Importa as telas do PongPong
from telas.jogo_pongpong.jogo_PongPong import TelaJogoPongPong
from telas.jogo_pongpong.menu_PongPong import TelaMenuPongPong
from telas.jogo_pongpong.config_PongPong import TelaConfigPongPong
from telas.jogo_pongpong.selecao_jogadores import TelaSelecaoJogadores
from telas.jogo_pongpong.rank_PongPong import TelaRankPongPong
from telas.jogo_pongpong.historico_PongPong import TelaHistoricoPongPong

# Importa as telas do Jogo da Velha
from telas.jogo_velha.jogo_da_velha import MenuJogoDaVelhaTela, JogoDaVelhaTela, HistoricoVelhaTela
from telas.jogo_velha.selecao_jogadores import TelaSelecaoJogadoresVelha

# Importa as telas do Jogo Dino
from telas.jogo_dino.jogo_dino import TelaJogoDino
from telas.jogo_dino.menu_dino import TelaMenuDino
from telas.jogo_dino.rank_dino import TelaRankDino
from telas.jogo_dino.historico_dino import TelaHistoricoDino

# Importa as telas do Jogo Tetris
from telas.jogo_tetris.tetris import TelaJogoTetris
from telas.jogo_tetris.menu_tetris import TelaMenuTetris
from telas.jogo_tetris.rank_tetris import TelaRankTetris
from telas.jogo_tetris.historico_tetris import TelaHistoricoTetris

# Importa as telas do Jogo Flappy Bird
from telas.jogo_flappy_bird.jogo_flappy_bird import TelaJogoFlappy
from telas.jogo_flappy_bird.menu_flappy_bird import TelaMenuFlappy
from telas.jogo_flappy_bird.rank_flappy_bird import TelaRankFlappy
from telas.jogo_flappy_bird.historico_flappy_bird import TelaHistoricoFlappy

# Importa as telas do Jogo Snake
from telas.jogo_snake.snake import TelaJogoSnake
from telas.jogo_snake.menu_Snake import TelaMenuSnake
from telas.jogo_snake.rank_Snake import TelaRankSnake
from telas.jogo_snake.historico_Snake import TelaHistoricoSnake

# Importa as telas do Jogo Forca
from telas.jogo_forca.forca import TelaJogoForca
from telas.jogo_forca.forca_menu import TelaMenuForca
from telas.jogo_forca.forca_rank import TelaRankForca
from telas.jogo_forca.forca_historico import TelaHistoricoForca

# Importa as telas do sistema bancário
from telas.sistema_banco.tela_login import TelaLogin
from telas.sistema_banco.tela_registro import TelaRegistro
from telas.sistema_banco.tela_menu_banco import TelaMenuBanco
from telas.sistema_banco.tela_saldo import TelaSaldo
from telas.sistema_banco.tela_deposito import TelaDeposito
from telas.sistema_banco.tela_saque import TelaSaque
from telas.sistema_banco.tela_pix import TelaPix

# Importa funções para criar o banco de dados e tabelas
from databases.musica_anterior import MusicaAnterior # Musica Anterior é uma classe que gerencia a música anterior tocada no menu
from utilitarios.Aprincipal_database import BancoDados # Classe base para operações com banco de dados MySQL
from databases.cadastro_database import DadosUsuario # Classe para gerenciar usuários no banco de dados
from databases.PongPong_database import PongPongDB # Classe para gerenciar partidas do PongPong
from databases.velha_database import BancoDadosVelha # Classe para gerenciar o jogo da velha no banco de dados
from databases.dino_database import DinoDB # Classe para gerenciar o jogo Dino no banco de dados
from databases.tetris_database import TetrisDB # Classe para gerenciar o jogo Tetris no banco de dados
from databases.flappy_database import FlappyDB # Classe para gerenciar o jogo Flappy Bird no banco de dados
from databases.Snake_database import SnakeDB # Classe para gerenciar o jogo Snake no banco de dados
from databases.forca_database import ForcaDB # Classe para gerenciar o jogo Forca no banco de dados
from databases.sistema_banco import SistemaBanco # Classe para gerenciar o sistema bancário

# configurações banco de dados
BancoDados.configurar_conexao(
    host="localhost",
    user="root",  # Your MySQL username
    password="81472529",  # Your MySQL password
    database="jogos"  # Nome do banco de dados que será criado
)

# Cria o banco de dados e as tabelas necessárias
# (adicione outras funções aqui se criar mais tabelas no futuro)
BancoDados.criar_database() # Cria o banco de dados 'jogos' se não existir
MusicaAnterior.criar_tabela_musica_anterior() # Cria a tabela para armazenar a música anterior tocada no menu
DadosUsuario.criar_tabela_usuarios() # Cria a tabela de usuários no banco de dados
PongPongDB.criar_tabela_pong() # Cria a tabela de partidas do PongPong
BancoDadosVelha.criar_tabela() # Cria a tabela de resultados do Jogo da Velha
BancoDadosVelha.criar_tabela_historico() # Cria a tabela de histórico de partidas do Jogo da Velha
DinoDB.criar_tabela() # Cria a tabela de resultados do Jogo Dino
TetrisDB.criar_tabela() # Cria a tabela de resultados do Jogo Tetris
FlappyDB.criar_tabela() # Cria a tabela de resultados do Jogo Flappy Bird
SnakeDB.criar_tabela() # Cria a tabela de resultados do Jogo Snake
ForcaDB.criar_tabela() # Cria a tabela de resultados do Jogo Forca
SistemaBanco.criar_tabelas_banco()  # Cria as tabelas do sistema bancário

# Instancia o navegador, responsável por gerenciar as telas
navegador = Navegador()

# Registra as telas disponíveis no sistema
# O nome é a chave usada para navegar entre elas
navegador.registrar_tela("menu", TelaMenu) # Tela do menu principal do sistema
navegador.registrar_tela("cadastro", TelaLoginCadastro) # Tela de login e cadastro de usuários
navegador.registrar_tela("musicas", TelaMusicas) # Tela para gerenciar músicas de fundo
navegador.registrar_tela("configurações", TelaConfiguracoes) # Tela de configurações do sistema
navegador.registrar_tela("ranking global", TelaRankGlobal) # Tela de ranking global dos jogos

# Registra as telas do Jogo da Velha
navegador.registrar_tela("menu jogo-da-velha", lambda nav: MenuJogoDaVelhaTela(nav)) 
navegador.registrar_tela("selecao jogadores velha", lambda nav: TelaSelecaoJogadoresVelha(nav)) 
navegador.registrar_tela("jogo da velha", lambda nav: JogoDaVelhaTela(nav, banco=BancoDadosVelha))
navegador.registrar_tela("historico velha", lambda nav: HistoricoVelhaTela(nav, banco=BancoDadosVelha))

# Registra as telas do PongPong
navegador.registrar_tela("menu pong-pong", TelaMenuPongPong)
navegador.registrar_tela("jogo pong-pong", TelaJogoPongPong)
navegador.registrar_tela("configurações pong-pong", lambda nav, editar=None: TelaConfigPongPong(nav, editar))
navegador.registrar_tela("selecao jogadores pong-pong", TelaSelecaoJogadores) 
navegador.registrar_tela("ranking pong-pong", TelaRankPongPong)
navegador.registrar_tela("historico pong-pong", TelaHistoricoPongPong)

# Registra as telas do Jogo Dino
navegador.registrar_tela("menu dino", TelaMenuDino)
navegador.registrar_tela("jogo dino", TelaJogoDino)
navegador.registrar_tela("ranking dino", TelaRankDino)
navegador.registrar_tela("historico dino", TelaHistoricoDino)

# Registra as telas do Jogo Tetris
navegador.registrar_tela("menu tetris", TelaMenuTetris)
navegador.registrar_tela("jogo tetris", TelaJogoTetris)
navegador.registrar_tela("ranking tetris", TelaRankTetris)
navegador.registrar_tela("historico tetris", TelaHistoricoTetris)

# Registra as telas do Jogo Flappy Bird
navegador.registrar_tela("menu flappy", TelaMenuFlappy)
navegador.registrar_tela("jogo flappy", TelaJogoFlappy)
navegador.registrar_tela("ranking flappy", TelaRankFlappy)
navegador.registrar_tela("historico flappy", TelaHistoricoFlappy)

# Registra as telas do Jogo Snake
navegador.registrar_tela("menu snake", TelaMenuSnake)
navegador.registrar_tela("jogo snake", TelaJogoSnake)
navegador.registrar_tela("ranking snake", TelaRankSnake)
navegador.registrar_tela("historico snake", TelaHistoricoSnake)

# Registra as telas do Jogo Forca
navegador.registrar_tela("menu forca", TelaMenuForca)
navegador.registrar_tela("jogo forca", TelaJogoForca)
navegador.registrar_tela("ranking forca", TelaRankForca)
navegador.registrar_tela("historico forca", TelaHistoricoForca)

# Registro das telas do sistema bancário
navegador.registrar_tela("login_banco", TelaLogin)
navegador.registrar_tela("registro_banco", TelaRegistro)
navegador.registrar_tela("menu_banco", TelaMenuBanco)
navegador.registrar_tela("saldo_banco", TelaSaldo)
navegador.registrar_tela("deposito_banco", TelaDeposito)
navegador.registrar_tela("saque_banco", TelaSaque)
navegador.registrar_tela("pix_banco", TelaPix)

#navegador.ir_para("login")

# (adicione outras telas aqui se criar mais jogos ou funcionalidades...)

# Toca a música padrão do menu e salva como anterior
from utilitarios.musicas import Musicas
MUSICA_PADRAO = "menu" # Nome da música padrão do menu principal
# Verifica se a música padrão já está tocando, se não, toca a música de fundo
if not Musicas.esta_tocando():
    Musicas.tocar_fundo(MUSICA_PADRAO, navegador.volume_fundo)
# Salva a música padrão como a anterior
MusicaAnterior.set_musica_anterior(MUSICA_PADRAO)

# Inicia o sistema exibindo a tela do menu principal
navegador.ir_para("menu")
