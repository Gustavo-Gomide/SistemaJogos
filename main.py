from flask.config import T
import pygame
from navegador import Navegador
from utilitarios.Aprincipal_widgets import Cores
from telas.tela_menu import TelaMenu
from telas.cadastro_login_interface import TelaLoginCadastro
from telas.tela_musicas import TelaMusicas
from telas.tela_configuracoes import TelaConfiguracoes

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

# Inicia o sistema exibindo a tela do menu principal
navegador.ir_para("menu")
