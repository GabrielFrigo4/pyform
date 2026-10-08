from typing import Protocol, runtime_checkable


@runtime_checkable
class Scene(Protocol):
    """Protocolo didático para cenas e experimentos gráficos do PyForm."""

    def update(self, delta_time: float) -> None:
        """Atualiza a lógica temporal e parâmetros analíticos da cena."""
        ...

    def render(self) -> None:
        """Submete a geometria e executa as chamadas de desenho no pipeline OpenGL."""
        ...

    def release(self) -> None:
        """Libera buffers (VBO/VAO) e programas de shader alocados na GPU."""
        ...
