#!/bin/bash
# Script by Adrian, if you're wondering

# To be executed in parent directory
if ! test -f "LICENSE"; then
    echo "License file not found in current directory. Canceling."
    exit
fi

ln -s /home/eml4u/EML4U/data/symlink-target data
