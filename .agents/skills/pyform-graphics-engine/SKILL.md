---
name: pyform-graphics-engine
description: >-
    Runbook cognitivo para o ecossistema PyForm em Python moderno (3.12+), ModernGL e OpenGL 4.2+,
    cobrindo shaders GLSL 4.20+, UBOs std140, FBOs, render loops 60/120 FPS, PyGLM, NumPy e POO didática.
---

# 🎮 PyForm Graphics Engine & Shaders Runbook

Esta habilidade orienta a engenharia de software, o pipeline programável de shaders e a integração de bibliotecas do motor gráfico PyForm em Python moderno (3.12+), equilibrando Programação Orientada a Objetos clássica, baixa abstração e Computação Gráfica moderna.

---

## 🐍 A Stack Tecnológica do PyForm

1. **ModernGL (OpenGL 4.2+ Core Profile):**
    - Sintaxe pythônica direta sobre a API gráfica moderna sem chamadas legadas (`glBegin`/`glEnd`).
    - Primitivas essenciais: `ctx.buffer()` (VBO), `ctx.vertex_array()` (VAO), `ctx.program()` (Shaders), `ctx.framebuffer()` (FBO) e `ctx.clear()`.
    - Gerenciamento explícito de recursos: descarte determinístico de buffers, texturas, framebuffers e programas via `.release()`.
2. **GLFW:**
    - Janela com context hints estritos de OpenGL Core Profile 4.2 (`CONTEXT_VERSION_MAJOR 4`, `CONTEXT_VERSION_MINOR 2`, `OPENGL_CORE_PROFILE`).
    - Callbacks não-bloqueantes (`_on_resize`, `_on_key`) associados via `glfw.set_window_user_pointer()`.
3. **PyGLM & Álgebra Linear Gráfica:**
    - Manipulação de vetores (`glm.vec2`, `glm.vec3`, `glm.vec4`) e matrizes afins (`glm.mat4`).
    - Transformações canônicas: `glm.translate()`, `glm.rotate()`, `glm.scale()`, `glm.ortho()` e `glm.perspective()`.
4. **NumPy:**
    - Criação e serialização de buffers de vértices contíguos em memória com dtype `f4` (float32).
    - Dados intercalados (_interleaved_): posições e atributos no mesmo buffer (`vertices.tobytes()`).
5. **miniaudio:**
    - Reprodução de áudio nativo em C desacoplada da thread de renderização, sem dependência de runtimes pesados externos.

---

## 🌌 Pipeline de Shaders ModernGL (GLSL 4.20+)

O PyForm utiliza o pipeline programável moderno em GLSL 4.20+ via `ctx.program()`:

```text
[VBO / Atributos] -> Vertex Shader -> Rasterizador -> Fragment Shader (SDF / Pós) -> [Framebuffer]
                                                              ^
                                                     Compute Shader (SSBO / GPGPU)
```

1. **Vertex Shader (`.vert`):**
    - Transforma coordenadas de vértices de _object space_ para _clip space_ (`gl_Position`).
    - Repassa atributos interpolados (_varyings_) para os estágios subsequentes do pipeline.
2. **Fragment Shader (`.frag`):**
    - Calcula a cor final de cada pixel/fragmento (`out vec4 frag_color`).
    - **SDFs (Signed Distance Fields):** Renderiza formas 2D perfeitas analiticamente sobre um _quad_ com antialiasing contínuo via `smoothstep()`, sem necessidade de malhas poligonais densas.
    - Pós-processamento e iluminação: vinheta, bloom, aberração cromática e sombras 2D.
3. **Compute Shader (`.comp` / GPGPU — `GL_ARB_compute_shader`):**
    - Paralelismo massivo em grupos de trabalho (`layout(local_size_x = 16, local_size_y = 16) in;`).
    - Opera sobre **SSBOs (Shader Storage Buffer Objects)** ou texturas de imagem (`image2D`).
    - Ideal para simulação física de partículas em larga escala (100k+), autômatos celulares e fluidos em grade.
4. **Compilação e Criação de Programa no ModernGL:**
    ```python
    program = ctx.program(
        vertex_shader=vertex_glsl_code,
        fragment_shader=fragment_glsl_code,
    )
    ```

---

## 📦 Uniform Buffer Objects (UBOs) & Alinhamento `std140`

Compartilha blocos globais de dados (câmera, matrizes de visão e projeção, tempo, resolução) entre múltiplos shaders com um único binding:

1. **Definição no GLSL:**
    ```glsl
    #version 420 core
    layout(std140, binding = 0) uniform GlobalFrameData {
        mat4  u_view;
        mat4  u_projection;
        vec2  u_resolution;
        float u_time;
    };
    ```
2. **Regras de Alinhamento `std140`:**
    - Escalares (`float`, `int`): 4 bytes.
    - `vec2`: alinhado a 8 bytes (múltiplo de 8).
    - `vec3` e `vec4`: **alinhados a 16 bytes** (múltiplo de 16).
    - `mat4`: array de 4 `vec4`, ocupando 64 bytes contíguos.
    - **Atenção ao Padding:** Nunca posicione um escalar (`float`) imediatamente antes de um `vec3` sem prever os 12 bytes de preenchimento exigidos pelo hardware.
3. **Associação no ModernGL:**
    ```python
    ubo = ctx.buffer(reserve=80)
    ubo.bind_to_uniform_block(binding=0)
    ```

---

## 🖼️ Framebuffers (FBOs) & Render Targets

O desacoplamento da renderização primária para texturas off-screen viabiliza resolução virtual fixa e pipelines modulares de pós-processamento:

1. **Criação de Render Targets:**
    ```python
    color_texture = ctx.texture((view_w, view_h), components=4)
    depth_texture = ctx.depth_texture((view_w, view_h))
    fbo = ctx.framebuffer(
        color_attachments=[color_texture],
        depth_attachment=depth_texture,
    )
    ```
2. **Ciclo de Render Off-Screen:**
    - Redirecionar comandos de renderização: `fbo.use()`.
    - Limpar e desenhar a cena didática: `fbo.clear(0.05, 0.05, 0.08, 1.0)`.
    - Restaurar o framebuffer principal da janela: `ctx.screen.use()`.
    - Renderizar o _screen quad_ com o fragment shader de pós-processamento vinculando `color_texture.use(location=0)`.

---

## ⏱️ Render Loops a 60/120 FPS & Temporização

1. **Sincronização Vertical (V-Sync):**
    - Ativado via `glfw.swap_interval(1)` para sincronizar frames com a taxa de atualização do monitor (60 Hz, 120 Hz, 144 Hz).
2. **Loop com Delta Time Estável:**
    ```python
    target_fps = 60.0
    dt_limit = 0.1  # Previne spiral of death em pausas de depuração
    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        now = glfw.get_time()
        dt = min(now - last_time, dt_limit)
        last_time = now

        glfw.poll_events()
        scene.update(dt)

        fbo.use()
        scene.render()

        ctx.screen.use()
        post_quad.render()

        glfw.swap_buffers(window)
    ```
3. **Passo de Física Desacoplado (Accumulator):**
    - Utiliza passo de tempo fixo (`fixed_dt = 1.0 / 60.0`) com acumulador de resíduo para simulação física consistente e determinística, independentemente de a renderização rodar a 60 FPS, 120 FPS ou monitores de alta frequência.

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
