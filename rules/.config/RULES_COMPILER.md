# Rules Compiler — Definición Interna del Compilador de Reglas y AST

> **Interno**: este documento define el esquema de las reglas, el compilador y el AST. No es una regla expuesta a proyectos consumidores; es la definición técnica de cómo se crean y validan las reglas aquí. Vive en `rules/.config/RULES_COMPILER.md` (excluido del validador de reglas).

## 1. Taxonomía de Tipos de Bloque

Cada regla se compone de **bloques tipados**. Un bloque se define por su encabezado `### Tipo: Nombre`, contenido y tags opcionales al final.

### Tipos obligatorios (toda regla los necesita)

| Tipo | Encabezado canónico | Propósito | Ejemplo |
|---|---|---|---|
| **Premisa** | `### Premisa: <nombre>` | Por qué existe la regla, qué garantiza. Contenido en bloque de cita `>`. | `### Premisa: El Makefile orquesta la construcción` |
| **Restriccion** | `### Restriccion: <nombre>` | Qué **NO** se debe hacer. Prohibiciones explícitas. | `### Restriccion: Makefile nunca ejecuta comandos directos` |
| **Ejemplo** | `### Ejemplo: <nombre>` | Código/configuración correcta. Al menos un bloque de código con lenguaje. | `### Ejemplo: Invocación multi-lenguaje` |
| **Referencia** | `### Referencia: <nombre>` | Enlaces a plantillas, otras reglas, documentación externa. | `### Referencia: Reglas relacionadas` |

### Tipos opcionales

| Tipo | Propósito |
|---|---|
| **Estructura** | Tree de directorios (```) |
| **Diagrama** | MermaidJS (```mermaid) |
| **Comando** | Comando canónico (```shell) |
| **Nombre Sugerido** | Convenciones de naming |
| **Plantilla** | Enlaces a templates asociados |
| **Comportamiento** | Flujo, regla de responsabilidad o patrón de delegación |
| **Sugerencia** | Recomendación no obligatoria |
| **Flujo** | Secuencia de operaciones |
| **Contrato** | Tabla de flags/contratos obligatorios |
| **Matriz** | Tabla comparativa (por lenguaje, herramienta o dominio) |

### Tag de bloque

Cada bloque puede cerrar con una línea `tags:` que indica si es obligatorio u opcional, y tags temáticos libres:

```
tags: [obligatorio, build, quality]
```

Vocabulario de tags: `obligatorio`, `opcional`, `recomendado`, `deprecado` + temáticos libres (`build`, `ci`, `cd`, `security`, `local`, `shell`, `python`, etc.).

## 2. Esquema Determinista del Bloque

### Sintaxis

```
### Premisa: El Makefile orquesta la construcción

> El Makefile es la **puerta de entrada universal**.
> No implementa lógica compleja por lenguaje.

```shell
# Ejemplo de uso
make build LANG=java BUILD_TOOL=maven
```

tags: [obligatorio, build]
```

### Reglas de parseo (deterministas)

1. **Encabezado**: `^#{2,6}\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*):\s+(.+)$` — el tipo DEBE ser canónico (capitalizado, palabra exacta de la taxonomía), seguido de `:` y un nombre no vacío.
2. **Contenido**: todo entre este encabezado y el siguiente encabezado de tipo (o el final del archivo, o un `##`/`#`) es contenido del bloque.
3. **Tags**: opcionales, al final del bloque: `^tags:\s*\[(.+)\]$`. Valores separados por coma. Si no hay tags, se considera implícito.
4. **Nivel**: recomendado uniforme `###` (H3) para consistencia, pero el patrón funciona con cualquier nivel `##`–`####`.

### Bloque sin tags

Si un bloque no tiene la línea `tags:`, el validador lo acepta (no es error). Los tags son una guía adicional para la IA y el auditor.

## 3. Esquema AST (Abstract Syntax Tree)

El compilador `rules_compiler.py` produce este AST al parsear una regla:

```json
{
  "id": "build-tooling",
  "title": "Herramientas de Construcción",
  "status": "Definida",
  "tags": ["build", "tooling", "makefile"],
  "heading": "Regla 01: Herramientas de Construcción",
  "blocks": [
    {
      "type": "premisa",
      "name": "El Makefile orquesta la construcción",
      "content": "> El Makefile es la **puerta de entrada universal**...\n\n```shell\nmake build LANG=java BUILD_TOOL=maven\n```",
      "tags": ["obligatorio", "build"]
    }
  ]
}
```

### Campos del AST

| Campo | Descripción |
|---|---|
| `id` | Identificador único (`frontmatter → id`) |
| `title` | Título descriptivo (`frontmatter → title`) |
| `status` | `Definida` o `Borrador` |
| `tags` | Tags del frontmatter |
| `heading` | Título H1 de la regla (`# Regla NN: Título`) |
| `blocks[]` | Lista de bloques tipados: `{type, name, content, tags}` |

## 4. Compilador `helpers/python/rules_compiler.py`

Motor determinista que opera sobre las reglas. Reutiliza `helpers/python/lib/`.

### Acciones

| `--action` | Input | Output | Función |
|---|---|---|---|
| `parse` | `rules/NN-topic.md` | AST (JSON por stdout) | Extrae frontmatter + título + bloques tipados |
| `validate` | `rules/NN-topic.md` (o `all`) | Reporte (líneas + exit code) | Valida el AST: whitelist de 14 tipos, nombre, contenido, tags, madurez, presencia. **Motor determinista de validación.** |
| `render` | AST o `rules/NN-topic.md` | Markdown normalizado (stdout o in-place) | Reescribe el markdown aplicando la guía de formato: negritas, tablas, code fences con lenguaje, mermaid, `<mark>`. |
| `new` | `--slug nn-topic --title "..." --log-file ...` | Crea `rules/NN-topic.md` | Genera una regla nueva desde la plantilla `templates/rule-template.md.tmpl`, aplicando la guía de formato. |

### Uso

```bash
# Parsear una regla a AST
uv run python helpers/python/rules_compiler.py --action parse 01-build-tooling

# Validar todas las reglas (motor determinista)
uv run python helpers/python/rules_compiler.py --action validate --all

# Renderizar una regla al formato normalizado
uv run python helpers/python/rules_compiler.py --action render 01-build-tooling --in-place

# Generar una regla nueva
uv run python helpers/python/rules_compiler.py --action new --slug 17-nueva --title "Nueva Regla"
```

### Integración con validador

`validate-rules.sh` (bash) orquesta y delega en el compilador para la validación de bloques tipados:

```bash
# wrapper bash → compilador
uv run python helpers/python/rules_compiler.py --action validate --all
```

El compilador reemplaza el chequeo por `grep "^## Sección"` con el motor determinista del AST. Los demás chequeos (frontmatter, enlaces entre reglas, enlaces a templates, sincronía, capa helpers) permanecen en el wrapper bash.

## 5. Guía de Formato Markdown

Estas convenciones las aplica el compilador en `--action render` y están documentadas como comentarios en `templates/rule-template.md.tmpl` para que los agentes de IA las sigan.

| Elemento | Sintaxis | Cuándo usarlo |
|---|---|---|
| **Negrita** | `**concepto clave**` | Términos importantes, nombres propios de herramientas, prohibiciones fuertes |
| *Cursiva* | `*énfasis*` | Énfasis secundario, definiciones |
| `` `código` `` | `` `comando` `` | Comandos, nombres de archivo, flags, variables |
| Code fence con lenguaje | ` ```python `, ` ```shell `, ` ```mermaid ` | Código ejecutable, diagramas |
| Tablas GFM | `| A | B |` `|-|-|` `| x | y |` | Comparativas, contratos, matrices |
| `<mark>` | `<mark>texto</mark>` | Hitos críticos (poco frecuente) |
| Cita `>` | `> texto` | Descripción de premisas, restricciones, sugerencias |
| Encabezados `###` | `### Tipo: Nombre` | Definir bloques tipados |

## 6. Madurez por Estado

| Estado | Requisitos mínimos de bloques | Requisitos adicionales |
|---|---|---|
| **Definida** | ≥1 `Premisa`, `Restriccion`, `Ejemplo`, `Referencia` | ≥1 `Comando` + ≥1 (`Estructura` o `Diagrama`) |
| **Borrador** | ≥1 `Premisa`, `Restriccion`, `Ejemplo`, `Referencia` | Ninguno |

### Chequeos del validador

1. **Tipo válido**: cada bloque debe usar uno de los 14 tipos de la taxonomía (error si no).
2. **Nombre presente**: el nombre tras `:` no puede estar vacío.
3. **Contenido no vacío**: entre encabezado y siguiente tipo debe haber contenido (texto, código, tabla…).
4. **Tags válidos**: si hay línea `tags:`, los valores deben estar en `obligatorio|opcional|recomendado|deprecado` o ser temáticos libres (warning si ambiguo).
5. **Presencia de tipos obligatorios**: deben existir al menos los requeridos por la madurez.
