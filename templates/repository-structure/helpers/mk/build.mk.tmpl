PROJECT_NAME ?= $(notdir $(CURDIR))
BUILD_HELPER ?= helpers/shell/build.sh
TEST_HELPER ?= helpers/shell/test.sh
CLEAN_HELPER ?= helpers/shell/clean.sh
BUILD_CMD ?=
TEST_CMD ?=
CLEAN_PATHS ?= build dist site
WORKSPACE ?= $(CURDIR)

.PHONY: build test clean

build:
	@if [ -f "$(BUILD_HELPER)" ]; then \
		bash "$(BUILD_HELPER)" --project-name "$(PROJECT_NAME)" --workspace "$(WORKSPACE)" --command "$(BUILD_CMD)"; \
	else \
		echo "No build helper found. Expected helpers/shell/build.sh"; \
		exit 1; \
	fi

test:
	@if [ -f "$(TEST_HELPER)" ]; then \
		bash "$(TEST_HELPER)" --project-name "$(PROJECT_NAME)" --workspace "$(WORKSPACE)" --command "$(TEST_CMD)"; \
	else \
		echo "No test helper found. Expected helpers/shell/test.sh"; \
		exit 1; \
	fi

clean:
	@if [ -f "$(CLEAN_HELPER)" ]; then \
		bash "$(CLEAN_HELPER)" --project-name "$(PROJECT_NAME)" --workspace "$(WORKSPACE)" --paths "$(CLEAN_PATHS)"; \
	else \
		echo "No clean helper found. Expected helpers/shell/clean.sh"; \
		exit 1; \
	fi
