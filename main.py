import pygame
from navegador import Navegador
from utilitarios.Aprincipal_widgets import Cores
from telas.gerais.tela_menu import TelaMenu
from telas.gerais.cadastro_login_interface import TelaLoginCadastro
from telas.gerais.tela_musicas import TelaMusicas
from telas.gerais.tela_configuracoes import TelaConfiguracoes
from telas.jogo_pongpong.jogo_PongPong import TelaJogoPongPong
from telas.jogo_pongpong.menu_PongPong import TelaMenuPongPong
from telas.jogo_pongpong.config_PongPong import TelaConfigPongPong
from telas.jogo_pongpong.selecao_jogadores import TelaSelecaoJogadores  # Importa a tela de seleção de jogadores
from telas.jogo_pongpong.rank_PongPong import TelaRankPongPong
from telas.jogo_pongpong.historico_PongPong import TelaHistoricoPongPong

# Importa funções para criar o banco de dados e tabelas
from utilitarios.Aprincipal_database import BancoDados
from databases.cadastro_database import DadosUsuario
from databases.PongPong_database import PongPongDB

# Inicializa o pygame (necessário para qualquer aplicação gráfica)

# Cria o banco de dados e as tabelas necessárias
# (adicione outras funções aqui se criar mais tabelas no futuro)
BancoDados.criar_database()
DadosUsuario.criar_tabela_usuarios()
PongPongDB.criar_tabela_pong()

# Instancia o navegador, responsável por gerenciar as telas
navegador = Navegador()

# Registra as telas disponíveis no sistema
# O nome é a chave usada para navegar entre elas
navegador.registrar_tela("menu", TelaMenu)
navegador.registrar_tela("cadastro", TelaLoginCadastro)
navegador.registrar_tela("musicas", TelaMusicas)
navegador.registrar_tela("configurações", TelaConfiguracoes)
navegador.registrar_tela("menu pong-pong", TelaMenuPongPong)
navegador.registrar_tela("jogo pong-pong", TelaJogoPongPong)
navegador.registrar_tela("configurações pong-pong", lambda nav, editar=None: TelaConfigPongPong(nav, editar))
navegador.registrar_tela("selecao jogadores pong-pong", TelaSelecaoJogadores)  # Registra a tela de seleção de jogadores
navegador.registrar_tela("ranking pong-pong", TelaRankPongPong)
navegador.registrar_tela("historico pong-pong", TelaHistoricoPongPong)
# (adicione outras telas aqui se criar mais jogos ou funcionalidades)

# Inicia o sistema exibindo a tela do menu principal
navegador.ir_para("menu")
