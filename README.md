# 🤖 Bot de Coordenadas CS – Norte e Sul 🌍

Este projeto é um **bot do Telegram** desenvolvido em Python que busca **coordenadas geográficas (latitude e longitude)** com base no número da UC (Unidade Consumidora). Ele retorna o link direto do Google Maps com a localização correspondente.

---

## 📌 Funcionalidades

- Recebe o número da UC via mensagem no Telegram.
- Busca a latitude e longitude no banco de dados `Coordenadas.db`.
- Retorna o link do Google Maps com a localização exata.
- Respostas automáticas e personalizadas para novos usuários.
- Tolerante a erros de conexão com reconexão automática.

---

## 🛠 Tecnologias utilizadas

- Python 3
- [PyTelegramBotAPI (telebot)](https://pypi.org/project/pyTelegramBotAPI/)
- SQLite3
- Pandas (para manipulação inicial dos CSVs)
- VS Code (com extensão SQLite instalada)

---

## 📂 Estrutura do projeto

-🗃️ Coordenadas.db # Banco de dados SQLite com coordenadas
-🗃️ bot.ipynb # Código principal do bot
-🗃️ chave.py # Arquivo com a chave da API do Telegram
-🗃️ requirements.txt # Dependências do projeto
-🗃️ README.md # Este arquivo

# 👨‍💻 Autores
- Lenon Castro Torma
- Rômulo Barreto da Silva
