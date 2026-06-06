#!/bin/bash

# Launch script for PPT Reel Converter

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Build the app first
npm run build

# Compile Electron
npx tsc --project tsconfig.electron.json

# Launch Electron
NODE_ENV=development ./node_modules/.bin/electron .