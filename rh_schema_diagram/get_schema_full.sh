#!/usr/bin/env bash
~/WORKSPACE/schemacrawler-16.11.7-distribution/_schemacrawler/schemacrawler.sh --server=sqlite --database="$1" --user=sa --password= --info-level=maximum -c=schema --title "Robot@Home2 Schema Diagram" --output-format=pdf -o="$2"
echo Database diagram is in "$2"
