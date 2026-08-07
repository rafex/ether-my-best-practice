# Estructura de Proyecto Hexagonal

Esta es una estructura de referencia para un proyecto que sigue arquitectura hexagonal.

```
project/
├── README.md
├── Makefile (o Justfile)
├── .gitignore
│
├── src/
│   ├── main/
│   │   ├── java/              # (o python/, rust/, kotlin/, etc.)
│   │   │   └── com/example/
│   │   │       ├── domain/            # Lógica de negocio pura
│   │   │       ├── application/       # Casos de uso
│   │   │       ├── infrastructure/    # Adaptadores
│   │   │       └── ports/            # Interfaces
│   │   └── resources/
│   │       └── application.yml
│   │
│   └── test/
│       ├── java/
│       │   └── com/example/
│       │       ├── domain/
│       │       ├── application/
│       │       └── infrastructure/
│       └── resources/
│
├── docs/                      # Documentación en Markdown
│   ├── index.md
│   ├── architecture.md
│   ├── api.md
│   └── contributing.md
│
├── site/                      # (generado) Sitio web estático
│
└── mkdocs.yml                 # Configuración de documentación
```

## Estructura de Código

### domain/
Contiene la lógica de negocio **pura**, sin dependencias de framework.

```
domain/
├── entities/          # Objetos de dominio
├── value_objects/     # Valores immutables
├── services/          # Servicios de dominio
└── repositories/      # Interfaces de persistencia (Puertos)
```

### application/
Casos de uso que orquestan dominio.

```
application/
├── use_cases/
│   ├── CreateUserUseCase
│   └── DeleteUserUseCase
└── dto/               # Data Transfer Objects
```

### infrastructure/
Implementaciones concretas de adaptadores.

```
infrastructure/
├── persistence/       # Implementación de repositories
├── web/              # Controllers/Handlers HTTP
├── external/         # Integraciones externas
└── config/           # Configuración de frameworks
```

### ports/
Interfaces públicas que definen los puertos.

```
ports/
├── UserRepository.java        # Puerto - qué no cómo
└── NotificationService.java
```

## Beneficios

✓ Cambiar base de datos sin tocar lógica de negocio  
✓ Tests sin dependencias externas  
✓ Fácil agregar nuevos adaptadores  
✓ Código mantenible y escalable
