#!/bin/sh
# Rebuild ./site from ./src. Run after any change to src/ and commit the result.
set -e
cd "$(dirname "$0")"
RB_EMAIL=info@razburg.com python3 src/build.py site
rm -rf src/__pycache__
