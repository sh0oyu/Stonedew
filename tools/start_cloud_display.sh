#!/usr/bin/env bash
set -euo pipefail
export DISPLAY="${DISPLAY:-:99}"
if xwininfo -root >/dev/null 2>&1; then
    printf 'Display %s is available.\n' "$DISPLAY"
    exit 0
fi
display_binary=$(command -v Xvfb || true)
if [[ -z "$display_binary" && -x /workspace/.stonedew-env/xvfb/usr/bin/Xvfb ]]; then
    display_binary=/workspace/.stonedew-env/xvfb/usr/bin/Xvfb
fi
if [[ -z "$display_binary" ]]; then
    printf 'Xvfb is missing. Install it or use a desktop display.\n' >&2
    exit 1
fi
"$display_binary" "$DISPLAY" -screen 0 1280x720x24 -nolisten tcp > /tmp/stonedew-xvfb.log 2>&1 &
display_pid=$!
for attempt in {1..20}; do
    if xwininfo -root >/dev/null 2>&1; then
        printf 'Started display %s (PID %s).\n' "$DISPLAY" "$display_pid"
        exit 0
    fi
    if ! kill -0 "$display_pid" 2>/dev/null; then
        cat /tmp/stonedew-xvfb.log >&2
        exit 1
    fi
    sleep 0.25
done
printf 'Display did not become available; see /tmp/stonedew-xvfb.log.\n' >&2
exit 1
