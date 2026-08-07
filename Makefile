.PHONY: help docs pages-build pages serve clean pages

SITE_DIR ?= site
PAGES_WORKFLOW ?= pages.yml
PAGES_REF ?= main

help:
	@echo "Tareas disponibles:"
	@echo "  make docs        - Generar el sitio MkDocs localmente"
	@echo "  make pages-build - Generar el sitio en $(SITE_DIR)"
	@echo "  make pages       - Disparar el workflow de GitHub Pages"
	@echo "  make serve       - Servir la documentación localmente"
	@echo "  make clean       - Limpiar artefactos"

docs:
	mkdocs build --site-dir "$(SITE_DIR)"

pages-build: docs
	@echo "Sitio generado en $(SITE_DIR)"

pages:
	@if command -v gh >/dev/null 2>&1; then \
		gh workflow run "$(PAGES_WORKFLOW)" --ref "$(PAGES_REF)"; \
		echo "Workflow $(PAGES_WORKFLOW) disparado en $(PAGES_REF)"; \
	else \
		echo "GitHub CLI (gh) no está disponible. Usa 'make pages-build' o instala gh para disparar el workflow."; \
		exit 1; \
	fi

serve:
	mkdocs serve

clean:
	rm -rf "$(SITE_DIR)"
