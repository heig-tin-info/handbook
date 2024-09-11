#!/bin/bash

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <index.pages> <input.pdf>"
  exit 1
fi

index_file="$1"
input_pdf="$2"
output_prefix="volume"

lines=($(cat "$index_file"))

num_lines=${#lines[@]}
if [[ $((num_lines % 2)) -eq 0 ]]; then
  echo "Erreur : Le fichier d'index doit contenir un nombre impair de lignes."
  exit 1
fi

previous=0
part=1
last_index=$((num_lines - 1))

for i in "${!lines[@]}"; do
  line="${lines[$i]}"

  if [[ $previous -ne 0 ]]; then
    if [[ $i -eq $last_index ]]; then
      range_end=$line
    else
      range_end=$(($line - 1))
    fi

    if [[ $previous -le $range_end ]]; then
      pdftk "$input_pdf" cat "$previous-$range_end" output "${output_prefix}${part}.pdf"
      ((part++))
    fi
  fi
  previous=$line
done
