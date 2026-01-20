#!/bin/bash

# Smart commit helper
# Generates conventional commit messages

echo "🎯 Smart Commit Helper"
echo ""

# Get changed files
files=$(git diff --cached --name-only)
if [ -z "$files" ]; then
  echo "❌ No staged changes"
  exit 1
fi

# Infer commit type
echo "Changed files:"
echo "$files"
echo ""

# Ask for commit type
echo "Select commit type:"
select type in "feat" "fix" "docs" "style" "refactor" "test" "chore"; do
  case $type in
    feat|fix|docs|style|refactor|test|chore)
      break
      ;;
  esac
done

# Get scope
echo ""
echo "Enter scope (optional, press enter to skip):"
read scope

# Get description
echo ""
echo "Enter description:"
read description

# Build commit message
if [ -z "$scope" ]; then
  message="$type: $description"
else
  message="$type($scope): $description"
fi

echo ""
echo "Commit message:"
echo "  $message"
echo ""

# Confirm
echo "Commit with this message? (y/n)"
read confirm

if [ "$confirm" = "y" ]; then
  git commit -m "$message"
  echo "✅ Committed!"
else
  echo "❌ Cancelled"
  exit 1
fi