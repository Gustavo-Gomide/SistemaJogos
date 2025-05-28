import pygame
import sys

# --- IMPORTAÇÃO REAL DO SEU BACKEND ---
try:
    from banco_completo import (
        login_cliente, registrar_cliente, criar_conta_bancaria,
        consultar_saldo, realizar_deposito, realizar_saque,
        cadastrar_chave_pix, realizar_pix, extrato,
        pagar_jogo, receber_premio_jogo,
        executar_query  # Para buscar contas e nome do cliente
    )

    BACKEND_DISPONIVEL = True
    print("Backend 'banco_completo.py' importado com sucesso!")
except ImportError as e:
    print(f"ERRO: Não foi possível importar 'banco_completo.py'. Detalhe: {e}")
    print("Funcionalidades do banco estarão SIMULADAS.")
    BACKEND_DISPONIVEL = False


    # Funções de simulação (adapte conforme necessário se o backend não carregar)
    def login_cliente(cpf, senha):
        return 1 if cpf == "123" else None


    def registrar_cliente(n, c, s):
        return 99


    def criar_conta_bancaria(id_c, tipo, saldo=0):
        return 10 + id_c if id_c else None


    def consultar_saldo(id_cta):
        return 1000.00 if id_cta else None


    def realizar_deposito(id_cta, val, desc=""):
        return True


    def realizar_saque(id_cta, val, desc=""):
        return True


    def cadastrar_chave_pix(id_cta, tipo, val):
        return True


    def realizar_pix(id_orig, ch_dest, val):
        return True


    def extrato(id_cta):
        return [{"tipo_transacao": "DEPOSITO", "valor": 100, "data_transacao": "HOJE", "descricao": "Simulado"}]


    def pagar_jogo(id_cta, val, nome):
        return True


    def receber_premio_jogo(id_cta, val, nome):
        return True


    def executar_query(query, params, fetch_one=False, fetch_all=False):
        if "SELECT nome FROM Clientes" in query and fetch_one: return {"nome": "Cliente Simulado"}
        if "FROM Contas WHERE id_cliente" in query and fetch_all:
            return [
                {"id_conta": 1, "numero_conta": "001", "agencia": "001", "tipo_conta": "CORRENTE", "saldo": 1000.00},
                {"id_conta": 2, "numero_conta": "002", "agencia": "001", "tipo_conta": "POUPANCA", "saldo": 500.00}]
        return None

# --- Configurações do Pygame ---
pygame.init()
pygame.font.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (220, 220, 220)  # Fundo um pouco mais claro
CINZA_MEDIO = (180, 180, 180)
CINZA_ESCURO = (100, 100, 100)
AZUL_BOTAO = (0, 120, 255)
AZUL_HOVER = (50, 150, 255)
VERDE_SUCESSO = (0, 150, 0)
VERMELHO_ERRO = (200, 0, 0)

# Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Banco Digital Interativo")

# Fontes
FONTE_TITULO = pygame.font.SysFont("Arial", 40)  # um pouco menor
FONTE_SUBTITULO = pygame.font.SysFont("Arial", 30)
FONTE_NORMAL = pygame.font.SysFont("Arial", 24)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 18)
FONTE_MICRO = pygame.font.SysFont("Arial", 14)


# --- Classes de UI (Botao, CaixaDeEntrada - com pequenas melhorias) ---
class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_fundo=AZUL_BOTAO, cor_hover=AZUL_HOVER, cor_texto=BRANCO,
                 fonte=FONTE_NORMAL, action_id=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo_base = cor_fundo
        self.cor_fundo_atual = cor_fundo
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.fonte = fonte
        self.imagem_texto = self.fonte.render(self.texto, True, self.cor_texto)
        self.rect_texto = self.imagem_texto.get_rect(center=self.rect.center)
        self.clicado_mouse_neste_frame = False
        self.action_id = action_id  # Para identificar a ação do botão

    def desenhar(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.cor_fundo_atual = self.cor_hover
        else:
            self.cor_fundo_atual = self.cor_fundo_base

        pygame.draw.rect(surface, self.cor_fundo_atual, self.rect, border_radius=8)
        surface.blit(self.imagem_texto, self.rect_texto)

    def verificar_clique(self, evento, mouse_pos):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botão esquerdo
            if self.rect.collidepoint(mouse_pos):
                self.clicado_mouse_neste_frame = True  # Registra que foi clicado neste frame
                return True
        return False


class CaixaDeEntrada:
    def __init__(self, x, y, largura, altura, placeholder="", fonte=FONTE_NORMAL, cor_ativa=PRETO,
                 cor_inativa=CINZA_ESCURO, oculto=False, max_chars=50):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.placeholder = placeholder
        self.texto = ""
        self.fonte = fonte
        self.cor_ativa = cor_ativa
        self.cor_inativa = cor_inativa
        self.cor_atual = self.cor_inativa
        self.ativo = False
        self.oculto = oculto
        self.max_chars = max_chars
        self.cursor_visivel = False
        self.cursor_timer = 0
        self.atualizar_imagem_texto()

    def manipular_evento(self, evento):
        retorno_evento = None
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.ativo = True
                self.cor_atual = self.cor_ativa
            else:
                self.ativo = False
                self.cor_atual = self.cor_inativa
            self.atualizar_imagem_texto()

        if evento.type == pygame.KEYDOWN and self.ativo:
            if evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif evento.key == pygame.K_RETURN:
                retorno_evento = "enter"
            elif len(self.texto) < self.max_chars:
                self.texto += evento.unicode
            self.atualizar_imagem_texto()
        return retorno_evento

    def atualizar_imagem_texto(self):
        texto_display = self.texto
        cor_display = self.cor_atual

        if not self.texto and not self.ativo and self.placeholder:
            texto_display = self.placeholder
            cor_display = CINZA_MEDIO
        elif self.oculto and self.texto:
            texto_display = "•" * len(self.texto)  # Usar • em vez de *

        self.imagem_texto = self.fonte.render(texto_display, True, cor_display)

    def desenhar(self, surface):
        pygame.draw.rect(surface, BRANCO, self.rect)
        pygame.draw.rect(surface, self.cor_atual, self.rect, 2, border_radius=3)

        # Centralizar texto verticalmente
        pos_y_texto = self.rect.y + (self.rect.height - self.imagem_texto.get_height()) // 2
        surface.blit(self.imagem_texto, (self.rect.x + 8, pos_y_texto))  # Adicionado padding

        if self.ativo:  # Desenha o cursor piscando
            self.cursor_timer += 1
            if self.cursor_timer % 30 < 15:  # Pisca a cada meio segundo (assumindo 30 FPS)
                cursor_x = self.rect.x + 8 + self.imagem_texto.get_width()
                cursor_y_start = self.rect.y + 5
                cursor_y_end = self.rect.y + self.rect.height - 5
                pygame.draw.line(surface, self.cor_ativa, (cursor_x, cursor_y_start), (cursor_x, cursor_y_end), 1)

    def obter_texto(self):
        return self.texto.strip()  # Remove espaços extras ao obter

    def limpar_texto(self):
        self.texto = ""
        self.ativo = False
        self.cor_atual = self.cor_inativa
        self.atualizar_imagem_texto()


# --- Funções Auxiliares de UI ---
def desenhar_texto(surface, texto, pos, fonte, cor=PRETO, centralizado_x=False, centralizado_y=False):
    imagem_texto = fonte.render(texto, True, cor)
    rect_texto = imagem_texto.get_rect()
    if centralizado_x:
        rect_texto.centerx = pos[0]
    else:
        rect_texto.x = pos[0]
    if centralizado_y:
        rect_texto.centery = pos[1]
    else:
        rect_texto.y = pos[1]
    surface.blit(imagem_texto, rect_texto)
    return rect_texto


# --- Variáveis de Estado Global da GUI e do Aplicativo ---
rodando = True
clock = pygame.time.Clock()
estado_tela_atual = "LOGIN"
id_cliente_logado_gui = None
nome_cliente_logado_gui = ""
contas_cliente_gui = []  # Lista de dicionários das contas do cliente
id_conta_selecionada_gui = None
saldo_conta_selecionada_gui = None
extrato_gui = []  # Lista de transações para a tela de extrato

mensagem_status = ""
cor_mensagem_status = PRETO
temporizador_mensagem = 0


def definir_mensagem_status(msg, cor=PRETO, duracao=150):
    global mensagem_status, cor_mensagem_status, temporizador_mensagem
    mensagem_status = msg
    cor_mensagem_status = cor
    temporizador_mensagem = duracao


# --- Inicialização dos Elementos de UI para cada Tela ---

# LOGIN
titulo_login_txt = "Bem-Vindo ao BlackBank"
input_cpf_login = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 200, 350, 40, placeholder="CPF")
input_senha_login = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 260, 350, 40, placeholder="Senha", oculto=True)
botao_login = Botao(LARGURA_TELA // 2 - 175, 330, 160, 50, "Login")
botao_ir_registrar = Botao(LARGURA_TELA // 2 + 15, 330, 160, 50, "Registrar")

# REGISTRO
titulo_registro_txt = "Registrar Novo Cliente"
input_nome_reg = CaixaDeEntrada(LARGURA_TELA // 2 - 200, 120, 400, 40, placeholder="Nome Completo")
input_cpf_reg = CaixaDeEntrada(LARGURA_TELA // 2 - 200, 180, 400, 40, placeholder="CPF (XXX.XXX.XXX-XX)")
input_senha_reg = CaixaDeEntrada(LARGURA_TELA // 2 - 200, 240, 400, 40, placeholder="Senha", oculto=True)
input_confirma_senha_reg = CaixaDeEntrada(LARGURA_TELA // 2 - 200, 300, 400, 40, placeholder="Confirmar Senha",
                                          oculto=True)
botao_confirmar_registro = Botao(LARGURA_TELA // 2 - 100, 370, 200, 50, "Confirmar Registro")
botao_voltar_login_reg = Botao(LARGURA_TELA // 2 - 100, 440, 200, 50, "Voltar para Login")

# MENU PRINCIPAL (os botões serão criados dinamicamente ou aqui)
botao_logout = Botao(LARGURA_TELA - 160, 20, 140, 40, "Logout", CINZA_ESCURO, fonte=FONTE_PEQUENA)
botao_listar_contas = Botao(50, 150, 250, 40, "Listar/Selecionar Contas", fonte=FONTE_PEQUENA)
botao_criar_conta_nav = Botao(50, 200, 250, 40, "Criar Nova Conta", fonte=FONTE_PEQUENA)
botao_consultar_saldo_nav = Botao(50, 250, 250, 40, "Consultar Saldo", fonte=FONTE_PEQUENA)
botao_deposito_nav = Botao(50, 300, 250, 40, "Realizar Depósito", fonte=FONTE_PEQUENA)
botao_saque_nav = Botao(50, 350, 250, 40, "Realizar Saque", fonte=FONTE_PEQUENA)
# Botões da segunda coluna
x_col2 = LARGURA_TELA - 300  # Posição X para a segunda coluna de botões
botao_cad_chave_pix_nav = Botao(x_col2, 150, 250, 40, "Cadastrar Chave PIX", fonte=FONTE_PEQUENA)
botao_realizar_pix_nav = Botao(x_col2, 200, 250, 40, "Realizar PIX", fonte=FONTE_PEQUENA)
botao_pagar_jogo_nav = Botao(x_col2, 250, 250, 40, "Pagar Jogo", fonte=FONTE_PEQUENA)
botao_receber_premio_nav = Botao(x_col2, 300, 250, 40, "Receber Prêmio", fonte=FONTE_PEQUENA)
botao_extrato_nav = Botao(x_col2, 350, 250, 40, "Ver Extrato", fonte=FONTE_PEQUENA)

# TELA CRIAR CONTA
titulo_criar_conta_txt = "Criar Nova Conta Bancária"
input_tipo_conta_crt = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 200, 350, 40, placeholder="Tipo (CORRENTE/POUPANCA)")
# Saldo inicial será 0 por padrão no backend, não precisa de input aqui.
botao_confirmar_criar_conta = Botao(LARGURA_TELA // 2 - 100, 270, 200, 50, "Confirmar Criação")
botao_voltar_menu_crt = Botao(LARGURA_TELA // 2 - 100, 340, 200, 50, "Voltar ao Menu")

# TELA LISTAR/SELECIONAR CONTAS
titulo_selecionar_conta_txt = "Selecione uma Conta"
botoes_contas_gui = []  # Será preenchido dinamicamente
botao_voltar_menu_sel = Botao(LARGURA_TELA // 2 - 100, ALTURA_TELA - 80, 200, 50, "Voltar ao Menu")

# TELA DEPOSITO
titulo_deposito_txt = "Realizar Depósito"
input_valor_dep = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 200, 350, 40, placeholder="Valor do Depósito (Ex: 100.50)")
input_desc_dep = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 260, 350, 40, placeholder="Descrição (Opcional)")
botao_confirmar_dep = Botao(LARGURA_TELA // 2 - 100, 330, 200, 50, "Confirmar Depósito")
botao_voltar_menu_dep = Botao(LARGURA_TELA // 2 - 100, 400, 200, 50, "Voltar ao Menu")

# TELA SAQUE (similar ao depósito)
titulo_saque_txt = "Realizar Saque"
input_valor_saq = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 200, 350, 40, placeholder="Valor do Saque (Ex: 50.00)")
input_desc_saq = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 260, 350, 40, placeholder="Descrição (Opcional)")
botao_confirmar_saq = Botao(LARGURA_TELA // 2 - 100, 330, 200, 50, "Confirmar Saque")
botao_voltar_menu_saq = Botao(LARGURA_TELA // 2 - 100, 400, 200, 50, "Voltar ao Menu")

# TELA CADASTRO CHAVE PIX
titulo_cad_pix_txt = "Cadastrar Chave PIX"
input_tipo_chave_pix = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 180, 350, 40,
                                      placeholder="Tipo (CPF,EMAIL,TELEFONE,ALEATORIA)")
input_valor_chave_pix = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 240, 350, 40, placeholder="Valor da Chave")
botao_confirmar_cad_pix = Botao(LARGURA_TELA // 2 - 100, 310, 200, 50, "Cadastrar Chave")
botao_voltar_menu_cad_pix = Botao(LARGURA_TELA // 2 - 100, 380, 200, 50, "Voltar ao Menu")

# TELA REALIZAR PIX
titulo_realizar_pix_txt = "Realizar Transferência PIX"
input_chave_destino_pix = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 180, 350, 40, placeholder="Chave PIX do Destinatário")
input_valor_realizar_pix = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 240, 350, 40, placeholder="Valor do PIX")
botao_confirmar_realizar_pix = Botao(LARGURA_TELA // 2 - 100, 310, 200, 50, "Confirmar PIX")
botao_voltar_menu_realizar_pix = Botao(LARGURA_TELA // 2 - 100, 380, 200, 50, "Voltar ao Menu")

# TELA PAGAR JOGO
titulo_pagar_jogo_txt = "Pagar Jogo"
input_valor_jogo = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 180, 350, 40, placeholder="Valor da Aposta/Pagamento")
input_nome_jogo = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 240, 350, 40, placeholder="Nome do Jogo (Opcional)")
botao_confirmar_pagar_jogo = Botao(LARGURA_TELA // 2 - 100, 310, 200, 50, "Confirmar Pagamento")
botao_voltar_menu_pagar_jogo = Botao(LARGURA_TELA // 2 - 100, 380, 200, 50, "Voltar ao Menu")

# TELA RECEBER PRÊMIO
titulo_receber_premio_txt = "Receber Prêmio de Jogo"
input_valor_premio = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 180, 350, 40, placeholder="Valor do Prêmio")
input_nome_jogo_premio = CaixaDeEntrada(LARGURA_TELA // 2 - 175, 240, 350, 40, placeholder="Nome do Jogo (Opcional)")
botao_confirmar_receber_premio = Botao(LARGURA_TELA // 2 - 100, 310, 200, 50, "Confirmar Recebimento")
botao_voltar_menu_receber_premio = Botao(LARGURA_TELA // 2 - 100, 380, 200, 50, "Voltar ao Menu")

# TELA EXTRATO
titulo_extrato_txt = "Extrato da Conta"
scroll_y_extrato = 0  # Para rolagem do extrato
botao_voltar_menu_ext = Botao(LARGURA_TELA // 2 - 100, ALTURA_TELA - 70, 200, 50, "Voltar ao Menu")
altura_linha_extrato = 20  # Altura de cada linha no extrato


# --- Funções para buscar dados do backend ---
def buscar_nome_cliente_db(id_cliente):
    if BACKEND_DISPONIVEL and id_cliente:
        # No seu backend, você precisaria de uma função que retorne o nome
        # Ou fazemos uma query direta aqui (menos ideal para separação de camadas)
        cliente_info = executar_query("SELECT nome FROM Clientes WHERE id_cliente = %s", (id_cliente,), fetch_one=True)
        if cliente_info:
            return cliente_info['nome']
    return f"Cliente ID {id_cliente}"  # Fallback


def carregar_contas_cliente_gui(id_cliente):
    global contas_cliente_gui, botoes_contas_gui
    contas_cliente_gui = []
    botoes_contas_gui = []
    if BACKEND_DISPONIVEL and id_cliente:
        contas_raw = executar_query(
            "SELECT id_conta, numero_conta, agencia, tipo_conta, saldo FROM Contas WHERE id_cliente = %s ORDER BY id_conta",
            (id_cliente,), fetch_all=True)
        if contas_raw:
            contas_cliente_gui = contas_raw
            # Cria botões para cada conta na tela de seleção
            y_offset = 120
            for i, conta in enumerate(contas_cliente_gui):
                texto_botao = f"{conta['tipo_conta']} Ag: {conta['agencia']} Cc: {conta['numero_conta']} (Saldo: R${conta['saldo']:.2f})"
                # Passa o id_conta como action_id para identificar qual botão foi clicado
                b = Botao(LARGURA_TELA // 2 - 250, y_offset + i * 50, 500, 40, texto_botao, fonte=FONTE_PEQUENA,
                          action_id=conta['id_conta'])
                botoes_contas_gui.append(b)
    return contas_cliente_gui


def limpar_inputs_tela(lista_inputs):
    for input_caixa in lista_inputs:
        input_caixa.limpar_texto()


# --- Loop Principal ---
while rodando:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # --- Manipulação de Eventos por Tela ---
        if estado_tela_atual == "LOGIN":
            input_cpf_login.manipular_evento(evento)
            ret_senha_login = input_senha_login.manipular_evento(evento)
            if botao_login.verificar_clique(evento, mouse_pos) or ret_senha_login == "enter":
                cpf = input_cpf_login.obter_texto()
                senha = input_senha_login.obter_texto()
                if BACKEND_DISPONIVEL:
                    id_cliente = login_cliente(cpf, senha)
                    if id_cliente is not None:
                        id_cliente_logado_gui = id_cliente
                        nome_cliente_logado_gui = buscar_nome_cliente_db(id_cliente)
                        definir_mensagem_status(f"Bem-vindo, {nome_cliente_logado_gui}!", VERDE_SUCESSO)
                        estado_tela_atual = "MENU_PRINCIPAL"
                        limpar_inputs_tela([input_cpf_login, input_senha_login])
                        carregar_contas_cliente_gui(id_cliente_logado_gui)  # Carrega contas ao logar
                        id_conta_selecionada_gui = None  # Reseta conta selecionada
                        saldo_conta_selecionada_gui = None
                    else:
                        definir_mensagem_status("CPF ou Senha inválidos.", VERMELHO_ERRO)
            if botao_ir_registrar.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "REGISTRO"
                definir_mensagem_status("Preencha para registrar.")
                limpar_inputs_tela([input_cpf_login, input_senha_login])

        elif estado_tela_atual == "REGISTRO":
            input_nome_reg.manipular_evento(evento)
            input_cpf_reg.manipular_evento(evento)
            input_senha_reg.manipular_evento(evento)
            input_confirma_senha_reg.manipular_evento(evento)
            if botao_confirmar_registro.verificar_clique(evento, mouse_pos):
                nome = input_nome_reg.obter_texto()
                cpf = input_cpf_reg.obter_texto()
                s1 = input_senha_reg.obter_texto()
                s2 = input_confirma_senha_reg.obter_texto()
                if not all([nome, cpf, s1, s2]):
                    definir_mensagem_status("Todos os campos são obrigatórios!", VERMELHO_ERRO)
                elif s1 != s2:
                    definir_mensagem_status("As senhas não coincidem!", VERMELHO_ERRO)
                else:
                    if BACKEND_DISPONIVEL:
                        novo_id = registrar_cliente(nome, cpf, s1)
                        if novo_id:
                            definir_mensagem_status(f"Cliente '{nome}' ID:{novo_id} registrado! Faça login.",
                                                    VERDE_SUCESSO)
                            estado_tela_atual = "LOGIN"
                            limpar_inputs_tela(
                                [input_nome_reg, input_cpf_reg, input_senha_reg, input_confirma_senha_reg])
                        else:
                            definir_mensagem_status("Falha no registro. Verifique os dados ou se o CPF já existe.",
                                                    VERMELHO_ERRO)
            if botao_voltar_login_reg.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "LOGIN"
                definir_mensagem_status("")
                limpar_inputs_tela([input_nome_reg, input_cpf_reg, input_senha_reg, input_confirma_senha_reg])

        elif estado_tela_atual == "MENU_PRINCIPAL":
            if botao_logout.verificar_clique(evento, mouse_pos):
                id_cliente_logado_gui = None;
                nome_cliente_logado_gui = "";
                contas_cliente_gui = [];
                id_conta_selecionada_gui = None;
                saldo_conta_selecionada_gui = None
                estado_tela_atual = "LOGIN"
                definir_mensagem_status("Logout realizado.", PRETO)
            if botao_listar_contas.verificar_clique(evento, mouse_pos):
                carregar_contas_cliente_gui(
                    id_cliente_logado_gui)  # Recarrega para caso novas contas tenham sido criadas
                estado_tela_atual = "SELECIONAR_CONTA"
                definir_mensagem_status("Selecione uma conta.")
            if botao_criar_conta_nav.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "CRIAR_CONTA"
                definir_mensagem_status("Informe o tipo da nova conta.")
            if botao_consultar_saldo_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    if BACKEND_DISPONIVEL: saldo_conta_selecionada_gui = consultar_saldo(id_conta_selecionada_gui)
                    if saldo_conta_selecionada_gui is not None:
                        definir_mensagem_status(
                            f"Saldo da conta {id_conta_selecionada_gui}: R$ {saldo_conta_selecionada_gui:.2f}", PRETO)
                    else:
                        definir_mensagem_status(f"Não foi possível obter o saldo da conta {id_conta_selecionada_gui}.",
                                                VERMELHO_ERRO)
                else:
                    definir_mensagem_status("Nenhuma conta selecionada. Use 'Listar/Selecionar'.", VERMELHO_ERRO)
            if botao_deposito_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    estado_tela_atual = "DEPOSITO"; definir_mensagem_status("Informe os dados do depósito.")
                else:
                    definir_mensagem_status("Selecione uma conta para depósito!", VERMELHO_ERRO)
            if botao_saque_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    estado_tela_atual = "SAQUE"; definir_mensagem_status("Informe os dados do saque.")
                else:
                    definir_mensagem_status("Selecione uma conta para saque!", VERMELHO_ERRO)
            if botao_cad_chave_pix_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    estado_tela_atual = "CAD_CHAVE_PIX"; definir_mensagem_status("Informe os dados da chave PIX.")
                else:
                    definir_mensagem_status("Selecione uma conta para cadastrar chave PIX!", VERMELHO_ERRO)
            if botao_realizar_pix_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    estado_tela_atual = "REALIZAR_PIX"; definir_mensagem_status("Informe os dados do PIX.")
                else:
                    definir_mensagem_status("Selecione uma conta de origem para o PIX!", VERMELHO_ERRO)
            if botao_pagar_jogo_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    estado_tela_atual = "PAGAR_JOGO"; definir_mensagem_status("Informe os dados do pagamento.")
                else:
                    definir_mensagem_status("Selecione uma conta para pagar o jogo!", VERMELHO_ERRO)
            if botao_receber_premio_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    estado_tela_atual = "RECEBER_PREMIO"; definir_mensagem_status("Informe os dados do prêmio.")
                else:
                    definir_mensagem_status("Selecione uma conta para receber o prêmio!", VERMELHO_ERRO)
            if botao_extrato_nav.verificar_clique(evento, mouse_pos):
                if id_conta_selecionada_gui:
                    if BACKEND_DISPONIVEL: extrato_gui = extrato(
                        id_conta_selecionada_gui) or []  # Garante que seja uma lista
                    estado_tela_atual = "EXTRATO";
                    definir_mensagem_status("Extrato da conta.");
                    scroll_y_extrato = 0
                else:
                    definir_mensagem_status("Selecione uma conta para ver o extrato!", VERMELHO_ERRO)


        elif estado_tela_atual == "SELECIONAR_CONTA":
            for i, btn_conta in enumerate(botoes_contas_gui):
                if btn_conta.verificar_clique(evento, mouse_pos):
                    id_conta_selecionada_gui = btn_conta.action_id  # action_id é o id_conta
                    saldo_conta_selecionada_gui = contas_cliente_gui[i]['saldo']  # Pega o saldo da lista já carregada
                    definir_mensagem_status(
                        f"Conta ID {id_conta_selecionada_gui} selecionada. Saldo: R$ {saldo_conta_selecionada_gui:.2f}",
                        VERDE_SUCESSO)
                    estado_tela_atual = "MENU_PRINCIPAL"
                    break
            if botao_voltar_menu_sel.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("")

        elif estado_tela_atual == "CRIAR_CONTA":
            input_tipo_conta_crt.manipular_evento(evento)
            if botao_confirmar_criar_conta.verificar_clique(evento, mouse_pos):
                tipo_conta = input_tipo_conta_crt.obter_texto().upper()
                if not tipo_conta:
                    definir_mensagem_status("Tipo da conta é obrigatório (CORRENTE/POUPANCA).", VERMELHO_ERRO)
                elif tipo_conta not in ["CORRENTE", "POUPANCA"]:
                    definir_mensagem_status("Tipo inválido. Use CORRENTE ou POUPANCA.", VERMELHO_ERRO)
                else:
                    if BACKEND_DISPONIVEL:
                        nova_cta_id = criar_conta_bancaria(id_cliente_logado_gui, tipo_conta)
                        if nova_cta_id:
                            definir_mensagem_status(f"Conta tipo {tipo_conta} ID:{nova_cta_id} criada!", VERDE_SUCESSO)
                            carregar_contas_cliente_gui(id_cliente_logado_gui)  # Atualiza lista de contas
                            limpar_inputs_tela([input_tipo_conta_crt])
                            estado_tela_atual = "MENU_PRINCIPAL"
                        else:
                            definir_mensagem_status("Erro ao criar conta.", VERMELHO_ERRO)
            if botao_voltar_menu_crt.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_tipo_conta_crt])

        elif estado_tela_atual == "DEPOSITO":
            input_valor_dep.manipular_evento(evento)
            input_desc_dep.manipular_evento(evento)
            if botao_confirmar_dep.verificar_clique(evento, mouse_pos):
                try:
                    valor = float(input_valor_dep.obter_texto())
                    desc = input_desc_dep.obter_texto()
                    if valor <= 0:
                        definir_mensagem_status("Valor do depósito deve ser positivo.", VERMELHO_ERRO)
                    elif BACKEND_DISPONIVEL and realizar_deposito(id_conta_selecionada_gui, valor, desc):
                        definir_mensagem_status(f"Depósito de R${valor:.2f} realizado!", VERDE_SUCESSO)
                        if saldo_conta_selecionada_gui is not None: saldo_conta_selecionada_gui += valor  # Atualiza saldo local
                        limpar_inputs_tela([input_valor_dep, input_desc_dep])
                        estado_tela_atual = "MENU_PRINCIPAL"
                    else:
                        definir_mensagem_status("Falha no depósito.", VERMELHO_ERRO)
                except ValueError:
                    definir_mensagem_status("Valor do depósito inválido.", VERMELHO_ERRO)
            if botao_voltar_menu_dep.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_valor_dep, input_desc_dep])

        elif estado_tela_atual == "SAQUE":
            input_valor_saq.manipular_evento(evento)
            input_desc_saq.manipular_evento(evento)
            if botao_confirmar_saq.verificar_clique(evento, mouse_pos):
                try:
                    valor = float(input_valor_saq.obter_texto())
                    desc = input_desc_saq.obter_texto()
                    if valor <= 0:
                        definir_mensagem_status("Valor do saque deve ser positivo.", VERMELHO_ERRO)
                    elif BACKEND_DISPONIVEL and realizar_saque(id_conta_selecionada_gui, valor, desc):
                        definir_mensagem_status(f"Saque de R${valor:.2f} realizado!", VERDE_SUCESSO)
                        if saldo_conta_selecionada_gui is not None: saldo_conta_selecionada_gui -= valor  # Atualiza saldo local
                        limpar_inputs_tela([input_valor_saq, input_desc_saq])
                        estado_tela_atual = "MENU_PRINCIPAL"
                    else:
                        definir_mensagem_status("Falha no saque (verifique saldo).",
                                                VERMELHO_ERRO)  # realizar_saque já imprime se saldo é insuficiente
                except ValueError:
                    definir_mensagem_status("Valor do saque inválido.", VERMELHO_ERRO)
            if botao_voltar_menu_saq.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_valor_saq, input_desc_saq])

        elif estado_tela_atual == "CAD_CHAVE_PIX":
            input_tipo_chave_pix.manipular_evento(evento)
            input_valor_chave_pix.manipular_evento(evento)
            if botao_confirmar_cad_pix.verificar_clique(evento, mouse_pos):
                tipo = input_tipo_chave_pix.obter_texto().upper()
                val = input_valor_chave_pix.obter_texto()
                if not tipo or not val:
                    definir_mensagem_status("Tipo e Valor da chave são obrigatórios.", VERMELHO_ERRO)
                elif BACKEND_DISPONIVEL and cadastrar_chave_pix(id_conta_selecionada_gui, tipo, val):
                    definir_mensagem_status(f"Chave PIX '{val}' ({tipo}) cadastrada!", VERDE_SUCESSO)
                    limpar_inputs_tela([input_tipo_chave_pix, input_valor_chave_pix])
                    estado_tela_atual = "MENU_PRINCIPAL"
                else:
                    definir_mensagem_status("Falha ao cadastrar chave PIX (verifique tipo ou se já existe).",
                                            VERMELHO_ERRO)
            if botao_voltar_menu_cad_pix.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_tipo_chave_pix, input_valor_chave_pix])

        elif estado_tela_atual == "REALIZAR_PIX":
            input_chave_destino_pix.manipular_evento(evento)
            input_valor_realizar_pix.manipular_evento(evento)
            if botao_confirmar_realizar_pix.verificar_clique(evento, mouse_pos):
                try:
                    chave_dest = input_chave_destino_pix.obter_texto()
                    valor = float(input_valor_realizar_pix.obter_texto())
                    if not chave_dest:
                        definir_mensagem_status("Chave PIX de destino é obrigatória.", VERMELHO_ERRO)
                    elif valor <= 0:
                        definir_mensagem_status("Valor do PIX deve ser positivo.", VERMELHO_ERRO)
                    elif BACKEND_DISPONIVEL and realizar_pix(id_conta_selecionada_gui, chave_dest, valor):
                        definir_mensagem_status(f"PIX de R${valor:.2f} para '{chave_dest}' realizado!", VERDE_SUCESSO)
                        if saldo_conta_selecionada_gui is not None: saldo_conta_selecionada_gui -= valor
                        limpar_inputs_tela([input_chave_destino_pix, input_valor_realizar_pix])
                        estado_tela_atual = "MENU_PRINCIPAL"
                    else:
                        definir_mensagem_status("Falha ao realizar PIX (verifique dados e saldo).", VERMELHO_ERRO)
                except ValueError:
                    definir_mensagem_status("Valor do PIX inválido.", VERMELHO_ERRO)
            if botao_voltar_menu_realizar_pix.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_chave_destino_pix, input_valor_realizar_pix])

        elif estado_tela_atual == "PAGAR_JOGO":
            input_valor_jogo.manipular_evento(evento)
            input_nome_jogo.manipular_evento(evento)
            if botao_confirmar_pagar_jogo.verificar_clique(evento, mouse_pos):
                try:
                    valor = float(input_valor_jogo.obter_texto())
                    nome = input_nome_jogo.obter_texto() or "Jogo Padrão"
                    if valor <= 0:
                        definir_mensagem_status("Valor do pagamento deve ser positivo.", VERMELHO_ERRO)
                    elif BACKEND_DISPONIVEL and pagar_jogo(id_conta_selecionada_gui, valor, nome):
                        definir_mensagem_status(f"Pagamento de R${valor:.2f} para '{nome}' realizado!", VERDE_SUCESSO)
                        if saldo_conta_selecionada_gui is not None: saldo_conta_selecionada_gui -= valor
                        limpar_inputs_tela([input_valor_jogo, input_nome_jogo])
                        estado_tela_atual = "MENU_PRINCIPAL"
                    else:
                        definir_mensagem_status("Falha no pagamento do jogo (verifique saldo).", VERMELHO_ERRO)
                except ValueError:
                    definir_mensagem_status("Valor do pagamento inválido.", VERMELHO_ERRO)
            if botao_voltar_menu_pagar_jogo.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_valor_jogo, input_nome_jogo])

        elif estado_tela_atual == "RECEBER_PREMIO":
            input_valor_premio.manipular_evento(evento)
            input_nome_jogo_premio.manipular_evento(evento)
            if botao_confirmar_receber_premio.verificar_clique(evento, mouse_pos):
                try:
                    valor = float(input_valor_premio.obter_texto())
                    nome = input_nome_jogo_premio.obter_texto() or "Prêmio Padrão"
                    if valor <= 0:
                        definir_mensagem_status("Valor do prêmio deve ser positivo.", VERMELHO_ERRO)
                    elif BACKEND_DISPONIVEL and receber_premio_jogo(id_conta_selecionada_gui, valor, nome):
                        definir_mensagem_status(f"Prêmio de R${valor:.2f} de '{nome}' recebido!", VERDE_SUCESSO)
                        if saldo_conta_selecionada_gui is not None: saldo_conta_selecionada_gui += valor
                        limpar_inputs_tela([input_valor_premio, input_nome_jogo_premio])
                        estado_tela_atual = "MENU_PRINCIPAL"
                    else:
                        definir_mensagem_status("Falha ao receber prêmio.", VERMELHO_ERRO)
                except ValueError:
                    definir_mensagem_status("Valor do prêmio inválido.", VERMELHO_ERRO)
            if botao_voltar_menu_receber_premio.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                limpar_inputs_tela([input_valor_premio, input_nome_jogo_premio])

        elif estado_tela_atual == "EXTRATO":
            if evento.type == pygame.MOUSEWHEEL:  # Rolagem com o mouse
                scroll_y_extrato += evento.y * 20  # Ajusta a velocidade da rolagem
                # Limita a rolagem para não sair da área visível do extrato
                max_scroll = max(0, len(extrato_gui) * altura_linha_extrato - (
                            ALTURA_TELA - 200))  # 200 é espaço para título e botão voltar
                scroll_y_extrato = max(-max_scroll, min(0, scroll_y_extrato))

            if botao_voltar_menu_ext.verificar_clique(evento, mouse_pos):
                estado_tela_atual = "MENU_PRINCIPAL";
                definir_mensagem_status("");
                extrato_gui = []

    # --- Lógica de Atualização de Estado ---
    if temporizador_mensagem > 0:
        temporizador_mensagem -= 1
    elif mensagem_status:  # Limpa apenas se o temporizador zerou e ainda há mensagem
        mensagem_status = ""

    # --- Desenhar na Tela ---
    tela.fill(CINZA_CLARO)

    if estado_tela_atual == "LOGIN":
        desenhar_texto(tela, titulo_login_txt, (LARGURA_TELA // 2, 100), FONTE_TITULO, PRETO, centralizado_x=True)
        input_cpf_login.desenhar(tela)
        input_senha_login.desenhar(tela)
        botao_login.desenhar(tela, mouse_pos)
        botao_ir_registrar.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "REGISTRO":
        desenhar_texto(tela, titulo_registro_txt, (LARGURA_TELA // 2, 60), FONTE_TITULO, PRETO, centralizado_x=True)
        input_nome_reg.desenhar(tela)
        input_cpf_reg.desenhar(tela)
        input_senha_reg.desenhar(tela)
        input_confirma_senha_reg.desenhar(tela)
        botao_confirmar_registro.desenhar(tela, mouse_pos)
        botao_voltar_login_reg.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "MENU_PRINCIPAL":
        desenhar_texto(tela, f"Bem-vindo, {nome_cliente_logado_gui}!", (LARGURA_TELA // 2, 60), FONTE_TITULO, PRETO,
                       centralizado_x=True)
        if id_conta_selecionada_gui:
            saldo_txt = f"Conta Selecionada: {id_conta_selecionada_gui}"
            if saldo_conta_selecionada_gui is not None:
                saldo_txt += f" | Saldo: R$ {saldo_conta_selecionada_gui:.2f}"
            desenhar_texto(tela, saldo_txt, (LARGURA_TELA // 2, 110), FONTE_NORMAL, PRETO, centralizado_x=True)
        else:
            desenhar_texto(tela, "Nenhuma conta selecionada. Use 'Listar/Selecionar'.", (LARGURA_TELA // 2, 110),
                           FONTE_NORMAL, CINZA_ESCURO, centralizado_x=True)

        botao_listar_contas.desenhar(tela, mouse_pos)
        botao_criar_conta_nav.desenhar(tela, mouse_pos)
        botao_consultar_saldo_nav.desenhar(tela, mouse_pos)
        botao_deposito_nav.desenhar(tela, mouse_pos)
        botao_saque_nav.desenhar(tela, mouse_pos)
        botao_cad_chave_pix_nav.desenhar(tela, mouse_pos)
        botao_realizar_pix_nav.desenhar(tela, mouse_pos)
        botao_pagar_jogo_nav.desenhar(tela, mouse_pos)
        botao_receber_premio_nav.desenhar(tela, mouse_pos)
        botao_extrato_nav.desenhar(tela, mouse_pos)
        botao_logout.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "SELECIONAR_CONTA":
        desenhar_texto(tela, titulo_selecionar_conta_txt, (LARGURA_TELA // 2, 60), FONTE_TITULO, PRETO,
                       centralizado_x=True)
        if not botoes_contas_gui:
            desenhar_texto(tela, "Nenhuma conta encontrada.", (LARGURA_TELA // 2, ALTURA_TELA // 2 - 50), FONTE_NORMAL,
                           CINZA_ESCURO, centralizado_x=True)
            desenhar_texto(tela, "Crie uma nova conta no menu principal.", (LARGURA_TELA // 2, ALTURA_TELA // 2),
                           FONTE_NORMAL, CINZA_ESCURO, centralizado_x=True)
        for btn_conta in botoes_contas_gui:
            btn_conta.desenhar(tela, mouse_pos)
        botao_voltar_menu_sel.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "CRIAR_CONTA":
        desenhar_texto(tela, titulo_criar_conta_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO,
                       centralizado_x=True)
        desenhar_texto(tela, f"Cliente: {nome_cliente_logado_gui} (ID: {id_cliente_logado_gui})",
                       (LARGURA_TELA // 2, 150), FONTE_NORMAL, CINZA_ESCURO, centralizado_x=True)
        input_tipo_conta_crt.desenhar(tela)
        botao_confirmar_criar_conta.desenhar(tela, mouse_pos)
        botao_voltar_menu_crt.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "DEPOSITO":
        desenhar_texto(tela, titulo_deposito_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO, centralizado_x=True)
        desenhar_texto(tela, f"Para Conta ID: {id_conta_selecionada_gui}", (LARGURA_TELA // 2, 150), FONTE_NORMAL,
                       CINZA_ESCURO, centralizado_x=True)
        input_valor_dep.desenhar(tela)
        input_desc_dep.desenhar(tela)
        botao_confirmar_dep.desenhar(tela, mouse_pos)
        botao_voltar_menu_dep.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "SAQUE":
        desenhar_texto(tela, titulo_saque_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO, centralizado_x=True)
        desenhar_texto(tela, f"Da Conta ID: {id_conta_selecionada_gui}", (LARGURA_TELA // 2, 150), FONTE_NORMAL,
                       CINZA_ESCURO, centralizado_x=True)
        input_valor_saq.desenhar(tela)
        input_desc_saq.desenhar(tela)
        botao_confirmar_saq.desenhar(tela, mouse_pos)
        botao_voltar_menu_saq.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "CAD_CHAVE_PIX":
        desenhar_texto(tela, titulo_cad_pix_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO, centralizado_x=True)
        desenhar_texto(tela, f"Para Conta ID: {id_conta_selecionada_gui}", (LARGURA_TELA // 2, 150), FONTE_NORMAL,
                       CINZA_ESCURO, centralizado_x=True)
        input_tipo_chave_pix.desenhar(tela)
        input_valor_chave_pix.desenhar(tela)
        botao_confirmar_cad_pix.desenhar(tela, mouse_pos)
        botao_voltar_menu_cad_pix.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "REALIZAR_PIX":
        desenhar_texto(tela, titulo_realizar_pix_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO,
                       centralizado_x=True)
        desenhar_texto(tela, f"Da Conta ID: {id_conta_selecionada_gui}", (LARGURA_TELA // 2, 150), FONTE_NORMAL,
                       CINZA_ESCURO, centralizado_x=True)
        input_chave_destino_pix.desenhar(tela)
        input_valor_realizar_pix.desenhar(tela)
        botao_confirmar_realizar_pix.desenhar(tela, mouse_pos)
        botao_voltar_menu_realizar_pix.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "PAGAR_JOGO":
        desenhar_texto(tela, titulo_pagar_jogo_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO,
                       centralizado_x=True)
        desenhar_texto(tela, f"Da Conta ID: {id_conta_selecionada_gui}", (LARGURA_TELA // 2, 150), FONTE_NORMAL,
                       CINZA_ESCURO, centralizado_x=True)
        input_valor_jogo.desenhar(tela)
        input_nome_jogo.desenhar(tela)
        botao_confirmar_pagar_jogo.desenhar(tela, mouse_pos)
        botao_voltar_menu_pagar_jogo.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "RECEBER_PREMIO":
        desenhar_texto(tela, titulo_receber_premio_txt, (LARGURA_TELA // 2, 100), FONTE_SUBTITULO, PRETO,
                       centralizado_x=True)
        desenhar_texto(tela, f"Para Conta ID: {id_conta_selecionada_gui}", (LARGURA_TELA // 2, 150), FONTE_NORMAL,
                       CINZA_ESCURO, centralizado_x=True)
        input_valor_premio.desenhar(tela)
        input_nome_jogo_premio.desenhar(tela)
        botao_confirmar_receber_premio.desenhar(tela, mouse_pos)
        botao_voltar_menu_receber_premio.desenhar(tela, mouse_pos)

    elif estado_tela_atual == "EXTRATO":
        desenhar_texto(tela, f"{titulo_extrato_txt} (ID: {id_conta_selecionada_gui})", (LARGURA_TELA // 2, 40),
                       FONTE_SUBTITULO, PRETO, centralizado_x=True)
        desenhar_texto(tela, "(Use a roda do mouse para rolar)", (LARGURA_TELA // 2, 70), FONTE_MICRO, CINZA_ESCURO,
                       centralizado_x=True)

        y_extrato = 100 + scroll_y_extrato
        if extrato_gui:
            for i, transacao in enumerate(extrato_gui):
                # Formata a linha do extrato de forma simples
                data_str = transacao.get('data_transacao').strftime('%d/%m/%y %H:%M') if transacao.get(
                    'data_transacao') else "N/A"
                tipo_str = str(transacao.get('tipo_transacao', 'N/A'))
                valor_str = f"R$ {transacao.get('valor', 0):.2f}"
                desc_str = str(transacao.get('descricao', ''))[:40]  # Limita descrição

                sinal = " "
                if tipo_str in ["DEPOSITO", "PIX_RECEBIDO", "PREMIO_JOGO"]:
                    sinal = "+"
                elif tipo_str in ["SAQUE", "PIX_ENVIADO", "PAGAMENTO_JOGO"]:
                    sinal = "-"

                linha_texto = f"{data_str} | {tipo_str:<15} | {sinal} {valor_str:<10} | {desc_str}"

                # Verifica se a linha está dentro da área visível antes de desenhar
                if y_extrato + i * altura_linha_extrato > 80 and y_extrato + i * altura_linha_extrato < ALTURA_TELA - 80:
                    desenhar_texto(tela, linha_texto, (30, y_extrato + i * altura_linha_extrato), FONTE_MICRO, PRETO)
        else:
            desenhar_texto(tela, "Nenhuma transação encontrada.", (LARGURA_TELA // 2, ALTURA_TELA // 2), FONTE_NORMAL,
                           CINZA_ESCURO, centralizado_x=True)

        botao_voltar_menu_ext.desenhar(tela, mouse_pos)

    # Desenhar mensagem de status global (no rodapé)
    if mensagem_status and temporizador_mensagem > 0:
        desenhar_texto(tela, mensagem_status, (LARGURA_TELA // 2, ALTURA_TELA - 30), FONTE_PEQUENA, cor_mensagem_status,
                       centralizado_x=True)

    pygame.display.flip()
    clock.tick(30)  # Mantém o FPS em 30

pygame.quit()
sys.exit()
