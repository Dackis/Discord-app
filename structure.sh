#!/bin/bash

# Function to display the directory structure
display_structure() {
    local directory="$1"
    local indent="$2"

    for entry in "$directory"/*; do
        if [ -d "$entry" ]; then
            echo "${indent}$(basename "$entry")/"
            display_structure "$entry" "    $indent"
        else
            echo "${indent}$(basename "$entry")"
        fi
    done
}

# Start with the current directory (or pass a directory as an argument)
start_directory="${1:-.}"

echo "$(basename "$start_directory")/"
display_structure "$start_directory" "    "
