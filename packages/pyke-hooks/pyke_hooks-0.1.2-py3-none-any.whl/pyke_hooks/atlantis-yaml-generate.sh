#!/usr/bin/env bash
set -eo pipefail

check_changes() {
    file_name="atlantis.yaml"

    # Check if there are unstaged changes for the specified file
    if git diff --exit-code -- "$file_name" >/dev/null 2>&1; then
        echo "No changes in $file_name";
    else
        echo "Configuration file $file_name updated. Please add it to your commit.";
        exit 1;
    fi
}

atlantis-yaml-generate "$@"

check_changes
