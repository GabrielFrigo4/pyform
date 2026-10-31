# 🎮 PyForm — AI Agent Briefing

> Motor gráfico e laboratório de computação gráfica procedural em Python moderno (3.12+), ModernGL (OpenGL 4.2 Core Profile) e GLFW. Repositório soberano do ecossistema pessoal de Gabriel Frigo.

---

## 🧭 Identidade e Papel

O **PyForm** é uma bancada de experimentação prática e aprendizado de Computação Gráfica moderna. O projeto serve como base laboratorial e acadêmica para exploração de shaders GLSL, geometria procedural, álgebra linear gráfica e desenvolvimento de um mini-game procedural:

- **Linguagem & Runtime:** Python 3.12+ com Astral `uv` e suporte antifrágil a ambientes POSIX (FreeBSD, Linux, macOS)
- **Camada Gráfica:** ModernGL sobre OpenGL Core Profile 4.2 (sem funções fixas legadas)
- **Janelas & Eventos:** GLFW nativo com callbacks defensivos e controle de ciclo de vida
- **Filosofia Arquitetural:** Baixa abstração, didática e clareza. Evite over-engineering ou burocracia excessiva. O código deve expor diretamente os conceitos gráficos (VBO, VAO, shaders, matrizes, loop de frame) de forma transparente e legível

---

## 📁 Estrutura Canônica de Arquivos

```text
PyForm/
├── game/
│   ├── assets/shaders/        # Fontes GLSL (.vert, .frag)
│   ├── core/                  # Engine, Window, GLFW callbacks e tempo
│   ├── graphics/              # ShaderProgram, Malhas (Triangle, Quad), Diagnósticos
│   ├── scenes/                # Protocolo Scene e cenas de demonstração/sandbox
│   └── audio/                 # Interface desacoplada com miniaudio
├── tests/                     # Contratos de pipeline e testes estruturais
├── .agents/                   # Governança e runbooks locais de IA
├── AGENTS.md                  # Constituição e briefing para agentes de IA
├── Makefile                   # Automação POSIX padronizada
├── PRINCIPLES.md              # 22 Princípios de Engenharia aplicados
├── README.md                  # Apresentação institucional e arquitetura
├── TODO.md                    # Roadmap estratégico e matriz de cobertura
└── main.py                    # Ponto de entrada CLI
```

---

## ⚠️ Regras Críticas para Agentes de IA

1. **Construção Didática Incremental (O Processo é o Objetivo):** O agente de IA NUNCA deve gerar módulos complexos prontos de uma vez ("one-shot dump"). Toda evolução do motor e do jogo deve ser construída passo a passo, em estreita colaboração com o usuário. O objetivo primordial é o aprendizado de Computação Gráfica; o resultado final sem o entendimento do processo é inútil.
2. **Hermetismo de Produção & Invariante `rm -rf .agents`:** Repositório 100% autônomo. Zero acoplamento de código de produção a `.agents/` ou `skills/` (a aplicação funciona plenamente se `.agents/` for sumariamente deletado).
3. **Baixa Abstração & POO Limpa:** Mantenha a arquitetura simples e direta ao ponto para fins didáticos. Use Programação Orientada a Objetos clássica, coesa e com responsabilidade única, evitando camadas intermediárias que mascarem a GPU.
4. **Zero Comentários Narrativos:** Evite comentários óbvios narrando código executável. Blocos lógicos devem ser separados por linhas em branco e expressar sua intenção via código autoexplicativo.
5. **Tipagem Estática & PEP 8:** Funções e métodos devem declarar type hints (`typing`) estritos e passar na validação do Ruff sem advertências (`make lint`).
6. **Nomenclatura Semântica:** Proibidas abreviações crípticas de uma única letra para variáveis de escopo amplo. Nomes devem ser legíveis e explicativos.
7. **Invariante Out-of-the-Box (Permissões Canônicas):** O projeto deve funcionar imediatamente após um simples `git clone`. Modos octais no Git Index DEVEM ser rigorosamente `0755` para executáveis/scripts/hooks e `0644` para código, configurações e documentação.
8. **Governança de Roadmap:** O repositório mantém seu [TODO.md](TODO.md) atualizado com a Matriz de Status e Backlog, referenciado pelo badge correspondente no [README.md](README.md).
9. **Refatoração Sem Legado (Clean-Break Invariant):** É proibido manter shims temporários ou código obsoleto em renomeações. Toda refatoração deve ser atômica e limpa.

---

## 🛡️ Regra da Proatividade e Correção Contínua (Boy Scout Rule)

O agente de IA atua de forma proativa na manutenção e aplicação dos padrões canônicos deste repositório.

Ao identificar linhas ou artefatos fora dos padrões estabelecidos:

1. **Notificar concisamente** o usuário sobre o ajuste realizado.
2. **Corrigir a inconformidade**, aplicando o padrão correspondente:
    - **Comentários Narrativos:** Eliminar comentários óbvios que apenas narram código executável.
    - **Banners Estruturais:** Ajustar réguas para exatamente 64 hífens no topo ou 32 caracteres com `### ` no corpo.
    - **Portabilidade POSIX:** Substituir bashismos (`[[ ]]`, `&>`, arrays, `source`) por sintaxe estrita POSIX `/bin/sh`.
    - **Shebang Universal:** Garantir sempre `#!/usr/bin/env sh` ou `#!/usr/bin/env python3`.
    - **Sequências ANSI & Escapes:** Não use octais (`\033`, `\001`) para caracteres ou escapes. Use `[ -t 1 ] && echo -n $'\e...'` ou notação hexadecimal (`\x01`, `\x1b`). Octal é exclusivo para permissões POSIX (`chmod 0755`, `chmod 0644`, `umask`).
    - **Redirecionamento Seguro:** Envolver destinos em aspas duplas (ex: `> "/dev/null" 2>&1`).
    - **Makefiles:** Assegurar cabeçalho `.POSIX: .SILENT:`, `MAKEFLAGS += --no-print-directory -s`, alinhamento estético de variáveis e zero `@` redundante.
    - **Permissões Canônicas:** Aplicar 4 dígitos octais (`chmod 0755`, `chmod 0644`, `chmod 0700`, `chmod 0600`).
    - **Invariante Out-of-the-Box:** Garantir modos octais corretos no Git Index e auto-cura em tempo de execução sem requerer intervenção manual pós-clone.
    - **Emissão Semântica de UI:** Substituir `echo` avulsos com emojis pelas rotinas canônicas `_ui_*`.
    - **Antifragilidade & Resiliência:** Resolução ativa de caminhos em cascata, auto-cura de permissões (0600 em chaves/segredos) e validação defensiva de pré-requisitos.
    - **Curadoria Cognitiva:** Capturar decisões estruturais e regras tácitas em skills locais compactas (`.agents/skills/`), mantendo-as atualizadas e expurgando ruído obsoleto.
    - **Refatoração Sem Legado:** Expurgar aliases obsoletos, variáveis mortas e shims de compatibilidade em renomeações.
    - **Elevação Antifrágil & Shift Seguro:** Usar o bloco explícito `if [ "$(id -u)" -ne 0 ]` para resolução de `ELEVATE` (evitando término fatal sob `set -e` como root) e proteger todo comando `shift` com validação prévia de parâmetros (`[ "$#" -ge N ] && shift N`).
    - **Simetria de Documentação:** Mover regras ou invariantes universais documentadas erroneamente em sub-membros específicos para o documento de arquitetura do grupo correspondente, eliminando falsas assimetrias.

---

## 🚀 Comandos de Verificação Rápida (Quality Gates)

| Comando            | Finalidade Operacional                                       |
| :----------------- | :----------------------------------------------------------- |
| `make help`        | Exibe o catálogo interativo de comandos disponíveis          |
| `make run`         | Executa a aplicação PyForm via `uv run`                      |
| `make dev`         | Executa em modo de desenvolvimento com hot-reload            |
| `make test`        | Executa a suíte de testes com pytest                         |
| `make format`      | Formata código-fonte e documentações (ruff + prettier)       |
| `make prettier`    | Formata arquivos Markdown com Prettier                       |
| `make ruff-format` | Formata código Python com Ruff                               |
| `make lint`        | Valida conformidade estática de linting sem alterar arquivos |
| `make hooks`       | Configura permissões `0755` nos ganchos de `.githooks/`      |
| `make ci`          | Executa a pipeline local de validação contínua (`test lint`) |
| `make clean`       | Remove caches temporários Python e ModernGL                  |

---

## 📖 Referências Obrigatórias

Antes de qualquer modificação neste ecossistema, consulte:

- [README.md](README.md) — Apresentação institucional, arquitetura e guia de execução
- [PRINCIPLES.md](PRINCIPLES.md) — Os 22 Princípios de Engenharia UNIX + Clean Code
- [TODO.md](TODO.md) — Roadmap estratégico e matriz de cobertura
- [LICENSE](LICENSE) — Licença do projeto
- [.agents/rules/python-standards.md](.agents/rules/python-standards.md) — Padrões de código Python
- [.agents/skills/pyform-graphics-engine/SKILL.md](.agents/skills/pyform-graphics-engine/SKILL.md) — Runbook da Engine Gráfica
- [.agents/skills/freebsd-uv-runtime/SKILL.md](.agents/skills/freebsd-uv-runtime/SKILL.md) — Runbook de Runtime FreeBSD e UV
