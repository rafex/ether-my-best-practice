# Makefile — Construcción (build/artefactos)
# Delega en helpers/mk/*.mk por dominio.
# Operativas en Justfile (vía helpers/just/*.just).

MK_FILES ?= $(wildcard helpers/mk/*.mk)
-include $(MK_FILES)

.PHONY: help check deploy

help:
	@echo "Makefile — Construcción (build, artefactos, CD)"
	@echo "  make validate      - Validar estructura y enlaces de las reglas"
	@echo "  make lint          - Validar sintaxis de helpers (shell + python)"
	@echo "  make format        - Formatear reglas y documentación"
	@echo "  make link-rules    - Crear hard links rules/ → docs/rules/"
	@echo "  make docs          - Compilar sitio MkDocs (estáticos para Pages)"
	@echo "  make preview-site  - Compilar sitio + servidor local (preview)"
	@echo "  make pages-build   - validate + docs"
	@echo "  make pages         - Disparar workflow de GitHub Pages"
	@echo "  make clean         - Limpiar artefactos (site, mcp/dist)"
	@echo "  make version-bump  - Bump de versión con Commitizen"
	@echo "  make checksums     - Generar checksums.json + incrustar hash en reglas"
	@echo "  make publish-checksums - Publicar checksums.json + contenido raw en site/"
	@echo "  make package       - Wheel del MCP (mcp/dist/*.whl)"
	@echo "  make release       - Publicar GitHub Release"
	@echo "  make deploy        - CI: validate + package + release"
	@echo "  make check         - Gate de calidad: lint + validate"
	@echo ""
	@echo "Operativas → Justfile: just <recipe> (repository.just, app.just)"

check: lint validate

deploy: validate package release
	@echo "Deploy completo."
	@echo "  Portal: https://github.com/rafex/ether-my-best-practice/releases/latest"
