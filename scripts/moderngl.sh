#!/usr/bin/env sh
set -eu

CALL_DIR="$(cd "$(dirname "${0}")" && pwd -P)"
if [ -d "${CALL_DIR}/game/assets/icons" ]; then
    PROJECT_ROOT="${CALL_DIR}"
elif [ -d "${CALL_DIR}/../game/assets/icons" ]; then
    PROJECT_ROOT="$(cd "${CALL_DIR}/.." && pwd -P)"
else
    PROJECT_ROOT="${CALL_DIR}"
fi

ICON_SOURCE="${PROJECT_ROOT}/game/assets/icons/icon.png"
if [ ! -f "${ICON_SOURCE}" ]; then
    ICON_SOURCE="${PROJECT_ROOT}/moderngl.png"
fi

if [ ! -f "${ICON_SOURCE}" ]; then
    printf "Erro: Ícone do ModernGL não encontrado em %s\n" "${PROJECT_ROOT}" >&2
    exit 1
fi

ICON_DEST="${HOME}/.local/share/icons/hicolor/512x512/apps"
mkdir -p "${ICON_DEST}"
cp "${ICON_SOURCE}" "${ICON_DEST}/moderngl.png"

APPS_DIR="${HOME}/.local/share/applications"
mkdir -p "${APPS_DIR}"

cat << DESKTOP_EOF > "${APPS_DIR}/moderngl.desktop"
[Desktop Entry]
Type=Application
Name=ModernGL
Exec=python3
Icon=${ICON_DEST}/moderngl.png
StartupWMClass=moderngl
DESKTOP_EOF

DEFAULT_ICONS_DIR="${HOME}/.icons/default"
if [ ! -f "${DEFAULT_ICONS_DIR}/index.theme" ]; then
    mkdir -p "${DEFAULT_ICONS_DIR}"
    cat << THEME_EOF > "${DEFAULT_ICONS_DIR}/index.theme"
[Icon Theme]
Inherits=breeze_cursors
THEME_EOF
fi

if command -v update-desktop-database > "/dev/null" 2>&1; then
    update-desktop-database "${APPS_DIR}"
fi

if command -v gtk-update-icon-cache > "/dev/null" 2>&1; then
    gtk-update-icon-cache -f -t "${HOME}/.local/share/icons/hicolor" > "/dev/null" 2>&1 || true
fi

if command -v kbuildsycoca6 > "/dev/null" 2>&1; then
    kbuildsycoca6 --noincremental > "/dev/null" 2>&1 || true
elif command -v kbuildsycoca5 > "/dev/null" 2>&1; then
    kbuildsycoca5 --noincremental > "/dev/null" 2>&1 || true
fi

rm -rf "${HOME}/.cache/icon-cache.kcache" "${HOME}/.cache/krunner" 2> "/dev/null" || true

printf "Configuração concluída com sucesso:\n"
printf "• Ícone XDG:     %s/moderngl.png\n" "${ICON_DEST}"
printf "• Desktop Entry: %s/moderngl.desktop\n" "${APPS_DIR}"
printf "• Cursor Padrão: %s/index.theme\n" "${DEFAULT_ICONS_DIR}"
