# 🎮 PyForm — AI Agent Briefing

> Motor gráfico e laboratório de exploração procedural em Python moderno (3.12+), ModernGL (OpenGL 3.3+ Core Profile) e GLFW. Repositório soberano do ecossistema pessoal de Gabriel Frigo.

---

## 🧭 Identidade e Papel

O **PyForm** é uma aplicação gráfica para renderização de formas geométricas procedurais, animações temporais analíticas e prototipagem ágil de shaders e pipelines gráficos com ModernGL e GLFW:

- **Linguagem & Runtime:** Python 3.12+ com Astral `uv` como gerenciador ultrarrápido.
- **Camada Gráfica:** ModernGL sobre OpenGL Core Profile 3.3 / 4.x.
- **Janelas & Eventos:** GLFW nativo com tratamento defensivo de erros e callbacks.
- **Filosofia:** Minimalismo, ausência de frameworks pesados, execução determinística e rápida.

---

## ⚠️ Regras Críticas para Agentes de IA

1. **Hermetismo de Produção & Invariante `rm -rf .agents`:** Repositório 100% autônomo. Zero acoplamento de código de produção a `.agents/` ou `skills/` (a aplicação funciona plenamente se `.agents/` for sumariamente deletado).
2. **Zero Comentários Narrativos:** Evite comentários óbvios narrando código executável. Blocos lógicos devem ser separados por linhas em branco e expressar sua intenção via código autoexplicativo.
3. **Tipagem Estática & PEP 8:** Funções e métodos devem declarar type hints (`typing`) estritos e passar na validação do Ruff sem advertências.
4. **Nomenclatura Semântica:** Proibidas abreviações crípticas de uma única letra para variáveis de escopo amplo. Nomes devem ser legíveis e explicativos.
5. **Invariante Out-of-the-Box (Permissões Canônicas):** O projeto deve funcionar imediatamente após um simples `git clone`. Modos octais no Git Index DEVEM ser rigorosamente `0755` para executáveis/scripts/hooks e `0644` para código, configurações e documentação.
6. **Governança de Roadmap (Opção C):** O repositório mantém seu [TODO.md](TODO.md) atualizado com a Matriz de Status e Backlog, referenciado pelo badge correspondente no `README.md`.
7. **Refatoração Sem Legado (Clean-Break Invariant):** É proibido manter shims temporários ou código obsoleto em renomeações. Toda refatoração deve ser atômica e limpa.

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
