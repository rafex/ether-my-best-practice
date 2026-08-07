# Regla 03: Testing

## Premisa

Todo código debe ser testeado siguiendo TDD (Test Driven Development) y la pirámide de tests.

## Pirámide de Tests

```
        /\
       /  \  E2E Tests (10%)
      /____\
     /      \
    /        \ Integration Tests (30%)
   /          \
  /__________  \
 /            \  Unit Tests (60%)
/              \
/______________\
```

## Estrategia

### Unit Tests (60%)
- Prueban funciones/métodos individuales
- Sin dependencias externas
- Rápidos de ejecutar
- Herramientas: JUnit, pytest, RSpec

### Integration Tests (30%)
- Prueban interacción entre componentes
- Pueden usar bases de datos en memoria
- Herramientas: TestContainers, pytest fixtures

### E2E Tests (10%)
- Prueban flujos completos
- Contra ambiente real o similar
- Lentos pero críticos
- Herramientas: Selenium, Playwright, Cypress

## TDD - Test Driven Development

1. **Red**: Escribir test que falla
2. **Green**: Escribir código mínimo para pasar
3. **Refactor**: Mejorar el código

## Cobertura

Objetivo: **> 80% de cobertura** en código crítico
