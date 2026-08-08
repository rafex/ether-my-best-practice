# Estructura de Repositorio (Monorepo Multi-Lenguaje)

Esta es la estructura de referencia para un proyecto generado con Ether Best Practices. Sigue arquitectura hexagonal y organiza el código fuente por **rol** (`backend`, `frontend`, `shared`) y **lenguaje** dentro de cada rol.

Los helpers (`helpers/`) constituyen la capa única de ejecución compartida: scripts de build, test, serve, lint, format, contenedores y operativas de aplicación.

## Árbol completo

```
proyecto/
├── Makefile                         # orquestación: build, test, ci
├── Justfile                         # operativas: serve, login, create-user, ...
├── .gitignore
├── VERSION                          # versión actual (bumpeada en release)
├── CHANGELOG.md                     # generado en release desde Conventional Commits
│
├── .config/                         # configuración de herramientas (regla 14)
│   ├── commitizen/
│   │   └── pyproject.toml           # [tool.commitizen] con version_files
│   ├── mkdocs/
│   │   ├── mkdocs.yml               # configuración del sitio (docs_dir: ../../docs)
│   │   └── requirements.txt         # dependencias de MkDocs
│   └── sops/
│       └── .sops.yaml               # age recipients públicos (cifrado sops+age)
│
├── .githooks/                       # git hooks (instalados con just hooks-install)
│   ├── .tools/                      # herramientas internas (commitizen-venv)
│   ├── pre-commit                   # → lint + gitleaks (gates antes de commit)
│   ├── pre-push                     # → test + trufflehog (gates antes de push)
│   └── commit-msg                   # → validar Conventional Commits
│
├── .secrets/                        # secretos cifrados con sops + age
│   ├── .gitkeep
│   └── secrets.{dev,prod,int}.enc.yaml  # solo los *.enc.yaml se versionan
│
├── docs/                            # documentación en Markdown + MermaidJS
│   ├── index.md
│   ├── architecture.md
│   ├── api.md
│   └── contributing.md
│
├── site/                            # (generado por mkdocs build) no se versiona
│
├── helpers/                         # capa única de ejecución
│   ├── mk/                          # módulos Makefile (build.mk, container.mk, docs.mk, ...)
│   ├── shell/                       # scripts shell (build.sh, test.sh, java.sh, container.sh, ...)
│   ├── python/                      # helpers python (opcional: lint.py, format.py, ...)
│   └── just/                        # operativas de aplicación (app.just, auth.just, ...)
│
├── containers/                      # definiciones de imágenes de contenedor
│   ├── Containerfile                # base: runtime mínimo (bash, curl, git)
│   ├── backend/Containerfile        # backend: JDK Temurin / Python / Rust runtime
│   ├── frontend/Containerfile       # frontend: Node.js LTS build + serve
│   ├── ci/Containerfile.ci          # CI: toolchain completo (build + test + lint)
│   └── cd/Containerfile             # CD: runtime ligero + herramientas de deploy
│
├── mcp/                             # configuración Model Context Protocol (opcional)
│   └── mcp-config.json
│
└── source/                          # código fuente por rol + lenguaje
    ├── backend/                     # aplicaciones y servicios backend
    │   ├── java/                    # Java con estructura Maven/Gradle
    │   │   └── <proyecto>/          # p.ej. "patos"
    │   │       ├── pom.xml          # Maven (o build.gradle si Gradle)
    │   │       └── src/
    │   │           ├── main/java/com/example/
    │   │           │   ├── domain/
    │   │           │   ├── application/
    │   │           │   ├── infrastructure/
    │   │           │   └── ports/
    │   │           ├── main/resources/
    │   │           └── test/java/com/example/
    │   │
    │   ├── python/                  # (si el backend es Python)
    │   │   └── <proyecto>/
    │   │       ├── pyproject.toml
    │   │       └── src/
    │   │
    │   └── rust/                    # (si el backend es Rust)
    │       └── <proyecto>/
    │           ├── Cargo.toml
    │           └── src/
    │
    ├── frontend/                    # aplicaciones web y clientes interactivos
    │   └── nodejs/                  # (o javascript/) Node.js / npm / pnpm
    │       └── <proyecto>/          # p.ej. "web"
    │           ├── package.json
    │           └── src/
    │               ├── components/
    │               └── pages/
    │
    └── shared/                      # código compartido entre roles
        └── libs/                    # (o domain/, contracts/, types/)
            └── <proyecto>/          # p.ej. "domain", "types"
                └── src/

```

## Principios

1. **Rol determina ubicación:** `backend/` contiene APIs y servicios; `frontend/` contiene interfaz de usuario; `shared/` contiene código usado por ambos.
2. **Lenguaje dentro del rol:** `source/backend/java/` vs `source/backend/python/`. Un mismo proyecto puede tener backend Java y frontend NodeJS.
3. **Nombre de proyecto en kebab-case:** `patos`, `web`, `domain`.
4. **Helpers en raíz:** la capa `helpers/` es compartida por todos los roles; nunca se duplica dentro de cada lenguaje.
5. **Hexagonal en cada backend:** bajo `source/backend/<lang>/<proyecto>/src/` se aplica la arquitectura de puertos y adaptadores (dominio, aplicación, infraestructura, puertos).
6. **Git hooks como gates:** `.githooks/` contiene gates puros (sin efectos laterales): lint antes de commit, test antes de push, validación de Conventional Commits. Instalar con `just hooks-install`.
7. **CHANGELOG y VERSION solo en release:** `VERSION` y `CHANGELOG.md` se actualizan exclusivamente con `just prepare-release <versión>`, nunca en hooks.
8. **Secretos cifrados con sops+age:** `.secrets/*.enc.yaml` son los únicos archivos de secretos versionables. La clave privada age vive en `~/.age/<proyecto>-key.txt` y nunca se sube. `just edit-secrets <env>` edita y encripta; `just env <env>` desencripta a `.env.<env>`. Gitleaks (pre-commit) + trufflehog (pre-push) bloquean secretos en plano.

## Ejemplo: proyecto "patos" (backend Java + frontend NodeJS + libs compartidas)

```
source/
├── backend/
│   └── java/
│       └── patos/
│           ├── pom.xml
│           └── src/
│               ├── main/java/com/patos/
│               │   ├── domain/                # entidades, servicios de dominio
│               │   ├── application/            # casos de uso, DTOs
│               │   ├── infrastructure/         # persistencia, web controllers
│               │   └── ports/                  # interfaces públicas
│               └── test/java/com/patos/
│
├── frontend/
│   └── nodejs/
│       └── web/
│           ├── package.json
│           └── src/
│               ├── components/
│               └── pages/
│
└── shared/
    └── libs/
        └── domain/
            └── src/
                └── (DTOs, tipos, contratos compartidos)
```

## Capas por rol y lenguaje

### Backend (Java / Python / Rust)

- `domain/` — lógica de negocio pura, entidades, value objects, servicios.
- `application/` — casos de uso que orquestan dominio.
- `infrastructure/` — implementaciones concretas (persistencia, HTTP, integraciones externas).
- `ports/` — interfaces públicas (puertos).

### Frontend (Node.js)

- `components/` — componentes reutilizables.
- `pages/` — páginas/rutas.
- `src/` también puede tener `hooks/`, `services/`, `types/` según el framework.

### Shared (libs)

- Código que ambos roles necesitan (DTOs, tipos TypeScript/Java records, contratos, validaciones).

## Biblioteca de .gitignore

Los templates de `.gitignore` por contexto viven en [templates/gitignore/](../gitignore/). Cada ubicación del proyecto arma su `.gitignore` tomando el template correspondiente:

| Ubicación en el proyecto | Template de referencia |
|---|---|
| Raíz (`proyecto/`) | `.gitignore.raiz.tmpl` |
| `source/backend/java/<proyecto>/` | `.gitignore.java.tmpl` |
| `source/backend/python/<proyecto>/` | `.gitignore.python.tmpl` |
| `source/backend/rust/<proyecto>/` | `.gitignore.rust.tmpl` |
| `source/frontend/nodejs/<proyecto>/` | `.gitignore.nodejs.tmpl` |
| `containers/` | `.gitignore.container.tmpl` |

**Complementos combinables** (el agente decide si añadirlos según el proyecto): `.gitignore.secretos.tmpl`, `.gitignore.temporales.tmpl`, `.gitignore.mcp.tmpl`.

## Referencias

- [Regla 01: Build Tooling](../rules/01-build-tooling.md) — Makefile, Justfile, helpers.
- [Regla 02: Arquitectura Hexagonal](../rules/02-architecture.md) — domain/application/infrastructure/ports.
- [Regla 08: Stack Tecnológico](../rules/08-stack.md) — versiones, Podman, Containerfile.
- [Regla 09: Estructura de Repositorio](../rules/09-repository-structure.md) — esta estructura como estándar.
- [Regla 10: Git Hooks](../rules/10-githooks.md) — prefieres, flujo de release.
