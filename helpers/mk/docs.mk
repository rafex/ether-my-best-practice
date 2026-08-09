.PHONY: docs pages-build
DOCS_FILE ?= .config/mkdocs/mkdocs.yml
SITE_DIR ?= site

docs: link-rules
	bash helpers/shell/docs.sh --goal build --file "$(DOCS_FILE)" --site-dir "$(SITE_DIR)"

pages-build: validate docs
	@echo "Sitio generado en $(SITE_DIR) h"
