# Regras de Engenharia Python & ModernGL

1. **Baseline Python:** Código estritamente compatível com Python 3.12+.
2. **Tipagem Estática:** Anotações de tipo completas em assinaturas de funções e métodos (`typing.Any`, `typing.Optional`, `typing.Callable`).
3. **Gerenciamento de Recursos Gráficos:** Todo buffer ModernGL (`VBO`, `VAO`, `Program`, `Context`) e janela GLFW deve implementar método explícito de liberação e descarte (`destroy()` / `release()`).
4. **Zero Comentários Narrativos:** Blocos lógicos separados exclusivamente por linhas em branco.
5. **Tratamento Defensivo:** Imports de pacotes com aceleração gráfica (`moderngl`, `glfw`) devem estar encapsulados para que testes de lógica e linting possam rodar em ambientes headless (CI/CD) sem falha catastrófica.
