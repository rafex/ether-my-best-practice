---
id: script-reuse
title: Reutilización de Scripts (Librerías Comunes)
status: Definida
tags: [scripts, libraries, reuse, helpers, shell, python, commons]
---

# Regla 15: Reutilización de Scripts (Librerías Comunes)



### Premisa: Premisa

La lógica común de los helpers debe centralizarse en librerías reutilizables (`helpers/shell/lib/` y `helpers/python/lib/`). Una función independizada es **máxima reutilización**: se escribe una vez, se usa desde cualquier helper, y cualquier mejora impacta a todos los consumidores. Los helpers ejecutables **nunca duplican** lógica que ya existe en `lib/`. Cada función tiene una sola responsabilidad y es independiente del contexto del proyecto.

tags: [obligatorio]

### Estructura: Estructura

### Árbol de librerías

```
helpers/
├── shell/
│   ├── lib/
│   │   ├── commons.sh       # entorno base, parse_flags, utilidades
│   │   ├── logs.sh           # init_log, log_info/warn/error/debug
│   │   ├── colors.sh         # ANSI COLOR_* + colorize()
│   │   ├── messages.sh       # success/error/warning/info/step/die/header
│   │   └── try-catch.sh      # run_with_guard, catch, fail_fast, trap ERR
│   ├── hooks.sh              # (helper ejecutable — sourcea libs)
│   ├── cz.sh
│   └── ...
│
└── python/
    ├── lib/
    │   ├── commons.py        # PROJECT_ROOT, argparse, utilidades
    │   ├── logs.py            # get_logger, RotatingFileHandler, fallback
    │   ├── colors.py          # ANSI + colorize()/supports_color()
    │   ├── messages.py        # success/error/warning/info/step/die/header
    │   └── exceptions.py      # @safe decorador, ErrorHandler context manager
    ├── changelog.py           # (helper ejecutable — importa libs)
    └── ...
```

### Cómo se conectan

**Shell:** los helpers ejecutables (`build.sh`, `cz.sh`, etc.) usan `source` para cargar las libs:

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"

init_log "mi-helper"
```

**Python:** los helpers ejecutables (`changelog.py`, `version.py`) importan las libs:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from lib.logs import get_logger
```

tags: [opcional]

### Nombre Sugerido: Nombres Sugeridos

- **Carpeta de librerías:** `helpers/shell/lib/`, `helpers/python/lib/` — en minúsculas, sin guiones, siempre `lib/`.
- **Nombres de módulos:** descriptivos del propósito: `commons`, `logs`, `colors`, `messages`, `try-catch` (shell), `commons`, `logs`, `colors`, `messages`, `exceptions` (python). Snake_case para python (`exceptions.py`, no `try_catch.py`).
- **Funciones de log:** `init_log <script_name>` (shell), `get_logger <name>` (python). El parámetro identifica al script en el archivo de auditoría.
- **Funciones de mensajes:** `success/error/warning/info/step/die/header` — mismas firmas en ambos lenguajes.

tags: [opcional]

### Comando: Comandos

### Shell: sourcear libs y usar funciones

```bash
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/commons.sh"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/colors.sh"
source "$SCRIPT_DIR/lib/messages.sh"
source "$SCRIPT_DIR/lib/try-catch.sh"

# Parsear flags
parse_common_flags "$@"

# Inicializar log
init_log "mi-helper"

# Usar mensajes
step 1 3 "Validando configuración..."
info "Todo correcto"
success "Proceso completado"
```

### Python: importar libs y usar funciones

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from lib.commons import add_common_args, ensure_dir
from lib.logs import get_logger
from lib.messages import success, error, step

log = get_logger("mi-helper")

step(1, 3, "Validando configuración")
success("Proceso completado")
```

tags: [opcional]

### Ejemplo: Ejemplos

### Antes (sin libs): bloque de log duplicado

```bash
# Cada helper repetía esto:
project_name="$(basename "$workspace")"
script_name="build"
ts="$(date -u +%Y%m%dT%H%M%SZ)"
if [[ -z "$log_file" ]]; then
    if mkdir -p "/var/log/$project_name" 2>/dev/null ...
fi
mkdir -p "$(dirname "$log_file")"
exec > >(tee -a "$log_file") 2>&1
echo "Audit log: $log_file"
```

### Después (con libs): una línea

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
init_log "build"
# Listo. log_file definido, tee activo, auditoría funcionando.
```

### Python sin y con libs

```python
# Antes: print + try/except manual
print("Error: algo falló")

# Después: logging + mensajes estandarizados
from lib.logs import get_logger
from lib.messages import error, success
log = get_logger("mi-helper")
success("Proceso completado")
```

### Extensión de libs

Agregar una nueva función a `commons.sh` o `logs.py` impacta **automáticamente** a todos los helpers que las sourcean/importan. Ejemplo: añadir `log_json <data>` a `logs.sh` → disponible en todos los helpers shell sin modificar ninguno.

tags: [obligatorio]

### Restriccion: Restricciones

- **Nunca duplicar lógica de lib en un helper ejecutable.** Si un bloque de código se repite en 2+ helpers, extraerlo a `lib/`.
- **Una función, una responsabilidad.** `init_log` inicializa el log, no parsea flags. `parse_common_flags` parsea flags, no inicializa el log. Cada función hace una cosa y la hace bien.
- **Independencia de contexto.** Las funciones de lib no hardcodean rutas de proyecto, nombres de directorios ni herramientas. Usan `PROJECT_ROOT`, `WORKSPACE`, `SCRIPT_DIR` o reciben parámetros explícitos.
- **Todo helper nuevo debe usar libs.** Cualquier helper creado a partir de ahora debe sourcear/importar las librerías comunes en lugar de implementar su propia lógica de logging, mensajes o errores.
- **Las libs son no ejecutables** (`source` en shell, `import` en python). No tienen `#!/bin/...` funcional ni `main()`. El punto de entrada son los helpers.
- **Las libs residen en `helpers/<lang>/lib/`** en el proyecto consumidor. Los templates fuente viven en `templates/repository-structure/helpers/<lang>/lib/`.

tags: [obligatorio]

### Comando: Sourcear libs en shell e importar en python

```bash
# Shell: sourcear libs
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/logs.sh"
source "$SCRIPT_DIR/lib/messages.sh"
init_log "mi-helper"
```

```python
# Python: importar libs
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from lib.logs import get_logger
from lib.messages import success, error
log = get_logger("mi-helper")
```

tags: [obligatorio]

### Referencia: Referencias

- [Regla 01: Build Tooling](01-build-tooling.md) — helpers como capa única de ejecución.
- [Regla 14: Archivos de Configuración](14-config-files.md) — configuración de herramientas.
- [templates/repository-structure/helpers/shell/lib/](../templates/repository-structure/helpers/shell/lib/)
- [templates/repository-structure/helpers/python/lib/](../templates/repository-structure/helpers/python/lib/)

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/repository-structure/helpers/shell/lib/commons.sh.tmpl](../templates/repository-structure/helpers/shell/lib/commons.sh.tmpl)
- [templates/repository-structure/helpers/shell/lib/logs.sh.tmpl](../templates/repository-structure/helpers/shell/lib/logs.sh.tmpl)
- [templates/repository-structure/helpers/shell/lib/colors.sh.tmpl](../templates/repository-structure/helpers/shell/lib/colors.sh.tmpl)
- [templates/repository-structure/helpers/shell/lib/messages.sh.tmpl](../templates/repository-structure/helpers/shell/lib/messages.sh.tmpl)
- [templates/repository-structure/helpers/shell/lib/try-catch.sh.tmpl](../templates/repository-structure/helpers/shell/lib/try-catch.sh.tmpl)
- [templates/repository-structure/helpers/python/lib/commons.py.tmpl](../templates/repository-structure/helpers/python/lib/commons.py.tmpl)
- [templates/repository-structure/helpers/python/lib/logs.py.tmpl](../templates/repository-structure/helpers/python/lib/logs.py.tmpl)
- [templates/repository-structure/helpers/python/lib/colors.py.tmpl](../templates/repository-structure/helpers/python/lib/colors.py.tmpl)
- [templates/repository-structure/helpers/python/lib/messages.py.tmpl](../templates/repository-structure/helpers/python/lib/messages.py.tmpl)
- [templates/repository-structure/helpers/python/lib/exceptions.py.tmpl](../templates/repository-structure/helpers/python/lib/exceptions.py.tmpl)

tags: [opcional]
