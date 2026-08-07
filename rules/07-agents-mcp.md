# Regla 07: Agentes de IA y Model Context Protocol (MCP)

## Premisa

Las reglas deben ser accesibles a agentes de IA (como Claude, GitHub Copilot) a través de Model Context Protocol para mejorar la asistencia en desarrollo.

## Model Context Protocol (MCP)

MCP es un protocolo estándar que permite que agentes de IA accedan a recursos (archivos, bases de datos, APIs) de forma estructurada.

### Servidor MCP

Un servidor MCP expone "recursos" (recursos) que un agente puede consultar.

```json
{
  "mcp_servers": {
    "ether-rules": {
      "command": "node",
      "args": ["mcp-server.js"]
    }
  }
}
```

### Recursos Disponibles

Cada regla es un recurso que el agente puede solicitar:

```
ether://rules/01-build-tooling
ether://rules/02-architecture
ether://rules/03-testing
...
```

## Configuración en Agentes

### GitHub Copilot

Agregar a `.instructions.md`:

```markdown
## Reglas de Proyecto

Consultar las siguientes reglas:
- ether://rules/01-build-tooling
- ether://rules/02-architecture
```

### Claude / Otros Agentes

Proporcionar URLs o rutas:

```
Context: Siempre sigue las reglas en:
- https://github.com/rafex/ether-my-best-practice/tree/main/rules
```

## Estructura para MCP

La carpeta `rules/` debe contener:

- Archivos Markdown con contenido claro
- Nombres descriptivos: `NN-topic.md`
- Índice centralizado: `00-index.md`
- JSON de metadatos (opcional): `rule.json`

```json
{
  "id": "build-tooling",
  "title": "Herramientas de Construcción",
  "description": "Estándares para Makefiles, Justfiles, etc.",
  "tags": ["build", "tooling", "automation"],
  "file": "01-build-tooling.md"
}
```

## Best Practices para Reglas

1. **Claridad**: Escribir de forma directa y estructurada
2. **Ejemplos**: Incluir código/configuración real
3. **Formato**: Markdown con títulos jerárquicos
4. **Versionado**: Cada cambio en Git con mensaje descriptivo
5. **Indexado**: Mantener `00-index.md` actualizado

## Cómo Integrar con Agentes

### Opción 1: Compartir repositorio

```bash
# Clonar las reglas
git clone https://github.com/rafex/ether-my-best-practice.git rules/
```

Luego el agente puede leerlas como archivos.

### Opción 2: Servidor MCP

Implementar servidor que sirva reglas:

```javascript
// mcp-server.js
const { Server } = require("@modelcontextprotocol/sdk/server/stdio");

const server = new Server();

server.addResourceHandler("ether://rules/*", async (uri) => {
  const file = uri.replace("ether://rules/", "");
  const content = readFile(`./rules/${file}.md`);
  return { contents: [{ type: "text", text: content }] };
});
```

### Opción 3: Embeddings + RAG

Vectorizar las reglas y usar Retrieval-Augmented Generation:

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(
    rules, embeddings, index_name="ether-rules"
)
```

## Integración con Proyectos

Cada proyecto debe referenciar estas reglas:

```markdown
# Mi Proyecto XYZ

Este proyecto sigue las reglas de [Ether My Best Practice](../rules/00-index.md).

Reglas aplicables:
- [02-architecture.md](../rules/02-architecture.md)
- [03-testing.md](../rules/03-testing.md)
- [05-version-control.md](../rules/05-version-control.md)
```

## Uso de Templates por Agentes

Además de consultar reglas, los agentes pueden usar [templates](../templates/) como cascarones iniciales para crear proyectos alineados con este estándar.

### Objetivo de los templates

- Dar una estructura base consistente a una API REST.
- Reducir decisiones repetitivas al crear un proyecto nuevo.
- Asegurar que el código generado por agentes siga las reglas del repositorio desde el inicio.

### Cómo debe usarlos un agente

1. Leer primero el índice en [00-index.md](00-index.md).
2. Consultar las reglas aplicables al tipo de cambio.
3. Copiar el template más cercano al objetivo.
4. Adaptar el contenido en el proyecto consumidor sin modificar este repositorio como si fuera el servicio final.

### Restricción importante

Los templates son esqueletos reutilizables. No deben llenarse aquí con detalles concretos de un servicio real salvo que el objetivo del cambio sea mejorar la plantilla misma.

## Ejemplo de Prompt a Agente

```
You are an AI coding assistant helping with a project that follows Ether Best Practices.

Context Rules:
1. Build: See rules/01-build-tooling.md
2. Architecture: See rules/02-architecture.md
3. Testing: See rules/03-testing.md

When making suggestions:
- Always follow the hexagonal architecture pattern
- Ensure tests are added (TDD)
- Use conventional commits
```
