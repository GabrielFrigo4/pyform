# 🎮 PyForm — AI Agent Briefing

> Motor gráfico e laboratório de computação gráfica procedural em Python moderno (3.12+), ModernGL (OpenGL 4.2 Core Profile) e GLFW. Repositório soberano do ecossistema pessoal de Gabriel Frigo.

---

## 🧭 Identidade e Filosofia do Projeto

O **PyForm** é uma bancada de experimentação prática e aprendizado de Computação Gráfica moderna. O projeto serve como base laboratorial e acadêmica para exploração de shaders GLSL, geometria procedural, álgebra linear gráfica e desenvolvimento de um mini-game procedural:

- **Linguagem & Runtime:** Python 3.12+ com Astral `uv` e suporte antifrágil a ambientes POSIX (FreeBSD, Linux, macOS).
- **Camada Gráfica:** ModernGL sobre OpenGL Core Profile 4.2 (sem funções fixas legadas).
- **Janelas & Eventos:** GLFW nativo com callbacks defensivos e controle de ciclo de vida.
- **Filosofia Arquitetural:** Baixa abstração, didática e clareza. Evite over-engineering ou burocracia excessiva. O código deve expor diretamente os conceitos gráficos (VBO, VAO, shaders, matrizes, loop de frame) de forma transparente e legível.

---

## 🏛️ Topologia Canônica de Módulos

```text
PyForm/
├── game/
│   ├── assets/shaders/   # Fontes GLSL (.vert, .frag)
│   ├── core/             # Engine, Window, GLFW callbacks e tempo
│   ├── graphics/         # ShaderProgram, Malhas (Triangle, Quad), Diagnósticos
│   ├── scenes/           # Protocolo Scene e cenas de demonstração/sandbox
│   └── audio/            # Interface desacoplada com miniaudio
├── tests/                # Contratos de pipeline e testes estruturais
├── Makefile              # Automação POSIX padronizada
└── main.py               # Ponto de entrada CLI
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
8. **Governança de Roadmap (Opção C):** O repositório mantém seu [TODO.md](TODO.md) atualizado com a Matriz de Status e Backlog, referenciado pelo badge correspondente no [README.md](README.md).
9. **Refatoração Sem Legado (Clean-Break Invariant):** É proibido manter shims temporários ou código obsoleto em renomeações. Toda refatoração deve ser atômica e limpa.

---

## 🛡️ Regra da Proatividade e Correção Contínua (Boy Scout Rule)

O agente de IA **DEVE SER ATIVAMENTE PROATIVO** na manutenção e aplicação dos padrões canônicos deste repositório.

Se durante a execução de qualquer tarefa o agente identificar qualquer linha de código, script, Makefile ou documentação fora dos padrões estabelecidos:

1. **Notificar concisamente** o usuário sobre a divergência encontrada.
2. **Corrigir imediatamente a inconformidade**, eliminando comentários narrativos, aplicando permissões octais corretas e assegurando a limpeza do repositório.

---

## 📖 Referências Obrigatórias

- **[README.md](README.md)**: Apresentação institucional, arquitetura e guia de execução
- **[PRINCIPLES.md](PRINCIPLES.md)**: Os 22 Princípios de Engenharia UNIX + Clean Code
- **[TODO.md](TODO.md)**: Roadmap estratégico e matriz de cobertura
- **[.agents/skills/](.agents/skills/)**: Runbooks operacionais locais
