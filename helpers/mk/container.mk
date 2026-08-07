.PHONY: runtime image ci

PROJECT_NAME ?= $(notdir $(CURDIR))
CONTAINER_RUNTIME ?=
CI_IMAGE ?= project-ci:local
CI_DOCKERFILE ?= Dockerfile.ci
CONTAINER_HELPER ?= helpers/shell/container.sh
CONTAINER_HELPER_PY ?= helpers/python/container.py

runtime:
	@if [ -f "$(CONTAINER_HELPER)" ]; then \
		bash "$(CONTAINER_HELPER)" --action runtime --project-name "$(PROJECT_NAME)" --container-runtime "$(CONTAINER_RUNTIME)" --ci-image "$(CI_IMAGE)" --dockerfile "$(CI_DOCKERFILE)"; \
	elif [ -f "$(CONTAINER_HELPER_PY)" ]; then \
		uv run python "$(CONTAINER_HELPER_PY)" --action runtime --project-name "$(PROJECT_NAME)" --container-runtime "$(CONTAINER_RUNTIME)" --ci-image "$(CI_IMAGE)" --dockerfile "$(CI_DOCKERFILE)"; \
	else \
		echo "No container helper found. Expected helpers/shell/container.sh or helpers/python/container.py"; \
		exit 1; \
	fi

image:
	@if [ -f "$(CONTAINER_HELPER)" ]; then \
		bash "$(CONTAINER_HELPER)" --action image --project-name "$(PROJECT_NAME)" --container-runtime "$(CONTAINER_RUNTIME)" --ci-image "$(CI_IMAGE)" --dockerfile "$(CI_DOCKERFILE)"; \
	elif [ -f "$(CONTAINER_HELPER_PY)" ]; then \
		uv run python "$(CONTAINER_HELPER_PY)" --action image --project-name "$(PROJECT_NAME)" --container-runtime "$(CONTAINER_RUNTIME)" --ci-image "$(CI_IMAGE)" --dockerfile "$(CI_DOCKERFILE)"; \
	else \
		echo "No container helper found. Expected helpers/shell/container.sh or helpers/python/container.py"; \
		exit 1; \
	fi

ci:
	@if [ -f "$(CONTAINER_HELPER)" ]; then \
		bash "$(CONTAINER_HELPER)" --action ci --project-name "$(PROJECT_NAME)" --container-runtime "$(CONTAINER_RUNTIME)" --ci-image "$(CI_IMAGE)" --dockerfile "$(CI_DOCKERFILE)"; \
	elif [ -f "$(CONTAINER_HELPER_PY)" ]; then \
		uv run python "$(CONTAINER_HELPER_PY)" --action ci --project-name "$(PROJECT_NAME)" --container-runtime "$(CONTAINER_RUNTIME)" --ci-image "$(CI_IMAGE)" --dockerfile "$(CI_DOCKERFILE)"; \
	else \
		echo "No container helper found. Expected helpers/shell/container.sh or helpers/python/container.py"; \
		exit 1; \
	fi
