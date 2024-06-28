#!/bin/bash
# Generates a svgz from a vsdx
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
BASENAME=${1%.*}
cscript.exe /NoLogo "$(wslpath -w "$DIR/visio2svg.vbs")" $1 $2
