import moderngl


def log_hardware_info(ctx: moderngl.Context) -> None:
    """Inspeciona e exibe no terminal as capacidades da GPU e extensões do driver."""
    has_compute = "GL_ARB_compute_shader" in ctx.extensions
    has_spirv = "GL_ARB_gl_spirv" in ctx.extensions

    print("=" * 64)
    print(f" Renderer  : {ctx.info['GL_RENDERER']}")
    print(f" Versão GL : {ctx.info['GL_VERSION']}")
    print(f" Compute   : {'Disponível (ARB)' if has_compute else 'Não suportado'}")
    print(f" SPIR-V    : {'Disponível (ARB)' if has_spirv else 'Não suportado'}")
    print("=" * 64)
