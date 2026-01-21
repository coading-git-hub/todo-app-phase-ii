#!/bin/bash
# Script to create a Prompt History Record

TITLE=""
STAGE=""
FEATURE=""
JSON=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --title)
      TITLE="$2"
      shift 2
      ;;
    --stage)
      STAGE="$2"
      shift 2
      ;;
    --feature)
      FEATURE="$2"
      shift 2
      ;;
    --json)
      JSON=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Create a basic PHR file
if [ -z "$STAGE" ]; then
  STAGE="general"
fi

if [ -z "$TITLE" ]; then
  TITLE="default-title"
fi

# Convert title to slug
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

ID_FILE="history/prompts/.phr_counter"
mkdir -p "history/prompts/${STAGE}"

if [ -f "$ID_FILE" ]; then
  ID=$(cat "$ID_FILE")
  ID=$((ID + 1))
else
  ID=1
fi

echo $ID > "$ID_FILE"

FILENAME="${ID}-$(printf "%03d" $ID)-${SLUG}.${STAGE}.prompt.md"
FILEPATH="history/prompts/${STAGE}/${FILENAME}"

# Create the template content
cat > "$FILEPATH" << EOF
---
id: "$(printf "%03d" $ID)"
title: "${SLUG}"
stage: "${STAGE}"
date: "$(date +%Y-%m-%d)"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "${FEATURE:-none}"
branch: "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'main')"
user: "$USER"
command: ""
labels: []
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files: []
tests: []
---

# Prompt History Record

## Original Prompt
\`\`\`
Enter original prompt here
\`\`\`

## Response Summary
Enter response summary here

## Outcome
Enter outcome here
EOF

if [ "$JSON" = true ]; then
  echo "{\"path\":\"$FILEPATH\",\"id\":\"$(printf "%03d" $ID)\",\"title\":\"$SLUG\",\"stage\":\"$STAGE\"}"
else
  echo "Created PHR: $FILEPATH"
fi