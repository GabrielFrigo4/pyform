.POSIX:
.SILENT:

MAKEFLAGS += --no-print-directory -s

# ----------------------------------------------------------------
# Makefile: PyForm Graphics Engine & Procedural Forms
# ----------------------------------------------------------------

APP        = pyform
VERSION   != grep '^version = ' pyproject.toml | cut -d '"' -f 2 2> "/dev/null" || echo 0.1.0

.PHONY: all help run dev install test format prettier ruff-format lint hooks clean ci

all: help

### ================================
### HELP & DOCUMENTATION
### ================================
help:
	_e=$$'\e'; \
	cmd() { printf "    $${_e}[36mmake %-22s$${_e}[0m %s\n" "$$1" "$$2"; }; \
	sec() { printf "\n  $${_e}[1;33m%s$${_e}[0m\n" "$$1"; }; \
	sub() { printf "  $${_e}[1;34m  ── %s ──$${_e}[0m\n" "$$1"; }; \
	printf "\n  $${_e}[1;37mPyForm Graphics Engine — Catálogo de Comandos$${_e}[0m (v%s)\n" "$(VERSION)"; \
	printf "  ============================================================\n"; \
	sec "Execução & Desenvolvimento:"; \
	cmd "run"            "Executa o motor gráfico com resolução padrão (960x540)"; \
	cmd "dev"            "Executa em alta resolução para desenvolvimento (1280x720)"; \
	cmd "install"        "Sincroniza dependências via uv ou pip"; \
	sec "Qualidade, Testes & CI:"; \
	cmd "test"           "Executa a suíte de testes unitários defensivos"; \
	cmd "lint"           "Executa análise estática de código com Ruff"; \
	cmd "format"         "Formata Markdown (Prettier) e código Python (Ruff)"; \
	cmd "prettier"       "Formata documentações Markdown com Prettier"; \
	cmd "ruff-format"    "Formata código Python com Ruff"; \
	cmd "ci"             "Executa pipeline completa de quality gates locais"; \
	sec "Governança & Manutenção:"; \
	cmd "hooks"          "Configura e valida os ganchos do Git (.githooks)"; \
	cmd "clean"          "Remove caches temporários, __pycache__ e artefatos"; \
	echo ""

### ================================
### RUN & DEVELOPMENT
### ================================
run:
	if command -v uv > "/dev/null" 2>&1; then \
		uv run python3 main.py; \
	else \
		python3 main.py; \
	fi

dev:
	if command -v uv > "/dev/null" 2>&1; then \
		uv run python3 main.py --width 1280 --height 720; \
	else \
		python3 main.py --width 1280 --height 720; \
	fi

install:
	echo "📦 Sincronizando dependências do PyForm..."
	if command -v uv > "/dev/null" 2>&1; then \
		uv sync; \
	else \
		pip install -e .; \
	fi
	echo "✅ Ambiente pronto!"

### ================================
### QUALITY & TESTING
### ================================
test:
	echo "🧪 Executando suíte de testes unitários..."
	python3 -m unittest discover tests
	echo "✅ Testes concluídos com sucesso!"

lint:
	echo "🔍 Analisando sintaxe e estilo de código..."
	if command -v ruff > "/dev/null" 2>&1; then \
		ruff check .; \
	elif command -v uv > "/dev/null" 2>&1; then \
		uv run ruff check . 2> "/dev/null" || python3 -m py_compile main.py pyform/*.py tests/*.py; \
	else \
		python3 -m py_compile main.py pyform/*.py tests/*.py; \
	fi
	echo "✅ Validação estática aprovada!"

format: prettier ruff-format
	echo "✅ Formatação concluída!"

prettier:
	echo "🎨 Formatando documentações Markdown com Prettier..."
	if command -v npx > "/dev/null" 2>&1; then \
		npx prettier --write "**/*.md" 2> "/dev/null" || true; \
	elif command -v prettier > "/dev/null" 2>&1; then \
		prettier --write "**/*.md" 2> "/dev/null" || true; \
	fi

ruff-format:
	echo "🎨 Formatando código Python com Ruff..."
	if command -v ruff > "/dev/null" 2>&1; then \
		ruff format . 2> "/dev/null" || true; \
	fi

hooks:
	echo "🪝 Configurando ganchos Git (.githooks)..."
	chmod 0755 .githooks/pre-commit .githooks/commit-msg 2> "/dev/null" || true
	git config core.hooksPath .githooks 2> "/dev/null" || true
	echo "  ✅ core.hooksPath -> .githooks"

clean:
	echo "🧹 Limpando artefatos e caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2> "/dev/null" || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2> "/dev/null" || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2> "/dev/null" || true
	rm -rf dist build .eggs *.egg-info .coverage htmlcov
	echo "✅ Limpeza concluída!"

ci: test lint
	sh .githooks/pre-commit
	echo "🚀 PyForm pronto para produção e commits!"
