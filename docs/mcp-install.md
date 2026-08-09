# Instalar el MCP

El servidor `ether-rules` se instala como paquete Python y se configura automáticamente en **Claude Code**, **Codex** (OpenAI) y **opencode**. Expone las reglas y templates de Ether Best Practices como Resources, Tools y Prompts.

## Instalación automática (recomendado)

El instalador descarga el wheel desde GitHub releases, verifica el checksum, instala y configura los 3 clientes:

```bash
curl -sL https://raw.githubusercontent.com/rafex/ether-my-best-practice/main/helpers/shell/mcp-install.sh | bash
```

O en un clon del repositorio: `just app-install`.

## Requisitos previos

| Requisito | Linux | macOS | Windows |
|---|---|---|---|
| **Python** | ≥ 3.12 (`apt install python3`) | ≥ 3.12 (`brew install python`) | ≥ 3.12 ([python.org](https://python.org)) |
| **uv** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `brew install uv` | `winget install astral-sh.uv` |
| **Conexión** | GitHub API + releases | ídem | ídem |

---

=== "Linux"

    ## Linux

    ### 1. Instalar uv

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Reiniciar terminal o: source ~/.bashrc
    ```

    ### 2. Instalar el MCP

    ```bash
    curl -sL https://raw.githubusercontent.com/rafex/ether-my-best-practice/main/helpers/shell/mcp-install.sh | bash
    ```

    O manualmente:

    ```bash
    curl -sL -o /tmp/ether_mcp.whl \
      "$(curl -sL https://api.github.com/repos/rafex/ether-my-best-practice/releases/latest \
       | python3 -c "import sys,json; assets=json.load(sys.stdin).get('assets',[]); print([a['browser_download_url'] for a in assets if a['name'].endswith('.whl')][0])")"
    uv tool install /tmp/ether_mcp.whl
    ```

    ### 3. Configurar clientes

    ```bash
    # Claude Code
    claude mcp add --scope user ether-rules -- uvx ether-mcp

    # Codex
    codex mcp add ether-rules -- uvx ether-mcp

    # opencode
    opencode mcp add ether-rules -- uvx ether-mcp
    ```

    ### 4. Verificar

    ```bash
    ether-mcp --version   # o uv run ether-mcp
    claude mcp list | grep ether-rules
    codex mcp list | grep ether-rules
    opencode mcp list | grep ether-rules
    ```

    **PATH:** `~/.local/bin/` debe estar en `$PATH`. Si no, añade `export PATH="$HOME/.local/bin:$PATH"` a tu `~/.bashrc`.

=== "macOS"

    ## macOS

    ### 1. Instalar uv

    ```bash
    brew install uv
    ```

    ### 2. Instalar el MCP

    ```bash
    curl -sL https://raw.githubusercontent.com/rafex/ether-my-best-practice/main/helpers/shell/mcp-install.sh | bash
    ```

    O manualmente: igual que Linux.

    ### 3. Configurar clientes

    ```bash
    # Claude Code
    claude mcp add --scope user ether-rules -- uvx ether-mcp

    # Codex
    codex mcp add ether-rules -- uvx ether-mcp

    # opencode
    opencode mcp add ether-rules -- uvx ether-mcp
    ```

    ### 4. Verificar

    Los mismos comandos que en Linux. `~/.local/bin/` suele estar ya en PATH desde `brew`/`uv`.

=== "Windows"

    ## Windows

    ### 1. Instalar uv

    **PowerShell** (recomendado):

    ```powershell
    winget install astral-sh.uv
    ```

    O vía script:

    ```powershell
    irm https://astral.sh/uv/install.ps1 | iex
    ```

    ### 2. Instalar el MCP

    **PowerShell** (requiere Python + uv instalados y en PATH):

    ```powershell
    irm https://raw.githubusercontent.com/rafex/ether-my-best-practice/main/helpers/shell/mcp-install.sh | bash
    ```

    > Si `bash` no está disponible, instala [Git Bash](https://git-scm.com) o ejecuta los pasos manuales:

    ```powershell
    $release = Invoke-RestMethod "https://api.github.com/repos/rafex/ether-my-best-practice/releases/latest"
    $wheel = $release.assets | Where-Object { $_.name -like "*.whl" } | Select-Object -First 1
    Invoke-WebRequest -Uri $wheel.browser_download_url -OutFile "$env:TEMP\ether_mcp.whl"
    uv tool install "$env:TEMP\ether_mcp.whl"
    ```

    ### 3. Configurar clientes

    ```powershell
    # Claude Code
    claude mcp add --scope user ether-rules -- uvx ether-mcp

    # Codex
    codex mcp add ether-rules -- uvx ether-mcp

    # opencode
    opencode mcp add ether-rules -- uvx ether-mcp
    ```

    ### 4. Verificar

    ```powershell
    ether-mcp --version
    claude mcp list | Select-String ether-rules
    codex mcp list | Select-String ether-rules
    opencode mcp list | Select-String ether-rules
    ```

    **PATH:** uv tool install escribe en `%USERPROFILE%\.local\bin`. Asegúrate de que esté en tu `PATH` (normalmente se agrega al instalar uv).

---

## Configuración manual de clientes (sin CLI)

Si los comandos CLI no están disponibles, edita los archivos de configuración directamente:

=== "Claude Code"

    Edita `~/.claude.json` (Linux/macOS) o `%HOME%\.claude.json` (Windows):

    ```json
    {
      "mcpServers": {
        "ether-rules": {
          "command": "uvx",
          "args": ["ether-mcp"]
        }
      }
    }
    ```

=== "Codex"

    Edita `~/.codex/config.toml` (Linux/macOS) o `%USERPROFILE%\.codex\config.toml` (Windows):

    ```toml
    [mcp_servers.ether-rules]
    command = "uvx"
    args = ["ether-mcp"]
    ```

=== "opencode"

    Edita `~/.config/opencode/opencode.json` (Linux/macOS) o `%APPDATA%\opencode\opencode.json` (Windows):

    ```json
    {
      "mcp": {
        "ether-rules": {
          "type": "local",
          "command": ["uvx", "ether-mcp"],
          "enabled": true
        }
      }
    }
    ```
    > opencode requiere el campo `"type": "local"` y el `command` como lista de strings.

---

## Desinstalación

```bash
curl -sL https://raw.githubusercontent.com/rafex/ether-my-best-practice/main/helpers/shell/mcp-install.sh | bash -s -- --action uninstall
```

O manualmente:

```bash
# En cada cliente
claude mcp remove ether-rules
codex mcp remove ether-rules
opencode mcp remove ether-rules

# Paquete
uv tool uninstall ether-mcp-my-best-practices
```

## Solución de problemas

| Problema | Solución |
|---|---|
| `uv: command not found` | Instalar uv (ver requisitos previos) |
| `ether-mcp: command not found` | Añadir `~/.local/bin` al PATH |
| `sha256sum: command not found` (macOS) | `brew install coreutils` y usar `gsha256sum` |
| Checksum no coincide | Borrar `/tmp/ether_mcp.whl` y reintentar (posible descarga corrupta) |
| Cliente no aparece en `mcp list` | Reiniciar el cliente; verificar que `uvx` esté en PATH |
| opencode `type` error | Asegurar que el JSON tiene `"type": "local"` y `"command"` como lista |

La [regla 07](rules/07-agents-mcp.md) documenta los Resources, Tools y Prompts que expone el servidor.
