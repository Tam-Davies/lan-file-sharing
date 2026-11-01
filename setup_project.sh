#!/bin/bash

set -e

echo "Creating LAN File Sharing project structure..."

# Directories
mkdir -p shared_files
mkdir -p database
mkdir -p templates
mkdir -p static/css
mkdir -p static/js

# Backend
touch app.py

# Dependencies
touch requirements.txt

# Environment / Git
touch .gitignore
touch .env.example

# Documentation
touch README.md

# Frontend
touch templates/index.html
touch static/css/style.css
touch static/js/app.js

# History database placeholder
touch database/.gitkeep

echo ""
echo "Project structure created successfully!"
echo ""

tree . 2>/dev/null || find . -maxdepth 3 -type f -o -type d
