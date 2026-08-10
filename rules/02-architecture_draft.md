---
id: architecture
title: Arquitectura Hexagonal
status: Borrador
tags: [architecture, hexagonal, ports, adapters, ddd]
---

# Regla 02: Arquitectura — ⚠️ *Borrador*



### Premisa: Premisa

Los proyectos deben seguir arquitectura hexagonal (puertos y adaptadores) para maximizar testabilidad y mantenibilidad. La lógica de negocio es independiente de frameworks.

tags: [obligatorio]

### Restriccion: Restricciones

- El dominio (lógica de negocio) **no debe depender de frameworks ni bibliotecas externas**.
- Las dependencias solo pueden apuntar desde infraestructura hacia puertos y dominio, nunca al revés.
- No mezclar lógica de negocio con controladores HTTP, repositories ni serialización/deserialización.

tags: [obligatorio]

### Ejemplo: Ejemplos

### Estructura hexagonal típica

```
src/
├── main/
│   ├── domain/              # Lógica de negocio (sin dependencias externas)
│   │   ├── models/
│   │   └── services/
│   ├── application/         # Casos de uso
│   ├── infrastructure/      # Implementaciones concretas
│   │   ├── repositories/    # Adaptadores de persistencia
│   │   ├── web/            # Adaptadores HTTP
│   │   └── external/       # Integraciones externas
│   └── ports/              # Interfaces (puertos)
└── test/
```

### Capas por responsabilidad

- `domain/` — entidades, value objects, servicios de dominio, interfaces de repositorio.
- `application/` — casos de uso, DTOs.
- `infrastructure/` — implementaciones concretas: persistencia, web, integraciones externas, configuración.
- `ports/` — interfaces públicas (puertos) que definen qué, no cómo.

tags: [obligatorio]

### Referencia: Referencias

- Alistair Cockburn — Hexagonal Architecture
- Domain Driven Design (DDD) — Eric Evans
- [templates/repository-structure/README.md](../templates/repository-structure/README.md)
- [Regla 01: Build Tooling](01-build-tooling.md)
- [Regla 03: Testing](03-testing_draft.md)
- [Regla 09: Estructura de Repositorio](09-repository-structure.md)

tags: [obligatorio]

### Estructura: Estructura

Ver [templates/repository-structure/](../templates/repository-structure/) para la estructura completa de un proyecto generado.

tags: [opcional]
