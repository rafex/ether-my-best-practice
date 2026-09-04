.PHONY: version-bump checksums mcp-smoke package publish-checksums release

PUBLISH_DIR ?= site/ether-rules

version-bump:
	bash helpers/shell/cz.sh --action bump

checksums:
	python3 helpers/python/generate_checksums.py

mcp-smoke:
	RULES_DIR="$(CURDIR)/rules" TEMPLATES_DIR="$(CURDIR)/templates" HELPERS_DIR="$(CURDIR)/helpers" DOCS_DIR="$(CURDIR)/docs" MCP_ROOT="$(CURDIR)" uv run --directory mcp python -c 'from ether_mcp_my_best_practices import server as s; assert len(s.list_rules()) == 18; assert hasattr(s, "audit_project") and hasattr(s, "check_project"); print("MCP smoke test: OK")'

publish-checksums: checksums
	mkdir -p $(PUBLISH_DIR)/rules $(PUBLISH_DIR)/templates $(PUBLISH_DIR)/helpers $(PUBLISH_DIR)/docs
	cp checksums.json $(PUBLISH_DIR)/checksums.json
	cp -R rules/. $(PUBLISH_DIR)/rules/
	cp -R templates/. $(PUBLISH_DIR)/templates/
	cp -R helpers/. $(PUBLISH_DIR)/helpers/
	cp docs/*.md $(PUBLISH_DIR)/docs/

package: checksums mcp-smoke
	bash helpers/shell/release.sh --action package

release:
	bash helpers/shell/release.sh --action release
