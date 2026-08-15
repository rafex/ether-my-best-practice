---
id: secrets
title: Gestión de Secretos
status: Definida
tags: [secrets, security, sops, age, encryption, gitleaks, trufflehog]
checksum: f915ce0f59e20f78d9e9e897a16b43fba14113041a20651c7a0bf17fc8de2876
---

# Regla 13: Gestión de Secretos



### Premisa: Premisa

Ningún secreto viaja en plano en el repositorio. Todo secreto (claves de API, contraseñas de base de datos, tokens, certificados) se cifra con **sops + age** en archivos `.secrets/secrets.<env>.enc.yaml`. La clave privada age vive en el host del desarrollador (`~/.age/<proyecto>-key.txt`) y **nunca** se versiona. Solo los `*.enc.yaml` cifrados se suben al repositorio. Los hooks `pre-commit` (gitleaks) y `pre-push` (trufflehog) bloquean cualquier secreto en plano que intente llegar al historial. Las variables de entorno (`.env.dev`, `.env.prod`, `.env.int`) se generan bajo demanda con `just env <entorno>` y nunca se versionan.

tags: [obligatorio]

### Estructura: Estructura

### Componentes del sistema de secretos y variables de entorno

```
proyecto/
├── .enviroments/                           # variables de entorno (SIN secretos)
│   ├── .gitignore                          # evita subir .env-* con secretos
│   ├── .env.example                        # plantilla (versionable, sin valores)
│   ├── .env.dev                            # (generado por just env dev)
│   ├── .env.test
│   └── .env.prod
├── .env → .enviroments/.env.dev            # symlink (apunta al entorno activo)
├── .secrets/                               # secretos cifrados (solo *.enc.yaml versionados)
│   ├── .gitkeep
│   ├── secrets.dev.enc.yaml                # cifrado con sops+age
│   ├── secrets.prod.enc.yaml
│   └── secrets.int.enc.yaml
├── .sops.yaml                              # configuración de sops (age recipients públicos)
│
├── helpers/
│   └── shell/
│       ├── secrets.sh                      # wrapper: edit, env, verify, keygen
│       └── env.sh                          # merge de secretos + variables, symlink
│
├── Justfile                                # recipes: edit-secrets, env, env-link, env-merge
└── ~/.age/<proyecto>-key.txt               # clave privada age (FUERA del repo, nunca versionada)
```

### Flujo de operación

```
just keygen               → age-keygen -o ~/.age/<proyecto>-key.txt
                              Añadir clave pública a .sops.yaml

just edit-secrets dev     → secrets.sh --action edit --env dev
                              Abre $EDITOR (vi), al guardar → sops edit encripta

just env dev              → secrets.sh --action env --env dev
                              sops decrypt → .enviroments/.env.dev

just env-link dev         → env.sh --action link --env dev
                              .env → .enviroments/.env.dev (symlink)

just env-merge dev        → env.sh --action merge --env dev
                              merge YAML desencriptado + variables del proceso

git commit                → pre-commit: gitleaks git --staged
                              + doble-check de .env/secretos en plano

git push                  → pre-push: trufflehog git file://.
                              Bloquea el push si hay secretos en el historial
```

tags: [opcional]

### Comportamiento: Merge de secretos + variables de entorno

Las aplicaciones suelen buscar el archivo `.env` en la raíz para cargar su configuración. El estándar usa un **symlink** `.env → .enviroments/.env.<entorno>` para controlar qué entorno está activo, y un helper de **merge** que combina las variables no-secretas (`.enviroments/`) con los secretos desencriptados (`.secrets/`).

1. **`secrets.sh --action env <env>`** desencripta `.secrets/secrets.<env>.enc.yaml` y genera `.enviroments/.env.<env>` con las variables **no-secretas**.
2. **`env.sh --action merge <env>`** combina el YAML desencriptado + las variables de entorno del proceso, generando el `.env.<env>` final en runtime.
3. **`env.sh --action link <env>`** actualiza el symlink `.env → .enviroments/.env.<env>`.
4. Las aplicaciones leen `.env` (symlink), que apunta al entorno activo.

**Precedencia en el merge:** si un secreto (de `.secrets/`) y una variable pública (de `.enviroments/`) tienen el mismo nombre, **el secreto gana**. El helper de merge **lanza un warning mostrando el valor de la variable pública que se perdió** (el secreto **nunca** se imprime en logs).

tags: [obligatorio]

### Contenido de `.sops.yaml`

```yaml
creation_rules:
  - age:
      - age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Contenido de `secrets.prod.enc.yaml` (después de `just edit-secrets prod`)

```yaml
DATABASE_URL: postgresql://user:pass@host:5432/db
API_KEY: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
REDIS_URL: redis://host:6379/0
```

### Hook pre-commit con gitleaks

```bash
# En hooks.sh --action pre-commit:
if command -v gitleaks >/dev/null 2>&1; then
    echo "Running secret scan: gitleaks git --staged..."
    gitleaks git --staged
else
    echo "WARNING: gitleaks no instalado."
fi
```

### Hook pre-push con trufflehog

```bash
# En hooks.sh --action pre-push:
if command -v trufflehog >/dev/null 2>&1; then
    echo "Running secret scan: trufflehog git file://. ..."
    trufflehog git file://. --no-verification --fail
else
    echo "WARNING: trufflehog no instalado."
fi
```

tags: [opcional]

### Nombre Sugerido: Nombres Sugeridos

- **Carpeta de variables de entorno:** `.enviroments/` en raíz del repositorio.
- **Archivos de entorno:** `.env.example` (plantilla versionable), `.env.dev`, `.env.test`, `.env.prod` — con punto, como en el estándar actual.
- **Symlink activo:** `.env → .enviroments/.env.<entorno>` (no versionado).
- **Carpeta de secretos:** `.secrets/` en raíz del repositorio.
- **Archivos cifrados:** `secrets.<env>.enc.yaml` (dev, prod, int, staging...).
- **Clave age:** `~/.age/<proyecto>-key.txt` (nombre del repositorio en kebab-case).
- **Configuración sops:** `.sops.yaml` en raíz.
- **Helpers:** `secrets.sh` (edit/env/verify/keygen), `env.sh` (link/merge/verify).

tags: [opcional]

### Comando: Comandos

### Generar clave age (una vez por máquina)

```bash
age-keygen -o ~/.age/<proyecto>-key.txt
age-keygen -y ~/.age/<proyecto>-key.txt   # copiar la clave pública a .sops.yaml
```

O vía Just:

```bash
just keygen            # → secrets.sh --action keygen
```

### Editar secretos (encripta al guardar)

```bash
just edit-secrets dev
just edit-secrets prod
just edit-secrets int
# → secrets.sh --action edit --env <env>
# → sops edit .secrets/secrets.<env>.enc.yaml
```

### Generar `.env.<entorno>`

```bash
just env dev          # → genera .enviroments/.env.dev desde secrets.dev.enc.yaml
just env prod         # → genera .enviroments/.env.prod
```

### Activar entorno (symlink .env)

```bash
just env-link dev     # → .env → .enviroments/.env.dev
just env-link prod    # → .env → .enviroments/.env.prod
```

### Merge de secretos + variables

```bash
just env-merge dev    # → combina YAML desencriptado + variables del proceso
```

### Verificar que no hay secretos en plano

```bash
just secrets-verify
# → gitleaks git --staged (si instalado)
```

### Flujo completo de primer uso

```bash
# 1. Generar clave age
just keygen
# → clave pública copiada de la salida

# 2. Configurar .sops.yaml con la clave pública (editar manual o just cz-init)
# Reemplazar el placeholder en .sops.yaml

# 3. Crear secretos para dev
just edit-secrets dev
# → abrir vi, rellenar, guardar → encriptado

# 4. Generar .env.dev (para desarrollo local)
just env dev
```

tags: [opcional]

### Ejemplo: Ejemplos

### `.secrets/secrets.dev.enc.yaml` (cifrado, versionable)

```yaml
DATABASE_URL: ENC[AES256_GCM,data:...]
API_KEY: ENC[AES256_GCM,data:...]
REDIS_URL: ENC[AES256_GCM,data:...]
sops:
    kms: []
    gcp_kms: []
    azure_kv: []
    hc_vault: []
    age:
        - recipient: age1s3cqcks5genc6ru8chl0hkkd04zmxvczsvdxq99ekffe4gmvjpzsedk23c
          enc: |
            -----BEGIN AGE ENCRYPTED FILE-----
            ...
            -----END AGE ENCRYPTED FILE-----
    lastmodified: "2026-08-07T12:00:00Z"
    mac: ENC[AES256_GCM,data:...]
```

### `.env.example` (versionable, sin valores)

```bash
# Plantilla de variables de entorno. Los valores se obtienen descifrando
# .secrets/secrets.<env>.enc.yaml con just env <env>.
DATABASE_URL=
API_KEY=
REDIS_URL=
```

### Resultado de `just env dev`

```bash
# .env.dev (generado, nunca versionado)
DATABASE_URL=postgresql://user:pass@localhost:5432/devdb
API_KEY=sk-dev-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
REDIS_URL=redis://localhost:6379/0
```

tags: [obligatorio]

### Restriccion: Restricciones

- **Nunca versionar la clave privada age** (`~/.age/<proyecto>-key.txt`). Cada desarrollador genera su propia clave y añade su clave pública a `.sops.yaml`.
- **Nunca versionar `.env`, `.env.*` ni `.enviroments/.env.*`.** Estos se generan con `just env <entorno>` y están en `.gitignore`. La plantilla `.env.example` (sin valores) y `.enviroments/.gitignore` sí se versionan.
- **Los `.env.*` en `.enviroments/` NUNCA contienen secretos.** Si una variable es secreta, va en `.secrets/`; el merge la inyecta en runtime. Los valores no-secretos (públicos) sí pueden estar en `.enviroments/`.
- **Nunca versionar secretos en plano** en archivos YAML, JSON, properties, `.env`, código fuente ni ningún otro formato. Todo secreto debe pasar por `sops edit` y vivir en `.secrets/*.enc.yaml`.
- **El symlink `.env` no se versiona** (está en `.gitignore`). Apunta a `.enviroments/.env.<entorno>` y se gestiona con `env.sh --action link`.
- **Merge con precedencia:** si un secreto y una variable pública tienen el mismo nombre, **el secreto gana**. El helper de merge lanza un warning mostrando el valor de la variable pública perdida (el secreto **nunca** se imprime).
- **Doble-check:** `pre-commit` (gate) y `commit-msg` (validación dura) rechazan `.env`, `.env.*` con contenido, o secretos sin cifrar staged.
- **`gitleaks git --staged` se ejecuta en pre-commit** y bloquea el commit si detecta secretos en los archivos staged.
- **`trufflehog git file://.` se ejecuta en pre-push** y bloquea el push si hay secretos en cualquier parte del historial.
- **Solo los archivos `*.enc.yaml` dentro de `.secrets/` se versionan.** Cualquier otro `.yaml`, `.yml` o `.json` en `.secrets/` es ignorado por git.
- **`just edit-secrets <env>` es la ÚNICA forma de modificar secretos.** No se editan los `.enc.yaml` a mano; `sops edit` abre el editor, y al guardar cifra automáticamente.
- **`sops` y `age` deben estar instalados en el entorno de desarrollo.** La instalación se documenta en `hooks.sh install` y puede automatizarse.
- **Las claves age son por máquina, no por repositorio compartido.** Si un nuevo desarrollador se une al proyecto, genera su clave age y añade su clave pública a `.sops.yaml`.
- **Si un secreto se sube en plano por accidente, rotarlo inmediatamente** y eliminarlo del historial (esto implica revocar la clave/token real, no solo borrar el commit).

tags: [obligatorio]

### Referencia: Referencias

- [Regla 10: Git Hooks](10-githooks.md) — gates de pre-commit y pre-push donde se integran gitleaks y trufflehog.
- [Regla 12: Gitignore](12-gitignore.md) — `.gitignore.secretos.tmpl` con exclusiones de `.env.*`, `.secrets/*.yaml`, claves.
- [Regla 01: Build Tooling](01-build-tooling.md) — helpers como capa única de ejecución (secrets.sh).
- [Regla 05: Control de Versiones](05-version-control_draft.md) — Conventional Commits aplican a cambios en `.sops.yaml` y `.secrets/`.
- [sops + age documentation](https://getsops.io/)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [trufflehog](https://github.com/trufflesecurity/trufflehog)
- [templates/repository-structure/.config/sops/.sops.yaml.tmpl](../templates/repository-structure/.config/sops/.sops.yaml.tmpl)
- [templates/helpers/shell/secrets.sh.tmpl](../templates/repository-structure/helpers/shell/secrets.sh.tmpl)
- [templates/helpers/shell/env.sh.tmpl](../templates/repository-structure/helpers/shell/env.sh.tmpl)
- [templates/gitignore/.gitignore.secretos.tmpl](../templates/gitignore/.gitignore.secretos.tmpl)

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/repository-structure/.config/sops/.sops.yaml.tmpl](../templates/repository-structure/.config/sops/.sops.yaml.tmpl)
- [templates/repository-structure/.secrets/](../templates/repository-structure/.secrets/)
- [templates/repository-structure/.enviroments/](../templates/repository-structure/.enviroments/)
- [templates/helpers/shell/secrets.sh.tmpl](../templates/repository-structure/helpers/shell/secrets.sh.tmpl)
- [templates/helpers/shell/env.sh.tmpl](../templates/repository-structure/helpers/shell/env.sh.tmpl)
- [templates/gitignore/.gitignore.secretos.tmpl](../templates/gitignore/.gitignore.secretos.tmpl)

tags: [opcional]
