# Regras Canônicas de Engenharia Python & ModernGL

> Diretrizes estritas de desenvolvimento, qualidade e arquitetura para o motor gráfico PyForm.

---

## 🏛️ Diretrizes de Domínio & Linguagem

1. **Baseline Python:** Código estritamente compatível com Python 3.12+, utilizando sintaxe moderna de coleções (`list[str]`, `dict[str, Any]`, `X | None`).
2. **Tipagem Estática Completa:** Todas as funções, métodos e parâmetros devem declarar type hints estritos (`typing`). Métodos que interagem com ponteiros brutos do GLFW devem explicitar `Any` com anotações sóbrias.
3. **Baixa Abstração Didática:** O repositório prioriza o aprendizado transparente de Computação Gráfica. Exponha diretamente o funcionamento de buffers (VBO/VAO), shaders GLSL e o loop de frames em vez de criar camadas complexas de abstração que ocultam a GPU.
4. **Construção Incremental Didática:** O desenvolvimento deve ser passo a passo, coeso e iterativo com o usuário. Proibido despejar códigos complexos prontos sem explicação prévia.
5. **POO Clássica & Responsabilidade Única:** Classes com papéis bem delimitados (`Window`, `Engine`, `Mesh`, `ShaderProgram`, `Scene`), sem acoplamento oculto.
6. **Gerenciamento de Recursos Gráficos:** Todo buffer ModernGL (`VBO`, `VAO`, `Program`, `Context`) e janela GLFW deve implementar método explícito de liberação e descarte (`release()` e `destroy()`), chamado de forma defensiva em blocos `finally:`.
7. **Zero Comentários Narrativos:** É estritamente proibido incluir comentários óbvios narrando código executável. Blocos lógicos devem ser separados por linhas em branco e expressar sua intenção de forma autoexplicativa. Comentários são reservados a equações matemáticas e notas de algoritmos de rendering.
8. **Tratamento Defensivo de Erros:** Erros de inicialização de janela, compilação de shaders ou ausência de arquivos devem levantar exceções descritivas (`RuntimeError`, `FileNotFoundError`) em vez de interromper o processo via `sys.exit`.
9. **Resiliência Headless em CI/CD:** Módulos de lógica, parsing de shaders e CLI devem ser testáveis sem exigir um display gráfico real ou servidor Wayland/X11 ativo.
