# Nexus Souls Bot

Bot de Discord com IA (Gemini) por servidor, personalidade configurável e pesquisa em wikis de Elden Ring.

## Configuração
1. Copie `.env.example` para `.env` e preencha (no FadeHost, use as variáveis do painel).
2. `pip install -r requirements.txt`
3. `python bot.py`

## Discord
- Ative o *Message Content Intent* no Developer Portal.
- `/canal` ativa a IA no canal atual; `/personalidade` define o prompt do servidor.

## Atenção
- Nunca suba o `.env` ou o token para o GitHub.
- A busca (`buscar_wiki`) usa a API da wiki.gg e precisa ser testada.
