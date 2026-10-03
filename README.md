# PyForm Graphics Engine

> Motor gráfico experimental e laboratório de computação gráfica procedural construído em Python, ModernGL (OpenGL 4.2 Core) e GLFW.

O **PyForm** nasceu como uma extensão prática e aprofundada dos conceitos explorados na disciplina de Computação Gráfica. Em vez de se limitar aos exercícios convencionais ou à linha de base acadêmica (OpenGL 4.0), o projeto funciona como uma bancada de testes para experimentação de baixo nível com shaders, álgebra linear gráfica, geração procedural e arquitetura de engines — convergindo no desenvolvimento de um mini-game modular.

---

## Destaques & Objetivos

- **Pipeline Gráfico Moderno:** Contexto focado em OpenGL 4.2 Core Profile via ModernGL, dispensando pipelines legados de função fixa.
- **Laboratório de Shaders & Compilação:** Suporte e testes com GLSL 4.20, binários SPIR-V (`GL_ARB_gl_spirv`), Compute Shaders (`GL_ARB_compute_shader`) e futuras integrações com outras linguagens de shading (HLSL, Slang).
- **Matemática Gráfica Vetorizada:** Transformações afins, projeções e matrizes de câmera gerenciadas com PyGLM e buffers estruturados com NumPy.
- **Áudio Nativo Desacoplado:** Reprodução de trilhas e efeitos via `miniaudio` (bindings C leves, sem dependência do runtime do Pygame).
- **Tooling de Automação:** Gerenciamento de dependências com `uv` e esteira de qualidade padronizada via Makefile `.POSIX` e Ruff.

---

## Arquitetura do Repositório

```text
.
├── game/
│   ├── assets/
│   └── code/
│       ├── audio/
│       ├── core/
│       ├── graphics/
│       └── scenes/
├── tests/
├── Makefile
├── pyproject.toml
└── main.py
```

---

## Pré-requisitos do Sistema

Bibliotecas de desenvolvimento OpenGL (`libGL.so` e `libEGL.so`) necessárias no sistema operacional:

### Fedora / RHEL

```bash
sudo dnf install -y libglvnd-devel mesa-libGL-devel mesa-libEGL-devel
```

### Debian / Ubuntu

```bash
sudo apt update && sudo apt install -y libgl-dev libegl-dev
```

### Arch Linux / Manjaro

```bash
sudo pacman -S --needed libglvnd mesa
```

### FreeBSD

```sh
sudo pkg install -y libglvnd mesa-libs
```

---

## Instalação e Execução

### Clonar e Instalar Dependências

```bash
git clone https://github.com/GabrielFrigo4/pyform
cd PyForm
make install
```

### Comandos Disponíveis

| Comando       | Descrição                                                |
| ------------- | -------------------------------------------------------- |
| `make run`    | Executa a engine na resolução padrão (960×540)           |
| `make dev`    | Executa em resolução de desenvolvimento (1280×720)       |
| `make test`   | Roda a suíte de testes unitários                         |
| `make lint`   | Executa análise estática com Ruff                        |
| `make format` | Aplica formatação automática em Python (Ruff) e Markdown |
| `make clean`  | Remove caches temporários (`__pycache__`, `.ruff_cache`) |

---

## Licença

Distribuído sob os termos da licença especificada no arquivo `LICENSE`.
