---
id: secrets
title: Gestión de Secretos
status: Definida
tags: [secrets, security, sops, age, encryption, gitleaks, trufflehog]
---

# Regla 13: Gestión de Secretos



### Premisa: Premisa

Ningún secreto viaja en plano en el repositorio. Todo secreto (claves de API, contraseñas de base de datos, tokens, certificados) se cifra con **sops + age** en archivos `.secrets/secrets.<env>.enc.yaml`. La clave privada age vive en el host del desarrollador (`~/.age/<proyecto>-key.txt`) y **nunca** se versiona. Solo los `*.enc.yaml` cifrados se suben al repositorio. Los hooks `pre-commit` (gitleaks) y `pre-push` (trufflehog) bloquean cualquier secreto en plano que intente llegar al historial. Las variables de entorno (`.env.dev`, `.env.prod`, `.env.int`) se generan bajo demanda con `just env <entorno>` y nunca se versionan.

tags: [obligatorio]

### Estructura: Estructura

### Componentes del sistema de secretos

```
proyecto/
├── .secrets/                               # secretos cifrados (solo *.enc.yaml versionados)
│   ├── .gitkeep
│   ├── secrets.dev.enc.yaml                # cifrado con sops+age
│   ├── secrets.prod.enc.yaml
│   └── secrets.int.enc.yaml
├── .sops.yaml                              # configuración de sops (age recipients públicos)
├── .env.example                            # plantilla de variables (sin valores, versionable)
│
├── helpers/
│   └── shell/
│       └── secrets.sh                      # wrapper: edit, env, verify, keygen
│
├── Justfile                                # recipes: edit-secrets, env, secrets-verify
└── ~/.age/<proyecto>-key.txt               # clave privada age (FUERA del repo, nunca versionada)
```

### Flujo de operación

```
just keygen               → age-keygen -o ~/.age/<proyecto>-key.txt
                              Añadir clave pública a .sops.yaml

just edit-secrets dev     → secrets.sh --action edit --env dev
                              Abre $EDITOR (vi), al guardar → sops edit encripta

just env dev              → secrets.sh --action env --env dev
                              sops decrypt → genera .env.dev (ignorado por git)

git commit                → pre-commit: gitleaks git --staged
                              Bloquea el commit si detecta secretos en plano

git push                  → pre-push: trufflehog git file://.
                              Bloquea el push si hay secretos en el historial
```

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

- **Carpeta de secretos:** `.secrets/` en raíz del repositorio.
- **Archivos cifrados:** `secrets.<env>.enc.yaml` (dev, prod, int, staging...).
- **Clave age:** `~/.age/<proyecto>-key.txt` (nombre del repositorio en kebab-case).
- **Configuración sops:** `.sops.yaml` en raíz.
- **Envs generados:** `.env.<env>` (dev, prod, int) — ignorados por git.
- **Plantilla versionable:** `.env.example` (sin valores, solo nombres de variables).

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
just env dev          # → genera .env.dev desde secrets.dev.enc.yaml
just env prod         # → genera .env.prod
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
- **Nunca versionar `.env.*` (`.env.dev`, `.env.prod`, `.env.int`).** Estos se generan con `just env <entorno>` y están en `.gitignore`. La plantilla `.env.example` (sin valores) sí se versiona.
- **Nunca versionar secretos en plano** en archivos YAML, JSON, properties, `.env`, código fuente ni ningún otro formato. Todo secreto debe pasar por `sops edit` y vivir en `.secrets/*.enc.yaml`.
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
- [Regla 05: Control de Versiones](05-version-control.md) — Conventional Commits aplican a cambios en `.sops.yaml` y `.secrets/`.
- [sops + age documentation](https://getsops.io/)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [trufflehog](https://github.com/trufflesecurity/trufflehog)
- [templates/repository-structure/.config/sops/.sops.yaml.tmpl](../templates/repository-structure/.config/sops/.sops.yaml.tmpl)
- [templates/helpers/shell/secrets.sh.tmpl](../templates/repository-structure/helpers/shell/secrets.sh.tmpl)
- [templates/gitignore/.gitignore.secretos.tmpl](../templates/gitignore/.gitignore.secretos.tmpl)

tags: [obligatorio]

### Plantilla: Plantilla

- [templates/repository-structure/.config/sops/.sops.yaml.tmpl](../templates/repository-structure/.config/sops/.sops.yaml.tmpl)
- [templates/repository-structure/.secrets/](../templates/repository-structure/.secrets/)
- [templates/helpers/shell/secrets.sh.tmpl](../templates/repository-structure/helpers/shell/secrets.sh.tmpl)
- [templates/gitignore/.gitignore.secretos.tmpl](../templates/gitignore/.gitignore.secretos.tmpl)

tags: [opcional]
