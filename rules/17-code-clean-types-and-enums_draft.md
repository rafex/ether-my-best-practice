---
id: code-clean-types-and-enums
title: Código Limpio — Tipos Fuertes y Enums
status: Borrador
tags: [code-clean, types, enums, stringly-typed, lint, refactoring]
checksum: e55cb0b7fb7714f0c2f82e47acec8b2fad874fdd73acc4966fbca15337edb123
---

# Regla 17: Código Limpio — Tipos Fuertes y Enums — ⚠️ *Borrador*

### Premisa: Evitar validaciones por string mágicos

No validar estados, categorías, modos ni tipos de dominio con **cadenas mágicas** comparadas con `equals`, `==`, o en `switch` sobre strings. Usar **enums / tipos fuertes** que encapsulen los valores válidos y la lógica de decisión. Un dominio cerrado (un conjunto finito y conocido de valores) debe modelarse como tipo, no como string suelto.

El anti-patrón se conoce como *stringly-typed*: las decisiones de negocio se toman comparando literales de string dispersos por el código, sin compilación que garantice su validez, sin autocompletado y sin refactorización segura.

tags: [obligatorio]

### Estructura: Matriz de herramientas lint por lenguaje

| Lenguaje | Herramienta | Detección del anti-patrón |
|---|---|---|
| Java | Error Prone + Checkstyle | `StringEquality`, `StringLiteralEquals`, `illegalType` |
| JavaScript/TypeScript | ESLint | `no-string-literal`, `ban-types`, reglas custom |
| Python | ruff / pylint | comparación de literales (magic-value), `typing.Literal` como mejora |
| Rust | clippy | comparaciones de strings/`&str`, `match` sobre strings |

tags: [opcional]

### Ejemplo: Antipatrón → Patrón correcto

**Antipatrón (stringly-typed):**

```java
private static String normalizeCanvasMode(final String tool, final String mode) {
    if ("ETHERPAD".equals(tool)) {
        if ("INDEPENDENT".equals(mode) || "MODERATOR_ONLY".equals(mode)) return mode;
        return "COLLABORATIVE";
    }
    return "MODERATOR_ONLY".equals(mode) ? "MODERATOR_ONLY" : "INDEPENDENT";
}
```

Problemas: strings dispersos, sin validación de compilación, valores inválidos posibles, imposible refactorizar con seguridad.

**Patrón correcto (enums + tipos fuertes):**

```java
enum Tool {
    ETHERPAD,
    OTHER
}

enum CanvasMode {
    INDEPENDENT,
    MODERATOR_ONLY,
    COLLABORATIVE
}

private static CanvasMode normalizeCanvasMode(final Tool tool, final CanvasMode mode) {
    if (tool == Tool.ETHERPAD) {
        return switch (mode) {
            case INDEPENDENT, MODERATOR_ONLY -> mode;
            case COLLABORATIVE -> CanvasMode.COLLABORATIVE;
        };
    }
    return mode == CanvasMode.MODERATOR_ONLY ? CanvasMode.MODERATOR_ONLY : CanvasMode.INDEPENDENT;
}
```

Ventajas: el compilador garantiza valores válidos, refactorización segura, autocompletado, y la lógica de transformación queda tipada.

**Ejemplo Python (typing.Literal / Enum):**

```python
from enum import Enum

class Tool(Enum):
    ETHERPAD = "etherpad"
    OTHER = "other"

class CanvasMode(Enum):
    INDEPENDENT = "independent"
    MODERATOR_ONLY = "moderator_only"
    COLLABORATIVE = "collaborative"

def normalize_canvas_mode(tool: Tool, mode: CanvasMode) -> CanvasMode:
    if tool is Tool.ETHERPAD:
        if mode in (CanvasMode.INDEPENDENT, CanvasMode.MODERATOR_ONLY):
            return mode
        return CanvasMode.COLLABORATIVE
    return CanvasMode.MODERATOR_ONLY if mode is CanvasMode.MODERATOR_ONLY else CanvasMode.INDEPENDENT
```

tags: [obligatorio]

### Comando: Lint para detectar stringly-typed

```bash
# Java
mvn verify -DskipTests -Derrorprone   # Error Prone (StringEquality, StringLiteralEquals)
mvn checkstyle:check                  # Checkstyle illegalType

# JavaScript/TypeScript
eslint src/ --rule 'no-string-literal: error'

# Python
uv run ruff check .                   # incluye detección de comparación de literales

# Rust
cargo clippy
```

Estos linters forman parte del gate `make lint` (regla 01) y del pre-commit (regla 10).

tags: [opcional]

### Restriccion: Restricciones

- **Prohibido comparar con strings mágicos** en lógica de decisión: `"X".equals(y)`, `y == "X"`, `switch` sobre `String` con literales de dominio.
- **Prohibido pasar strings sueltos entre capas** cuando representan un dominio cerrado (estado, categoría, modo, tipo). Modelar con enum/tipo fuerte en la frontera de la capa.
- **Los enums encapsulan los valores válidos.** Si hay lógica de transformación (normalización, mapeo), vive en el enum (método) o en una función tipada, nunca en cadenas dispersas.
- **Evitar `null` como valor mágico** para representar "sin valor". Usar `Optional<T>` o un enum con valor explícito (p.ej. `UNKNOWN`, `DEFAULT`).
- **No introducir el anti-patrón en nuevos componentes** aunque el código legacy lo tenga. Refactorizar progresivamente al tocar el módulo.
- **El lint (Error Prone/ESLint/ruff/clippy) debe ejecutarse en CI** y en pre-commit para bloquear la regresión.

tags: [obligatorio]

### Referencia: Referencias

- [Regla 02: Arquitectura](02-architecture_draft.md) — tipos fuertes en los límites de dominio/aplicación.
- [Regla 03: Testing](03-testing_draft.md) — tests facilitados por tipos fuertes.
- [Regla 01: Build Tooling](01-build-tooling.md) — `make lint` integra los linters.
- [Error Prone](https://errorprone.info/)
- [ESLint](https://eslint.org/)
- [ruff](https://docs.astral.sh/ruff/)
- [Clippy](https://github.com/rust-lang/rust-clippy)

tags: [obligatorio]

### Plantilla: Plantillas

- [templates/rule-template.md.tmpl](../templates/rule-template.md.tmpl) — esqueleto para crear reglas con este esquema.

tags: [opcional]
