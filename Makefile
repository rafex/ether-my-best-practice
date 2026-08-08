.PHONY: help validate lint format link-rules docs pages-build pages clean

SITE_DIR ?= site
PAGES_WORKFLOW ?= static.yml
PAGES_REF ?= main

help:
	@echo "Tareas disponibles (operación de este repositorio):"
	@echo "  make validate      - Validar estructura y enlaces de las reglas"
	@echo "  make lint          - Validar estilo de las reglas y documentación"
	@echo "  make format        - Formatear reglas y documentación"
	@echo "  make link-rules    - Crear hard links rules/ → docs/rules/"
	@echo "  make docs          - Generar el sitio MkDocs localmente"
	@echo "  make pages-build   - Generar el sitio en $(SITE_DIR)"
	@echo "  make pages         - Disparar el workflow de GitHub Pages"
	@echo "  make clean         - Eliminar el sitio generado ($(SITE_DIR))"
	@echo ""
	@echo "Operativas de levantar (serve) pertenecen a Justfile: just serve"

validate:
	bash helpers/shell/validate-rules.sh

link-rules:
	bash helpers/shell/rules-link.sh --goal link

lint:
	@echo "Lint pendiente de implementar."
	@echo "Agrega la lógica en helpers/shell/lint.sh"

format:
	@echo "Format pendiente de implementar."
	@echo "Agrega la lógica en helpers/shell/format.sh"

docs: link-rules
	mkdocs build -f .config/mkdocs/mkdocs.yml

pages-build: validate docs
	@echo "Sitio generado en $(SITE_DIR)"

pages:
	bash helpers/shell/github.sh --action workflow-run --workflow "$(PAGES_WORKFLOW)" --ref "$(PAGES_REF)"

clean:
	rm -rf "$(SITE_DIR)"
