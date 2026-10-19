#!/usr/bin/env bash
# Stop any running test server without killing the calling shell.
#
# `pkill -f` is a trap here: the pattern appears in the caller's own command
# line, so pkill matches (and kills) the shell that invoked it. This script
# selects candidate PIDs by script path instead, and skips anything that is
# not a java process.
set -uo pipefail

killed=0
for pid in $(pgrep -f 'unix_args\.txt' || true); do
    [[ "$pid" == "$$" ]] && continue
    cmd=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null || true)
    case "$cmd" in
        *java*) kill -9 "$pid" 2>/dev/null && killed=$((killed + 1)) ;;
    esac
done

for pid in $(pgrep -x java || true); do
    [[ "$pid" == "$$" ]] && continue
    cmd=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null || true)
    case "$cmd" in
        *unix_args.txt*) kill -9 "$pid" 2>/dev/null && killed=$((killed + 1)) ;;
    esac
done

echo "stopped $killed server process(es)"
