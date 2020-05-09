#!/usr/bin/env bash

set -o errexit
set -o nounset

declare -a mac_settings_dirs=("${HOME}/Library/Preferences" "${HOME}/Library/Application Support" )
declare -a editors=("PyCharm*" "GoLand*" )

for settings_dir in "${mac_settings_dirs[@]}"; do
    for editor in "${editors[@]}"; do
        find "${settings_dir}" -type d -mindepth 0 -maxdepth 2 -name "${editor}" 2> /dev/null
    done
done
