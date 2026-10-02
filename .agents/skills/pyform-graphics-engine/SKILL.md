---
name: pyform-graphics-engine
description: Runbook cognitivo para desenvolvimento de shaders procedurais, gerenciamento de contexto ModernGL e arquitetura de eventos GLFW no PyForm.
---

# 🎮 PyForm Graphics Engine Runbook

Esta habilidade orienta o agente de IA na manutenção, extensão e otimização do motor gráfico PyForm, cobrindo o pipeline ModernGL, compilação de shaders GLSL e ciclo de vida do GLFW.

---

## 🏛️ Pipeline Gráfico do ModernGL

1. **Alocação de Buffers:**
    - VBOs contêm dados intercalados de vértice e cor (`2f 3f` para posição 2D + RGB).
    - O VAO (`vertex_array`) mapeia os atributos aos shaders usando nomes explícitos (`in_position`, `in_color`).
2. **Ciclo de Atualização e Desenho:**
    - Invocado em cada iteração do loop principal após `poll_events()`.
    - Limpeza de tela com `ctx.clear(r, g, b, a)` seguida por `vao.render(moderngl.TRIANGLES)`.
    - Atualização de variáveis uniformes (`u_time`, `u_resolution`) antes do draw call.

---

## ⚡ Shader Procedural e Funções de Distância (SDF)

1. **Correção de Aspecto:**
    - O fragment shader calcula a razão de aspecto (`u_resolution.x / u_resolution.y`) para preservar a simetria circular em qualquer resolução de janela.
2. **Antialiasing Analítico:**
    - Uso de `smoothstep(radius, radius - edge_width, dist)` em vez de cortes binários (`step`), garantindo bordas perfeitamente suavizadas sem serrilhamento.

---

## 🛡️ Invariantes do GLFW & Execução Headless

1. **Isolamento de Janela:**
    - A criação de contexto exige `OPENGL_CORE_PROFILE` e versão mínima 3.3.
2. **Resiliência em CI/CD:**
    - Módulos devem permitir testes estáticos e de lógica sem tentar inicializar display gráfico real, suportando ambientes sem servidor X11/Wayland configurado.
