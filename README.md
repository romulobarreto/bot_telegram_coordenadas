# 🤖 Bot de Coordenadas – Regional Norte e Sul 🌍

Este projeto é um **bot do Telegram** desenvolvido em Python que busca **coordenadas geográficas (latitude e longitude)** com base no número da UC (Unidade Consumidora), chave, poste ou transformador. Ele retorna o link direto do Google Maps com a localização correspondente.  
  
Este bot foi criado para economizar tempo do time de backoffices, que antes, demoravam em média 3 minutos por atendimento, agora demoram 45 segundos, ou seja, um ganho de produtividade de 75%. Dessa forma, o time pode ajudar em outras demandas.

---

## 📌 Funcionalidades

- Exibe o menu de opções ao usuário (`🔌 UC`, `🔑 Chave`, `🗼 Poste`, `⚡ Transformador`).
- Recebe o número da pesquisa via mensagem no Telegram.
- Busca a latitude e longitude no banco de dados.
- Retorna o link do Google Maps com a localização exata.
- Respostas automáticas e personalizadas para novos usuários.
- Tolerante a erros de conexão com reconexão automática.

---

## 🛠 Tecnologias utilizadas

- Python 3
- [PyTelegramBotAPI (telebot)](https://pypi.org/project/pyTelegramBotAPI/)
- SQLite3

---

## 📁 Estrutura do Projeto

### 📂 Models
- `chave.py`: Classe Chave
- `poste.py`: Classe Poste
- `trafo.py`: Classe Trafo
- `uc.py`: Classe UC

### 📂 Database
- `chave.db`: Banco de chaves
- `poste.db`: Banco de postes
- `trafo.db`: Banco de transformadores
- `uc.db`: Banco de UCs

### 📂 Daos
- `chave_dao.py`: Realiza a busca da chave no banco
- `poste_dao.py`: Realiza a busca do poste no banco
- `trafo_dao.py`: Realiza a busca do trafo no banco
- `uc.py`: Realiza a busca da UC no banco

### 📂 Controllers
- `controller.py`: Regra de negócio para pesquisar e retornar o link do google maps

### 📂 Main
- `main.py`: Importa e inicia o bot. Manipula os inputs do usuário com o objetivo de retornar a localização exata que a equipe precisa 
---

## 🌍 Deploy

- Plataforma é a PythonAnyWhere  
- Bot rodando no plano free de 512mb de espaço  

---

# 👨‍💻 Autores  
- Breno Lucas Tomé Domingues
- Lenon Castro Torma
- Rômulo Barreto da Silva