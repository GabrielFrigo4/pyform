# 🗺️ PyForm — Roadmap & Status de Engenharia

> Matriz detalhada de cobertura, governança e backlog estratégico de desenvolvimento do motor gráfico PyForm.

---

## 📊 Matriz de Status dos Componentes

| Componente                | Módulo            |    Status    | Cobertura | Descrição                                                       |
| :------------------------ | :---------------- | :----------: | :-------: | :-------------------------------------------------------------- |
| **Janela & Contexto**     | `pyform.window`   | ✅ Concluído |   100%    | Inicialização GLFW, tratamento de erros e eventos de teclado    |
| **Renderizador ModernGL** | `pyform.renderer` | ✅ Concluído |   100%    | Pipeline ModernGL 3.3 Core, alocação de VBO/VAO e ciclo de draw |
| **Shaders Procedurais**   | `pyform.shaders`  | ✅ Concluído |   100%    | Vertex & fragment shaders GLSL com antialiasing analítico       |
| **Orquestrador de App**   | `pyform.app`      | ✅ Concluído |   100%    | Loop principal de animação com cálculo de delta time            |
| **Interface CLI**         | `main.py`         | ✅ Concluído |   100%    | Parser de argumentos (`--width`, `--height`, `--title`)         |
| **Governança & Hooks**    | `.githooks/`      | ✅ Concluído |   100%    | Quality gates `pre-commit` e validador semântico `commit-msg`   |
| **Pipeline de CI**        | `.github/`        | ✅ Concluído |   100%    | Validação automatizada de sintaxe e testes via GitHub Actions   |

---

## 🎯 Backlog Estratégico de Evolução

### Épico 1: Shaders e Formas Procedurais Avançadas

- [ ] Adicionar catálogo de formas geométricas analíticas (SDFs 2D de polígonos regulares, estrelas e curvas de Bézier).
- [ ] Implementar seletor interativo de shaders e modos de visualização via teclado (teclas 1 a 9).
- [ ] Adicionar suporte a hot-reloading de arquivos `.glsl` em tempo de execução sem reiniciar o processo.

### Épico 2: Câmera e Transformações 3D

- [ ] Integrar biblioteca leve de matemática vetorial para matrizes Model-View-Projection (MVP).
- [ ] Adicionar suporte a formas 3D procedurais (hipercubos, sólidos platônicos e rotação contínua nos eixos XYZ).

### Épico 3: Captura de Mídia e Exportação

- [ ] Implementar captura instantânea de tela (_screenshot_) para PNG via buffer do ModernGL.
- [ ] Adicionar modo de gravação de loop de animação sem perda de frames.
