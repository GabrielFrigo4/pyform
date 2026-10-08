import moderngl

SEPARATOR_WIDTH = 64


def log_hardware_info(ctx: moderngl.Context) -> None:
    """Inspeciona e exibe no terminal as capacidades e extensões da GPU."""
    exts = ctx.extensions
    feature_groups: dict[str, dict[str, bool]] = {
        "Shaders & Compilação": {
            "GLSL 420 Pack (Bindings explícitos)": ctx.version_code >= 420
            or "GL_ARB_shading_language_420pack" in exts,
            "Compute Shaders (4.3+)": ctx.version_code >= 430 or "GL_ARB_compute_shader" in exts,
            "SPIR-V nativo (4.6+)": ctx.version_code >= 460 or "GL_ARB_gl_spirv" in exts,
            "Geometry Shaders (3.2+)": ctx.version_code >= 320 or "GL_ARB_geometry_shader4" in exts,
            "Tessellation Shaders (4.0+)": ctx.version_code >= 400
            or "GL_ARB_tessellation_shader" in exts,
        },
        "Buffers & Memória GPU": {
            "UBO (Uniform Buffer Objects 3.1+)": ctx.version_code >= 310
            or "GL_ARB_uniform_buffer_object" in exts,
            "SSBO (Shader Storage Buffers 4.3+)": ctx.version_code >= 430
            or "GL_ARB_shader_storage_buffer_object" in exts,
            "Image Load / Store (4.2+)": ctx.version_code >= 420
            or "GL_ARB_shader_image_load_store" in exts,
            "Persistent Buffers (4.4+)": ctx.version_code >= 440 or "GL_ARB_buffer_storage" in exts,
        },
        "Pipeline Gráfico & Rendição": {
            "Base Instance / Instancing (4.2+)": ctx.version_code >= 420
            or "GL_ARB_base_instance" in exts,
            "Multi-Draw Indirect (4.3+)": ctx.version_code >= 430
            or "GL_ARB_multi_draw_indirect" in exts,
            "Direct State Access (DSA 4.5+)": ctx.version_code >= 450
            or "GL_ARB_direct_state_access" in exts,
            "Bindless Textures (ARB)": "GL_ARB_bindless_texture" in exts,
            "Conservative Rasterization": any(
                ext in exts
                for ext in ("GL_NV_conservative_raster", "GL_INTEL_conservative_rasterization")
            ),
        },
        "Diagnóstico & Profiling": {
            "GPU Timer Queries (3.3+)": ctx.version_code >= 330 or "GL_ARB_timer_query" in exts,
            "Debug Output Callback (4.3+)": ctx.version_code >= 430
            or "GL_ARB_debug_output" in exts,
            "Vulkan Memory Interop": "GL_EXT_memory_object" in exts,
        },
    }

    separator = "=" * SEPARATOR_WIDTH
    sub_separator = "-" * SEPARATOR_WIDTH
    title = "DIAGNÓSTICO DO HARDWARE & DRIVER (OPENGL)"

    print(separator)
    print(f" {title:^60}")
    print(separator)
    print(f" GPU (Renderer)    : {ctx.info['GL_RENDERER']}")
    print(f" Fabricante        : {ctx.info['GL_VENDOR']}")
    print(f" Versão do Driver  : {ctx.info['GL_VERSION']}")
    samples = ctx.screen.samples if 0 <= ctx.screen.samples <= 64 else 4
    print(f" Código GLSL       : {ctx.version_code} (#version {ctx.version_code} core)")
    print(f" Amostras MSAA     : {samples}x")

    for group_name, feats in feature_groups.items():
        print(sub_separator)
        print(f" [{group_name}]")
        for feat, enabled in feats.items():
            status = "✔ Suportado" if enabled else "✘ Indisponível"
            print(f"   • {feat:<38}: {status}")

    print(separator)
    print("Pressione ESC na janela para sair.\n")
