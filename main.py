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

# Importa funções para criar o banco de dados e tabelas
from databases.cadastro_database import DadosUsuario
from utilitarios.Aprincipal_database import BancoDados

# Inicializa o pygame (necessário para qualquer aplicação gráfica)

# Cria o banco de dados e as tabelas necessárias
# (adicione outras funções aqui se criar mais tabelas no futuro)
BancoDados.criar_database()
DadosUsuario.criar_tabela_usuarios()

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
# (adicione outras telas aqui se criar mais jogos ou funcionalidades)

# Inicia o sistema exibindo a tela do menu principal
navegador.ir_para("menu")
