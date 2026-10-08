# 🗺️ PyForm — Roadmap & Status de Engenharia

> Matriz detalhada de cobertura, governança e backlog estratégico de desenvolvimento do motor gráfico PyForm.

---

## 📊 Matriz de Status dos Componentes

| Camada       | Subsistema / Módulo      | Arquivos Principais                                            | Status      | Descrição                                                                    |
| :----------- | :----------------------- | :------------------------------------------------------------- | :---------- | :--------------------------------------------------------------------------- |
| **Core**     | Loop & Orquestração      | [`game/core/engine.py`](game/core/engine.py)                   | `ESTÁVEL`   | Coordenação do ciclo principal, delta time e despacho de eventos.            |
| **Core**     | Janela & Contexto        | [`game/core/window.py`](game/core/window.py)                   | `ESTÁVEL`   | GLFW Core Profile 4.2, callbacks defensivos de resize/teclado.               |
| **Core**     | Entrypoint CLI           | [`main.py`](main.py)                                           | `ESTÁVEL`   | Interface de linha de comando com resolução e título configuráveis.          |
| **Graphics** | Compilação de Shaders    | [`game/graphics/shader.py`](game/graphics/shader.py)           | `ESTÁVEL`   | Pipeline GLSL 4.20 Core com carregamento UTF-8 e injeção de uniforms.        |
| **Graphics** | Geometria Procedural     | [`game/graphics/mesh.py`](game/graphics/mesh.py)               | `ESTÁVEL`   | Buffers VBO/VAO intercalados (`TriangleMesh` e `QuadMesh`).                  |
| **Graphics** | Diagnósticos de Hardware | [`game/graphics/diagnostics.py`](game/graphics/diagnostics.py) | `ESTÁVEL`   | Detecção de GPU, versão OpenGL, extensões ARB SPIR-V e Compute.              |
| **Graphics** | Blocos UBO (`std140`)    | _A implementar_                                                | `PLANEJADO` | Uniform Buffer Objects compartilhados entre shaders com alinhamento binário. |
| **Graphics** | Compute Shaders (GPGPU)  | _A implementar_                                                | `PLANEJADO` | Simulação paralela de partículas em SSBOs via `GL_ARB_compute_shader`.       |
| **Graphics** | Compilação SPIR-V        | _A implementar_                                                | `PLANEJADO` | Pipeline offline com `glslangValidator`, `glslc`, Slang e DXC.               |
| **Scenes**   | Arquitetura de Cenas     | [`game/scenes/base.py`](game/scenes/base.py)                   | `ESTÁVEL`   | Protocolo didático desacoplado (`update`, `render`, `release`).              |
| **Scenes**   | Sandbox Demonstrativo    | [`game/scenes/sandbox.py`](game/scenes/sandbox.py)             | `ESTÁVEL`   | Demonstração do ciclo de renderização e uniform `u_time`.                    |
| **Audio**    | Áudio Nativo             | [`game/audio/__init__.py`](game/audio/__init__.py)             | `PLANEJADO` | Interface desacoplada com miniaudio para efeitos sonoros e trilha.           |
| **Math**     | Álgebra Linear & Câmera  | _A implementar_                                                | `PLANEJADO` | Matrizes Model-View-Projection (MVP) e câmeras 2D/3D via PyGLM.              |
| **Quality**  | Suíte de Testes          | [`tests/test_engine.py`](tests/test_engine.py)                 | `ESTÁVEL`   | Contrato estático de shaders GLSL, CLI e conformidade de protocolos.         |
| **Tooling**  | Esteira & Automação      | [`Makefile`](Makefile), [`.githooks/`](.githooks/)             | `ESTÁVEL`   | Targets POSIX antifrágeis para teste, linting, formatação e pre-commit.      |

---

## 🎯 Backlog Estratégico de Evolução Didática (Passo a Passo)

### Fase 1: Fundação & Clean Code (Concluída)

- [x] Eliminação do subdiretório redundante `game/code/` e padronização em `game/{core,graphics,scenes,audio}`.
- [x] Remoção de artefatos órfãos na raiz (diretório vazio `shader/`).
- [x] Tipagem estática rigorosa (`typing.Any`, retornos estritos) e eliminação de saídas abruptas com `sys.exit`.
- [x] Criação da abstração didática `Scene` (protocolo) e especialização `SandboxScene`.
- [x] Introdução de classe base `Mesh`, `TriangleMesh` e `QuadMesh` para experimentação gráfica.
- [x] Suporte seguro à passagem de uniforms analíticos (`set_uniform`) em `ShaderProgram`.
- [x] Adaptação antifrágil de `Makefile` e `.githooks/pre-commit` para interoperabilidade POSIX (FreeBSD, Linux, macOS).

### Fase 2: Shaders Procedurais e Funções de Distância (SDFs)

- [ ] Implementação de shader analítico de fragmento para formas procedurais 2D via SDF (círculos, retângulos, anéis).
- [ ] Injeção de `u_resolution` para correção automática de aspect ratio no fragment shader.
- [ ] Antialiasing analítico de borda via `smoothstep`.
- [ ] Suporte a hot-reloading de arquivos GLSL em tempo de execução para prototipagem rápida.

### Fase 3: Uniform Buffer Objects (UBOs) & Álgebra Linear (PyGLM)

- [ ] Implementação de UBO com layout `std140` contendo matrizes de câmera (`u_view`, `u_projection`), tempo e resolução.
- [ ] Criação de módulo de transformação e câmera 2D (`OrthographicCamera`) com PyGLM.
- [ ] Compartilhamento do UBO entre diferentes materiais e shaders.

### Fase 4: Compute Shaders & GPGPU na Prática

- [ ] Alocação de Shader Storage Buffer Object (SSBO) para estado de partículas (posição, velocidade, vida).
- [ ] Shader de computação (`.comp`) para cálculo físico em paralelo na GPU via `GL_ARB_compute_shader`.
- [ ] Renderização direta dos buffers do Compute Shader sem tráfego de volta para a CPU.

### Fase 5: Tooling SPIR-V & Compilação Offline

- [ ] Automação no Makefile para compilação offline de GLSL/HLSL para `.spv` via `glslangValidator` e `glslc`.
- [ ] Suporte no carregador `ShaderProgram` para carregar binários SPIR-V pré-compilados.

### Fase 6: Mini-Game Procedural Didático & Áudio

- [ ] Cena de jogo 2D com entidade controlável pelo jogador via teclado.
- [ ] Geração procedural contínua de obstáculos e detecção analítica de colisão.
- [ ] Encapsulamento de efeitos sonoros com `miniaudio`.
