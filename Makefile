.PHONY: help validate lint format docs pages-build pages serve clean

SITE_DIR ?= site
PAGES_WORKFLOW ?= static.yml
PAGES_REF ?= main

help:
	@echo "Tareas disponibles (operación de este repositorio):"
	@echo "  make validate      - Validar estructura y enlaces de las reglas"
	@echo "  make lint          - Validar estilo de las reglas y documentación"
	@echo "  make format        - Formatear reglas y documentación"
	@echo "  make docs          - Generar el sitio MkDocs localmente"
	@echo "  make pages-build   - Generar el sitio en $(SITE_DIR)"
	@echo "  make pages         - Disparar el workflow de GitHub Pages"
	@echo "  make serve         - Servir la documentación localmente"
	@echo "  make clean         - Eliminar el sitio generado ($(SITE_DIR))"

validate:
	bash helpers/shell/validate-rules.sh

lint:
	@echo "Lint pendiente de implementar."
	@echo "Agrega la lógica en helpers/shell/lint.sh"

format:
	@echo "Format pendiente de implementar."
	@echo "Agrega la lógica en helpers/shell/format.sh"

docs:
	mkdocs build --site-dir "$(SITE_DIR)"

pages-build: validate docs
	@echo "Sitio generado en $(SITE_DIR)"

pages:
	@if command -v gh >/dev/null 2>&1; then \
		gh workflow run "$(PAGES_WORKFLOW)" --ref "$(PAGES_REF)"; \
		echo "Workflow $(PAGES_WORKFLOW) disparado en $(PAGES_REF)"; \
	else \
		echo "GitHub CLI (gh) no está disponible. Usa 'make pages-build' o instala gh para disparar el workflow static.yml."; \
		exit 1; \
	fi

serve:
	mkdocs serve

clean:
	rm -rf "$(SITE_DIR)"
