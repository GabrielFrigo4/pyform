---
name: freebsd-uv-runtime
description: >-
    Runbook cognitivo para resolução de dependências e runtime antifrágil com Astral uv no FreeBSD,
    cobrindo pacotes C/C++ sem wheels no PyPI, integração com pkg, flags de compilação e system-site-packages.
---

# 🐡 FreeBSD & Astral uv Antifragile Runtime

Este runbook orienta a configuração, resolução de dependências e execução determinística de projetos Python com aceleração gráfica (ModernGL, GLFW, PyGLM) no FreeBSD utilizando o Astral `uv`.

---

## 🧭 O Desafio dos Pacotes Python no FreeBSD

No ecossistema Python padrão, a maioria dos pacotes no PyPI distribui binários pré-compilados (_wheels_) exclusivamente para Linux (`manylinux`), macOS e Windows.

No FreeBSD:

1. **Ausência de Wheels no PyPI:** Pacotes que contêm extensões em C/C++ (`moderngl`, `glcontext`, `pyglm`, `cffi`, `ruff`) não possuem _wheels_ binárias no PyPI para arquitetura FreeBSD amd64.
2. **Falha de Compilação dos Sources (sdist):** Ao tentar compilar a partir do código-fonte bruto (`.tar.gz`), a compilação frequentemente falha porque:
    - Os cabeçalhos e bibliotecas do sistema no FreeBSD ficam localizados sob `/usr/local/include` e `/usr/local/lib`, enquanto o compilador busca por padrão em `/usr/include`.
    - Cabeçalhos de X11 (`X11/Xlib.h`) e Mesa OpenGL exigem flags explícitas.
    - Ferramentas como `ruff` ou `maturin` tentam acionar o compilador Rust caso não haja binário nativo.

---

## 🛡️ A Solução Canônica: `pkg` + `uv --system-site-packages`

A abordagem mais rápida, estável e antifrágil no FreeBSD consiste em utilizar os binários nativos empacotados pelo projeto FreeBSD Ports/Packages:

### 1. Instalar Dependências Nativas via `pkg`

```sh
sudo pkg install -y \
    libglvnd \
    mesa-libs \
    ruff \
    py312-glfw \
    py312-moderngl \
    py312-numpy \
    py312-pyglm \
    py312-pillow
```

### 2. Configurar o Virtualenv com Acesso ao Sistema

Crie o ambiente virtual do `uv` instruindo-o a herdar as bibliotecas instaladas pelo `pkg` no sistema:

```sh
uv venv --system-site-packages .venv
```

Isso gera um `.venv/pyvenv.cfg` contendo `include-system-site-packages = true`, permitindo que o interpretador acesse instantaneamente os binários C nativos otimizados do FreeBSD.

### 3. Execução sem Sincronização Destrutiva

Para evitar que o `uv` tente sobrescrever o ambiente ou compilar dependências faltantes do PyPI a cada execução, utilize a flag `--no-sync`:

```sh
uv run --no-sync python3 main.py
```

---

## 🔧 Compilação Manual de Fontes C/C++ (Quando Necessário)

Se um pacote Python específico não estiver disponível no catálogo do `pkg` e precisar ser compilado via código-fonte (`sdist`), forneça explicitamente os caminhos de busca do FreeBSD:

```sh
CFLAGS="-I/usr/local/include" \
LDFLAGS="-L/usr/local/lib" \
CPATH="/usr/local/include" \
LIBRARY_PATH="/usr/local/lib" \
uv pip install --no-binary :all: <nome_do_pacote>
```
