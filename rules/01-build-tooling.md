# Regla 01: Herramientas de Construcción

## Premisa

Todo proyecto debe tener un sistema de construcción declarativo y reproducible, independientemente del lenguaje.

La regla principal es responsabilidad única en la capa de build: el `Makefile` orquesta objetivos y variables, y la lógica específica vive en helpers reutilizables.

## Regla Base

- `Makefile` es la puerta de entrada universal para construir, testear y limpiar.
- El `Makefile` no implementa lógica compleja por lenguaje.
- La lógica de compilación/ejecución vive en archivos de helpers (`.mk`, `sh`/`bash`, `python`).
- Los scripts de helpers siempre reciben parámetros por flags.
- La construcción debe ejecutarse en contenedores cuando sea posible para no ensuciar el host local.
- `Justfile` es task manager de operativas de aplicación (acciones de negocio/operación), no de compilación.

## Arquitectura Recomendada

Estructura sugerida:

```text
.
├── Makefile
└── helpers/
	├── mk/
	│   ├── java.mk
	│   ├── python.mk
	│   ├── javascript.mk
	│   └── rust.mk
	├── shell/
	│   ├── java.sh (o java.bash)
	│   ├── python.sh (o python.bash)
	│   ├── javascript.sh (o javascript.bash)
	│   └── rust.sh (o rust.bash)
	└── python/
		└── *.py
```

Flujo recomendado (aplica a cualquier lenguaje):

1. `Makefile` recibe parámetros y define variables (`BUILD_TOOL`, `MODULE`, `PROFILE`, etc.).
2. `Makefile` incluye `helpers/mk/{lenguaje}.mk`.
3. `helpers/mk/{lenguaje}.mk` delega en `helpers/shell/{lenguaje}.sh` o `helpers/shell/{lenguaje}.bash`.
4. El helper shell o python ejecuta la herramienta nativa según flags (`--tool ...`).

## Matriz por Lenguaje

El patrón es el mismo para Java, Python, JavaScript y Rust:

- Java: `LANG=java`, `BUILD_TOOL=maven|gradle`, helper en `helpers/mk/java.mk`.
- Python: `LANG=python`, `BUILD_TOOL=uv|poetry|pip`, helper en `helpers/mk/python.mk`.
- JavaScript: `LANG=javascript`, `BUILD_TOOL=npm|pnpm|yarn`, helper en `helpers/mk/javascript.mk`.
- Rust: `LANG=rust`, `BUILD_TOOL=cargo`, helper en `helpers/mk/rust.mk`.

Ejemplos de invocación:

```bash
make build LANG=java BUILD_TOOL=maven MODULE=api PROFILE=dev
make test LANG=python BUILD_TOOL=uv MODULE=service PROFILE=ci
make build LANG=javascript BUILD_TOOL=pnpm MODULE=web PROFILE=dev
make test LANG=rust BUILD_TOOL=cargo MODULE=core PROFILE=ci
```

## Contrato de Flags en Helpers

- Evitar parámetros posicionales ambiguos.
- Usar flags explícitos y estables.
- Validar flags obligatorios y fallar rápido con mensaje claro.
- Incluir logging de auditoría en toda ejecución de helper.

## Auditoría y Logging (Obligatorio)

Todo helper (`sh`, `bash` o `python`) debe escribir log de ejecución.

Política de ruta:

1. Intentar escribir en `/var/log/<nombre-proyecto>/`.
2. Si no hay permisos, usar fallback en `/tmp/<nombre-proyecto>/`.
3. Nombre de archivo recomendado: `log-<script>-<timestamp>.log`.

Contrato mínimo de flags para helpers:

- `--log-file <ruta>` obligatorio.
- Opcionalmente `--log-level <nivel>` según necesidad del proyecto.

Ejemplo:

```bash
bash helpers/shell/java.bash --tool maven --goal package --skip-tests --log-file /var/log/my-api/log-java-20260807T120000Z.log
sh helpers/shell/javascript.sh --tool pnpm --goal test --module web --log-file /tmp/my-api/log-javascript-20260807T120000Z.log
sh helpers/shell/rust.sh --tool cargo --goal build --module core --log-file /var/log/my-api/log-rust-20260807T120000Z.log
python3 helpers/python/release.py --version 1.2.0 --dry-run --log-file /tmp/my-api/log-release-20260807T120000Z.log
```

## Estándares por Tipo de Script

### Shell helpers

- Permitido: `sh` o `bash`.
- Recomendado: `bash` cuando haya parsing de flags, arrays o validaciones más ricas.

### Python helpers

- Requerido: Python 3.11 o superior.
- Dependencias gestionadas con `uv`.
- Ubicación sugerida: `helpers/python/`.

Ejemplo de ejecución:

```bash
uv run python helpers/python/my_helper.py --flag value
```

## Objetivos Mínimos del Makefile

Todo proyecto debe exponer al menos:

```text
make build
make test
make clean
make docs
```

Opcionales frecuentes:

```text
make lint
make format
make serve
make ci
make image
```

## Build en Contenedor (Recomendado por Defecto)

Para mantener el host limpio y lograr reproducibilidad:

- Detectar runtime disponible: `podman` o `docker`.
- Construir imagen de CI para el proyecto.
- Ejecutar build/test dentro del contenedor montando el workspace.
- Publicar artefactos en rutas estándar del proyecto (`target/`, `dist/`, etc.).

Ejemplo de flujo:

```bash
make image LANG=java BUILD_TOOL=maven
make ci LANG=java BUILD_TOOL=maven
```

Artefactos típicos a generar:

- Java: `target/*.class`, `target/*.jar`
- Python: `dist/*`, `build/*`, `*.pyc`
- JavaScript: `dist/*`, `build/*`
- Rust: `target/release/*`

## Herramientas Complementarias

### Makefile
- Clásica, universal, disponible en prácticamente todos los sistemas
- Ideal para orquestación declarativa
- Usar para: build, test, clean, docs, lint, format

### Justfile
- Sintaxis más moderna que Makefile
- Punto de control para tareas operativas (ejemplo: `just create-user`, `just login`, `just db-create`)
- Puede invocar `make` cuando una operación necesite artefactos o CI
- Debe delegar operativas en `helpers/just/*.just`

### Relación de Responsabilidad (Obligatoria)

- Flujo permitido: `Justfile -> helpers/just -> shell/python/binarios`.
- Flujo permitido: `Justfile -> Makefile`.
- Flujo prohibido: `Makefile -> Justfile`.
- La capa de build/artefactos pertenece a Makefile; la capa de tareas operativas pertenece a Justfile.

Ejemplo de flujo operativo:

```text
just create-user --username alice --email alice@example.com
	-> helpers/just/app.just:create-user
		-> helpers/shell/app.bash o helpers/python/app.py
			-> ejecuta jar / npm run / binario generado por CI
```

### npm scripts / cargo / gradle / maven
- Se ejecutan detrás de `make` (directamente o vía helpers)
- Mantener un único punto de entrada para agentes y humanos

### uv / poetry / pip
- Para proyectos Python, exponer igual un objetivo `make` y delegar en helpers
- Si se usa Python helper, ejecutar con Python 3.11+ y dependencias gestionadas por `uv`

## Plantilla

Ver [templates/Makefile.tmpl](../templates/Makefile.tmpl) y [templates/Justfile.tmpl](../templates/Justfile.tmpl).
