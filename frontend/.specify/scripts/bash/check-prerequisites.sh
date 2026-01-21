#!/bin/bash
# Script to check prerequisites for SDD

JSON=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    -Json|--json)
      JSON=true
      shift
      ;;
    -RequireTasks|--require-tasks)
      REQUIRE_TASKS=true
      shift
      ;;
    -IncludeTasks|--include-tasks)
      INCLUDE_TASKS=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [ "$JSON" = true ]; then
  echo '{"FEATURE_DIR":"specs/todo-feature","AVAILABLE_DOCS":["spec.md","plan.md","tasks.md"]}'
else
  echo "FEATURE_DIR=specs/todo-feature"
  echo "AVAILABLE_DOCS=spec.md,plan.md,tasks.md"
fi