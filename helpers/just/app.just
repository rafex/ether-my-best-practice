# app.just — Capacidades de la aplicación central de este repositorio.
# La "app" de ether-my-best-practice es el servidor MCP que expone
# Resources, Tools y Prompts de las reglas definidas.

# Levantar el servidor MCP (la aplicación)
@app:
    uv run --directory mcp python ether_mcp_my_best_practices/server.py

# Empaquetar el MCP (construcción → make)
@app-package:
    make package
