---
name: modern-opengl-shaders
description: >-
    Runbook cognitivo para desenvolvimento de shaders modernos (GLSL 4.20+, Vertex, Fragment/SDF,
    Compute/SSBO, Geometry, Tessellation), UBOs com std140 e compilação binária para SPIR-V via
    glslangValidator, glslc, Slang e DXC.
---

# 🌌 Modern OpenGL Shaders & SPIR-V Runbook

Esta habilidade orienta o desenvolvimento e a arquitetura de shaders modernos em OpenGL 4.2+ Core Profile, cobrindo todo o espectro do pipeline programável, blocos uniformes e ferramentas de compilação offline.

---

## 🏛️ O Espectro do Pipeline Programável de Shaders

```text
[VBO / Atributos] -> Vertex -> [Tessellation] -> [Geometry] -> Rasterizador -> Fragment -> [Framebuffer]
                                                                                   ^
                                                                          Compute (GPGPU puro / SSBO)
```

1. **Vertex Shader (`.vert`):**
    - Transforma vértices do _object space_ para _clip space_ (`gl_Position`).
    - Repassa atributos interpolados (_varyings_) para os estágios seguintes.
2. **Fragment Shader (`.frag` / Pixel Shader):**
    - Calcula a cor final de cada pixel/fragmento (`out vec4 frag_color`).
    - **SDFs (Signed Distance Fields):** Renderiza formas 2D perfeitas analiticamente sobre um _quad_ com antialiasing contínuo via `smoothstep()`, sem necessidade de malhas poligonais densas.
    - **Pós-Processamento & Luz:** Bloom, sombras 2D, raymarching analítico e vinheta.
3. **Compute Shader (`.comp` / GPGPU — `GL_ARB_compute_shader`):**
    - Executa paralelismo massivo fora da rasterização via grupos de trabalho (`layout(local_size_x = 16, local_size_y = 16) in;`).
    - Opera sobre **SSBOs (Shader Storage Buffer Objects)** ou texturas de imagem (`image2D`).
    - Ideal em 2D para: simulação física de partículas (100k+), autômatos celulares (_Game of Life_, _Falling Sand_) e fluidos em grade.
4. **Geometry Shader (`.geom`):**
    - Recebe primitivas inteiras (pontos, linhas, triângulos) e pode gerar novas primitivas dinamicamente na GPU (ex: expandir um ponto em um _quad_ de partícula).
5. **Tessellation Shaders (`.tesc` e `.tese`):**
    - Subdivide primitivas adaptativamente na GPU. Raramente necessário em jogos 2D; reservado para curvas de Bézier/splines complexas ou LOD em terrenos 3D.

---

## 📦 Uniform Buffer Objects (UBOs) & Alinhamento `std140`

1. **Objetivo:** Compartilhar blocos globais de dados (câmera, tempo, viewport) entre múltiplos programas com um único _bind_:
    ```glsl
    layout(std140, binding = 0) uniform GlobalFrameData {
        mat4  u_view;
        mat4  u_projection;
        vec2  u_resolution;
        float u_time;
    };
    ```
2. **Regra de Ouro do Alinhamento `std140`:**
    - Escalares (`float`, `int`): 4 bytes.
    - `vec2`: alinhado a 8 bytes (múltiplo de 8).
    - `vec3` e `vec4`: **alinhados a 16 bytes** (múltiplo de 16).
    - `mat4`: array de 4 `vec4`, ocupando 64 bytes contíguos.
    - _Atenção Didática:_ Nunca empacote um `float` logo antes de um `vec3` sem prever o padding de 12 bytes exigido pelo hardware.

---

## ⚡ Compilação Binária Offline & Ecossistema SPIR-V

Em pipelines modernos de produção, shaders não são distribuídos como texto GLSL puro, mas sim pré-compilados para bytecode intermediário binário **SPIR-V (`.spv`)**:

1. **Ferramentas Canônicas de Compilação:**
    - **`glslangValidator` (Khronos Reference):** `glslangValidator -V shader.vert -o shader.vert.spv`
    - **`glslc` (Google Shaderc):** `glslc shader.frag -o shader.frag.spv`
    - **`slangc` (Slang Shading Language):** Permite escrever shaders modernos em Slang e compilar diretamente para SPIR-V, HLSL ou GLSL.
    - **`dxc` (DirectX Shader Compiler):** Compila HLSL moderno diretamente para SPIR-V com `-spirv -T ps_6_0`.
2. **Vantagens de Engenharia:**
    - Validação estática em tempo de build (erros de sintaxe detectados antes do runtime).
    - Inicialização instantânea da aplicação (zero tempo gasto pelo driver compilando texto).
    - Suporte cruzado de linguagens de shading (GLSL, HLSL, Slang) convergindo no mesmo binário SPIR-V.
