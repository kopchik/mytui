#/bin/bash

OUTDIR="`dirname \"$0\"`"
pip-compile --output-file "${OUTDIR}/dev.txt" "${OUTDIR}/dev.in"
