.PHONY: clean
SITE_DIR ?= site

clean:
	bash helpers/shell/clean.sh --paths "$(SITE_DIR) mcp/dist"
