# clubsonar.com.br

Páginas ponte dos grupos de ofertas no WhatsApp. Site estático servido pelo GitHub Pages.

## Como editar

1. Edite o `site.json` (textos, grupos, link do convite, contato).
2. Rode `python3 build.py` para gerar os HTML e o `config.js`.
3. Faça commit dos arquivos gerados e abra um PR. O GitHub Pages publica a `main`.

- **Trocar o link de um grupo** (ex.: #101 → #102): mude só o `groupUrl` no `site.json` e rode o build. Todos os botões passam por `/<nicho>/entrar`.
- **Novo nicho** (ex.: `/carros`): adicione uma entrada em `niches` copiando uma existente e rode o build.
- **Tirar um grupo do ar** sem apagar: `"active": false`.

## Estrutura

- `build.py` — gera `index.html`, `<nicho>/index.html`, `<nicho>/entrar/index.html`, `privacidade/index.html` e `config.js`.
- `assets/site.css` — estilo único (paleta e contrastes comentados no topo).
- `tracking.js` — eventos `page_view`, `cta_click` (nicho, posição, variante) e `scroll_50`, guarda UTMs da visita. Analytics e pixel só carregam se os IDs forem preenchidos no `site.json`.
