#!/bin/sh

# Build a Windows .exe binary

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Reading config..."
source "$DIR/config-dev.sh" "$@" || exit 1
echo "Building $APP_NAME..."

echo "Calling pyinstaller..."
pyinstaller --noconfirm "$DIR/specs/windows-dev.spec" || exit 1

echo "Success!"
