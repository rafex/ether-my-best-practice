.PHONY: version-bump checksums package publish-checksums release

PUBLISH_DIR ?= site/ether-rules

version-bump:
	bash helpers/shell/cz.sh --action bump

checksums:
	python3 helpers/python/generate_checksums.py

publish-checksums: checksums
	mkdir -p $(PUBLISH_DIR)/rules $(PUBLISH_DIR)/templates $(PUBLISH_DIR)/helpers $(PUBLISH_DIR)/docs
	cp checksums.json $(PUBLISH_DIR)/checksums.json
	cp -R rules/. $(PUBLISH_DIR)/rules/
	cp -R templates/. $(PUBLISH_DIR)/templates/
	cp -R helpers/. $(PUBLISH_DIR)/helpers/
	cp docs/*.md $(PUBLISH_DIR)/docs/

package: checksums
	bash helpers/shell/release.sh --action package

release:
	bash helpers/shell/release.sh --action release
