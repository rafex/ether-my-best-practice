---
id: testing
title: Estrategias de Testing
status: Borrador
tags: [testing, tdd, unit-tests, integration, e2e, coverage]
checksum: f4776560135e370cb2400cf03aeab7e0b2e3551b451d46d88d1e5253a2dcc03b
---

# Regla 03: Testing — ⚠️ *Borrador*



### Premisa: Premisa

Todo código debe ser testeado siguiendo TDD (Test Driven Development) y la pirámide de tests. El testing es parte del build, no una fase separada.

tags: [obligatorio]

### Restriccion: Restricciones

- **No deployar código sin tests.** El pipeline de CI debe fallar si los tests no pasan.
- Los tests unitarios **no deben depender de red, base de datos ni sistema de archivos**.
- No escribir tests que solo validen implementación interna (white-box extremo); preferir tests de comportamiento.
- La cobertura no es un fin en sí mismo: no forzar 100% si implica tests sin valor. Mínimo >80% en código crítico.

tags: [obligatorio]

### Ejemplo: Ejemplos

### TDD: Red → Green → Refactor

```bash
# 1. Red: escribir test que falla
# 2. Green: escribir código mínimo para pasar
# 3. Refactor: mejorar el código sin romper tests
```

### Pirámide de tests

```
        /\
       /  \  E2E Tests (~10%) — Playwright, Cypress, Selenium
      /____\
     /      \
    /        \ Integration Tests (~30%) — TestContainers, pytest fixtures
   /          \
  /__________  \
 /            \  Unit Tests (~60%) — JUnit, pytest, RSpec
/______________\
```

### Ejecución

```bash
make test LANG=java BUILD_TOOL=maven
make test LANG=python BUILD_TOOL=uv
make test LANG=javascript BUILD_TOOL=pnpm
make test LANG=rust BUILD_TOOL=cargo
```

tags: [obligatorio]

### Referencia: Referencias

- Kent Beck — Test Driven Development
- Martin Fowler — TestPyramid
- [Regla 01: Build Tooling](01-build-tooling.md) — `make test`
- [Regla 06: CI](06-ci.md) — tests en el pipeline

tags: [obligatorio]
