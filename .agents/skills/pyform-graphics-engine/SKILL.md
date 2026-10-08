---
name: pyform-graphics-engine
description: >-
    Runbook cognitivo para o ecossistema PyForm em Python moderno (3.12+), ModernGL, PyGLM,
    NumPy, GLFW e miniaudio, cobrindo POO limpa, buffers VBO/VAO, ciclo de vida e cenas didáticas.
---

# 🎮 PyForm Graphics Engine & Python Stack Runbook

Esta habilidade orienta a engenharia de software e a integração de bibliotecas do motor gráfico PyForm, equilibrando Programação Orientada a Objetos clássica, tipagem estática e baixa abstração em Computação Gráfica.

---

## 🐍 A Stack Tecnológica do PyForm

1. **ModernGL (OpenGL 4.2 Core):**
    - Elimina chamadas legadas com sintaxe pythônica direta.
    - Recursos principais: `ctx.buffer()` (VBO), `ctx.vertex_array()` (VAO), `ctx.program()` (Shaders), `ctx.clear()`.
    - Gerenciamento explícito: todo buffer ou programa alocado deve ter seu descarte garantido via `.release()`.
2. **GLFW:**
    - Criação de janela com hints estritos de OpenGL Core Profile 4.2 (`CONTEXT_VERSION_MAJOR 4`, `CONTEXT_VERSION_MINOR 2`, `OPENGL_CORE_PROFILE`).
    - Callbacks não-bloqueantes (`_on_resize`, `_on_key`) associados via `glfw.set_window_user_pointer()`.
3. **PyGLM & Álgebra Linear Gráfica:**
    - Manipulação de vetores (`glm.vec2`, `glm.vec3`, `glm.vec4`) e matrizes afins (`glm.mat4`).
    - Geração de transformações padrão: `glm.translate()`, `glm.rotate()`, `glm.scale()`, `glm.ortho()` e `glm.perspective()`.
4. **NumPy:**
    - Criação e serialização de buffers de vértice contíguos em memória com dtype `f4` (float32).
    - Dados intercalados (_interleaved_): posições e atributos no mesmo buffer (`vertices.tobytes()`).
5. **miniaudio:**
    - Reprodução de áudio nativo em C desacoplada da thread de renderização, sem dependência do runtime do Pygame.

---

## 🏛️ Filosofia de POO & Arquitetura Didática

O PyForm segue a **Programação Orientada a Objetos clássica, limpa e coesa**:

1. **Responsabilidade Única por Classe:**
    - `Window`: Gerencia a janela GLFW, contexto gráfico e tratamento de eventos de tela.
    - `Engine`: Orquestra o loop temporal de frames, cálculo de `delta_time` e despacho para a cena ativa.
    - `Mesh` (`TriangleMesh`, `QuadMesh`): Encapsula a geometria de vértices, VBO e VAO.
    - `ShaderProgram`: Encapsula a leitura, compilação de shaders e injeção de uniforms.
    - `Scene` (Protocolo): Define o contrato didático para qualquer experimento ou fase de jogo (`update(dt)`, `render()`, `release()`).
2. **Baixa Abstração Didática:**
    - Evite intermediários que ocultem a GPU. O desenvolvedor deve enxergar diretamente quando um buffer é alocado, quando um uniform é enviado e quando uma chamada de desenho (`vao.render()`) é emitida.

---

## 🎯 Regra da Construção Incremental Passo a Passo

1. **O Processo é o Objetivo:** O PyForm existe prioritariamente para o aprendizado prático de Computação Gráfica pelo usuário.
2. **Proibido "One-Shot Dumping":** O agente NUNCA deve gerar mecânicas inteiras ou arquiteturas complexas adiantadas. Cada vértice, shader, uniform, transformação de matriz e colisão deve ser construído, explicado e validado em conjunto, etapa por etapa.
