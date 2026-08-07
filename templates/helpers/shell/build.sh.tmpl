#!/usr/bin/env bash
set -euo pipefail

project_name=""
workspace="$(pwd)"
command_line=""
log_file=""

while [[ $# -gt 0 ]]; do
	case "$1" in
		--project-name)
			project_name="${2:-}"; shift 2 ;;
		--workspace)
			workspace="${2:-}"; shift 2 ;;
		--command)
			command_line="${2:-}"; shift 2 ;;
		--log-file)
			log_file="${2:-}"; shift 2 ;;
		*)
			echo "Unknown flag: $1" >&2
			exit 1 ;;
	esac
done

if [[ -z "$command_line" ]]; then
	echo "Missing required flag --command" >&2
	exit 1
fi

if [[ -z "$project_name" ]]; then
	project_name="$(basename "$workspace")"
fi

script_name="build"
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
echo "Workspace: $workspace"
echo "Build command: $command_line"

cd "$workspace"
bash -lc "$command_line"
