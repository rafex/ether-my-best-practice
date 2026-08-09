.PHONY: pages
PAGES_WORKFLOW ?= static.yml
PAGES_REF ?= main

pages:
	bash helpers/shell/github.sh --action workflow-run --workflow "$(PAGES_WORKFLOW)" --ref "$(PAGES_REF)"
