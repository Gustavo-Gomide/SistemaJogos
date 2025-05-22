# SistemaJogos

Sistema de jogos retrô feito em Python com Pygame e MySQL.

---

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

Abra o terminal e execute:
```sh
git clone https://github.com/Gustavo-Gomide/SistemaJogos.git
cd caminho/para/pasta/pygame
```

### 2. Criar ambiente virtual (opcional, recomendado)

No terminal:
```sh
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar as dependências

```sh
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

- Certifique-se de ter o MySQL instalado e rodando.
- Crie o banco de dados e as tabelas necessárias (veja instruções ou scripts SQL no projeto).
- Ajuste as configurações de conexão no arquivo de banco de dados, se necessário.

### 5. Rodar o sistema

```sh
python main.py
```

---

## 🕹️ Sobre o sistema

Esse projeto é um sistema de jogos retrô, com visual inspirado em menus clássicos.  
Você pode acessar diferentes jogos, testar músicas e efeitos, ajustar configurações de áudio e gerenciar usuários com login/cadastro integrado ao banco de dados.

- **Menu Principal:** Tela inicial com acesso rápido aos jogos, músicas, configurações e login/cadastro.
- **Jogos:** Lista de jogos clássicos (Snake, Tetris, Pong, etc.) em uma área rolável.
- **Músicas:** Teste músicas de fundo e efeitos sonoros, com botões de play, pause e parar.
- **Configurações:** Ajuste volumes de efeitos e músicas.
- **Login/Cadastro:** Sistema de autenticação de usuários integrado ao banco de dados.

---

## 🛠️ Como adicionar novas telas ou jogos

1. **Crie uma nova classe de tela**
   - Crie um novo arquivo em `telas/` (ex: `tela_novojogo.py`).
   - Importe e herde de `Tela`.
   - Implemente o layout e lógica da tela.

2. **Registre a tela no navegador**
   - No arquivo principal ou onde o navegador é configurado:
     ```python
     navegador.registrar_tela("novojogo", TelaNovoJogo)
     ```

3. **Adicione um botão de acesso**
   - No menu, adicione um botão que chama `navegador.ir_para("novojogo")`.

Assim, você pode expandir o sistema facilmente, criando novas experiências retrô.

---

## 📁 Estrutura de pastas (exemplo)

```
projeto/
│
├── main.py
├── requirements.txt
├── README.md
├── telas/
│   ├── tela_menu.py
│   ├── tela_musicas.py
│   └── ...
├── utilitarios/
│   ├── Aprincipal_widgets.py
│   ├── musicas.py
│   └── ...
├── databases/
│   └── cadastro_database.py
└── ...
```

---

## 💡 Dicas

- Use imagens e fontes personalizadas para deixar o visual mais retrô.
- Adicione novos jogos seguindo o padrão das classes existentes.
- Melhore a responsividade ajustando tamanhos e posições dos componentes.
- Implemente novos recursos, como rankings, conquistas ou multiplayer local.
- Leia os comentários no código para entender cada parte e facilitar a manutenção.

---

## ❓ Dúvidas

Se tiver qualquer dúvida, consulte os comentários no código ou entre em contato comigo.  
Sugestões e melhorias são sempre bem-vindas!

---

**Divirta-se programando e jogando!**
