# Game Store API 🎮

## 1. Membros do Grupo 👥

- Nome: Jalmir de Jesus Ferreira da Silva Junior

---

## 2. Explicação do Sistema 📝

Esta aplicação é uma **API REST** para uma loja de jogos, desenvolvida com o objetivo de demonstrar a importância dos testes automatizados na manutenção de software.

### Funcionalidades principais:

- 📋 **Cadastro de Clientes (Customers):**
  Permite criar, listar e buscar clientes da loja.

- 🧑‍💻 **Cadastro de Jogadores (Gamers):**
  Permite criar, listar e buscar gamers cadastrados na plataforma.

- 🕹️ **Gerenciamento de Jogos (Games):**
  Permite adicionar jogos ao catálogo da loja, listar os jogos disponíveis e buscar jogos por título.

- 🛒 **Simulação de Compra (em construção):**
  Funcionalidade futura que permitirá simular compras de jogos.

---

## 3. Tecnologias Utilizadas 🛠️

- **Linguagem:** Python 3.12
- **Framework Web:** FastAPI
- **ORM:** SQLModel
- **Banco de Dados:** SQLite (durante o desenvolvimento e nos testes)
- **Testes:** Pytest
- **Integração Contínua:** GitHub Actions
- **Ambiente de Teste:** CI configurado para rodar os testes automaticamente nos seguintes sistemas operacionais:
  - Ubuntu (Linux)
  - MacOS
  - Windows

---

## Rodando o projeto localmente 🚀

### Requisitos:

- Python 3.12+
- Virtualenv (ou gerenciador de ambiente similar)

### Instalação:

```bash
# Clonar o repositório
git clone https://github.com/SEU-USUARIO/game-store-api.git
cd game-store-api

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # (Linux / Mac)
# ou
.venv\Scripts\activate  # (Windows)

# Instalar dependências
pip install -r requirements.txt
```
