#!/bin/sh
# Tile a WireViz SVG onto US-letter landscape pages for printing.
# usage: docs/wiring/tile.sh <name> [zoom]   -> docs/wiring/<name>_tiled_letter.pdf
# Needs rsvg-convert (brew install librsvg) and qpdf (brew install qpdf).
set -e
name=$1; zoom=${2:-0.7}
dir=$(dirname "$0"); svg=$dir/$name.svg; out=$dir/${name}_tiled_letter.pdf
pw=792; ph=612; ov=18                      # page pt, overlap pt
w=$(rsvg-convert -z "$zoom" -f pdf "$svg" | pdfinfo - | awk '/Page size/{print int($3+0.999)}')
h=$(rsvg-convert -z "$zoom" -f pdf "$svg" | pdfinfo - | awk '/Page size/{print int($5+0.999)}')
sw=$((pw-ov)); sh=$((ph-ov))
cols=$(( (w + sw - 1) / sw )); rows=$(( (h + sh - 1) / sh ))
tmp=$(mktemp -d); i=0
r=0; while [ $r -lt $rows ]; do
  c=0; while [ $c -lt $cols ]; do
    i=$((i+1))
    rsvg-convert -z "$zoom" -f pdf --page-width "${pw}pt" --page-height "${ph}pt" \
      --left="-$((c*sw))pt" --top="-$((r*sh))pt" -o "$tmp/$(printf %03d $i).pdf" "$svg"
    c=$((c+1)); done
  r=$((r+1)); done
qpdf --empty --pages "$tmp"/*.pdf -- "$out"
rm -rf "$tmp"
echo "$out: ${cols}x${rows} pages (zoom $zoom, read left-to-right then next row)"
