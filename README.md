# rediauto

Monitor de janelas para Windows que preenche automaticamente o espaço livre da tela. Se você já tem uma janela encaixada (`Win + Seta Esquerda/Direita`) ou maximizada, ao abrir um novo programa ele é movido sozinho para o lado oposto — sem precisar arrastar nada.

Projeto **open source**, licenciado sob [MIT](LICENSE) — use, modifique e distribua livremente.

## Funcionalidades

- Detecta a próxima janela aberta e move para o lado livre da tela
- Se a janela existente estiver **maximizada**, divide a tela automaticamente entre as duas
- Ignora janelas irrelevantes: tooltips, diálogos, overlays click-through (ex: HUD do DualSenseX)
- Ícone na bandeja do sistema com opção de **pausar/retomar** e **sair**
- Roda como script Python ou como executável standalone (`.exe`), sem depender do Windows ter Python instalado

## Requisitos

- Windows 10/11
- [uv](https://docs.astral.sh/uv/) para gerenciar o ambiente Python (instala a versão do Python do projeto automaticamente)

## Instalação e uso

```bash
git clone https://github.com/mayconaraujosantos/rediauto.git
cd rediauto
make sync   # ou: uv sync
make run    # ou: uv run main.py
```

Depois de rodar, um ícone aparece na bandeja do sistema. Clique com o botão direito para pausar/retomar o monitor ou sair.

### Gerar o executável

```bash
make build
```

Gera `dist/rediauto.exe`, um executável standalone (não precisa de Python instalado na máquina de destino).

## Comandos do Makefile

| Comando | Descrição |
| --- | --- |
| `make sync` | Instala/atualiza as dependências do projeto |
| `make run` | Roda o app em modo console (`uv run main.py`) |
| `make icon` | Regenera o ícone em `assets/icon.ico` |
| `make build` | Gera o ícone e empacota `dist/rediauto.exe` |
| `make clean` | Remove artefatos de build (`build/`, `dist/`, `*.spec`) |

## Estrutura do projeto

```text
main.py                 # lógica de monitoramento e ícone de bandeja
scripts/gerar_icone.py  # gera assets/icon.ico
assets/icon.ico          # ícone do app
```

## Contribuindo

Contribuições são bem-vindas!

1. Faça um fork do repositório
2. Crie uma branch para sua alteração (`git checkout -b feat/minha-feature`)
3. Use [Conventional Commits](https://www.conventionalcommits.org/) nas mensagens (`feat:`, `fix:`, `docs:`, `refactor:`, etc.)
4. Abra um Pull Request descrevendo a mudança e, se possível, como testar

Se for reportar um bug, inclua: versão do Windows, o que você esperava que acontecesse e o que de fato aconteceu.

## Licença

[MIT](LICENSE) © mayconaraujosantos
