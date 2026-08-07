# Regla 02: Arquitectura

## Premisa

Los proyectos deben seguir arquitectura hexagonal (puertos y adaptadores) para maximizar testabilidad y mantenibilidad.

## Estructura Hexagonal

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

## Beneficios

- **Testabilidad**: La lógica de negocio es independiente de frameworks
- **Mantenibilidad**: Cambios en tecnología no afectan el core
- **Escalabilidad**: Fácil agregar nuevos adaptadores

## Referencias

- Alistair Cockburn - Hexagonal Architecture
- DDD - Domain Driven Design
