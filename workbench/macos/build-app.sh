#!/bin/zsh
set -euo pipefail

script_dir="${0:A:h}"
workbench_dir="${script_dir:h}"
build_dir="$workbench_dir/build"
app_dir="$build_dir/Dalala 封面工作台.app"

rm -rf "$app_dir"
mkdir -p "$app_dir/Contents/MacOS" "$app_dir/Contents/Resources"

/usr/bin/clang -fobjc-arc \
  -framework Cocoa \
  -framework WebKit \
  -framework UniformTypeIdentifiers \
  "$script_dir/DalalaCoverWorkbench.m" \
  -o "$app_dir/Contents/MacOS/DalalaCoverWorkbench"

cp "$script_dir/Info.plist" "$app_dir/Contents/Info.plist"
cp "$script_dir/ensure-server.sh" "$app_dir/Contents/Resources/ensure-server.sh"
cp "$workbench_dir/public/assets/brand/dalala-three-eye-cat-workbench-icon.png" "$app_dir/Contents/Resources/AppIcon.png"
chmod +x "$app_dir/Contents/MacOS/DalalaCoverWorkbench" "$app_dir/Contents/Resources/ensure-server.sh"
/usr/bin/codesign --force --deep --sign - "$app_dir"
/usr/bin/touch "$app_dir"

echo "$app_dir"
