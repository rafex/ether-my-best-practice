#!/usr/bin/env bash
set -euo pipefail

action=""
project_name=""
container_runtime=""
ci_image="project-ci:local"
dockerfile="Dockerfile.ci"
workspace="$(pwd)"
site_dir="site"
log_file=""

while [[ $# -gt 0 ]]; do
	case "$1" in
		--action)
			action="${2:-}"; shift 2 ;;
		--project-name)
			project_name="${2:-}"; shift 2 ;;
		--container-runtime)
			container_runtime="${2:-}"; shift 2 ;;
		--ci-image)
			ci_image="${2:-}"; shift 2 ;;
		--dockerfile)
			dockerfile="${2:-}"; shift 2 ;;
		--workspace)
			workspace="${2:-}"; shift 2 ;;
		--site-dir)
			site_dir="${2:-}"; shift 2 ;;
		--log-file)
			log_file="${2:-}"; shift 2 ;;
		*)
			echo "Unknown flag: $1" >&2
			exit 1 ;;
	esac
done

if [[ -z "$action" ]]; then
	echo "Missing required flag --action" >&2
	exit 1
fi

if [[ -z "$project_name" ]]; then
	project_name="$(basename "$workspace")"
fi

script_name="container"
ts="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ -z "$log_file" ]]; then
	if mkdir -p "/var/log/$project_name" 2>/dev/null && [[ -w "/var/log/$project_name" ]]; then
		log_file="/var/log/$project_name/log-$script_name-$ts.log"
	else
		mkdir -p "/tmp/$project_name"
		log_file="/tmp/$project_name/log-$script_name-$ts.log"
	fi
fi

mkdir -p "$(dirname "$log_file")"
exec > >(tee -a "$log_file") 2>&1

echo "Audit log: $log_file"

resolve_runtime() {
	if [[ -n "$container_runtime" ]]; then
		echo "$container_runtime"
		return
	fi

	if command -v podman >/dev/null 2>&1; then
		echo "podman"
	elif command -v docker >/dev/null 2>&1; then
		echo "docker"
	else
		echo "No container runtime found. Install podman or docker." >&2
		return 1
	fi
}

if ! runtime="$(resolve_runtime)"; then
	exit 1
fi

echo "Container runtime: $runtime"

case "$action" in
	runtime)
		;;
	image)
		if [[ ! -f "$dockerfile" ]]; then
			echo "Missing $dockerfile. Add CI container definition first." >&2
			exit 1
		fi
		echo "Building CI image $ci_image with $runtime using $dockerfile..."
		"$runtime" build -f "$dockerfile" -t "$ci_image" "$workspace"
		;;
	ci)
		if [[ ! -f "$dockerfile" ]]; then
			echo "Missing $dockerfile. Add CI container definition first." >&2
			exit 1
		fi
		echo "Building CI image $ci_image with $runtime using $dockerfile..."
		"$runtime" build -f "$dockerfile" -t "$ci_image" "$workspace"
		echo "Running containerized CI with $runtime..."
		"$runtime" run --rm \
			-v "$workspace":/workspace \
			-w /workspace \
			-e SITE_DIR="$site_dir" \
			"$ci_image" \
			sh -lc 'make build && make test'
		mkdir -p target dist build
		;;
	*)
		echo "Unknown action: $action" >&2
		exit 1 ;;
esac
