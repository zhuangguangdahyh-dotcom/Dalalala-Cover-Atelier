#!/bin/zsh
set -u

script_dir="${0:A:h}"
# The built app lives in workbench/build/. Keep it there or make an alias to it.
workbench_dir="${script_dir:h:h:h:h}"
if [[ ! -f "$workbench_dir/server.mjs" ]]; then
  print -u2 "找不到工作台文件：请将 App 留在下载目录的 workbench/build 文件夹，或使用访达替身。"
  exit 1
fi
health_url="http://127.0.0.1:4318/api/auth"
log_file="$workbench_dir/data/server.log"

if /usr/bin/curl -fsS --max-time 2 "$health_url" >/dev/null 2>&1; then
  exit 0
fi

# A long-running local Node process can keep the port open after macOS has
# revoked its access to the workbench folder. In that state curl reaches the
# process but the API returns an error, and starting a second server only ends
# in EADDRINUSE. Replace only the listener that belongs to this workbench.
for pid in $(/usr/sbin/lsof -tiTCP:4318 -sTCP:LISTEN 2>/dev/null); do
  process_cwd=$(/usr/sbin/lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | /usr/bin/sed -n 's/^n//p')
  process_command=$(/bin/ps -p "$pid" -o command= 2>/dev/null)
  if [[ "$process_cwd" == "$workbench_dir" && "$process_command" == *"node server.mjs"* ]]; then
    /bin/kill "$pid" 2>/dev/null || true
    for _ in {1..30}; do
      /bin/kill -0 "$pid" 2>/dev/null || break
      /bin/sleep 0.1
    done
    if /bin/kill -0 "$pid" 2>/dev/null; then
      /bin/kill -KILL "$pid" 2>/dev/null || true
    fi
  fi
done

# Do not start the replacement while the old listener is still releasing the
# port. Otherwise Node exits with EADDRINUSE and the app opens onto a dead page.
for _ in {1..50}; do
  if ! /usr/sbin/lsof -tiTCP:4318 -sTCP:LISTEN >/dev/null 2>&1; then
    break
  fi
  /bin/sleep 0.1
done

if /usr/sbin/lsof -tiTCP:4318 -sTCP:LISTEN >/dev/null 2>&1; then
  exit 1
fi

mkdir -p "$workbench_dir/data"
cd "$workbench_dir" || exit 1
PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
exec /usr/bin/env node server.mjs >>"$log_file" 2>&1
