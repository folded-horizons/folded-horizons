#!/usr/bin/env bash
# Stand up a throwaway NeoForge test server with the pack + companion mod.
#
#   scripts/test-server.sh          # start (downloads server + mods on first run)
#   scripts/test-server.sh --fresh  # wipe the world first
#   scripts/test-server.sh --stop   # stop a running test server
#
# The server runs in the background with a console you can read, listens on
# 25565, and is EULA-accepted for you (Mojang requires it; you are accepting
# it by running this script).
#
# Layout (gitignored):
#   .test-server/          server jar + libraries + world
#   .test-server/mods/     pack mods + the built companion jar
#
# Requirements: java 21, and pakku (for `pakku fetch`). Run it inside the
# dev container, where both exist.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_DIR="$REPO_ROOT/.test-server"
MC_VERSION="1.21.1"
NEO_VERSION="21.1.264"
CORE_JAR="$REPO_ROOT/companion/core/build/libs/foldedhorizons-0.1.0.jar"

info()  { printf '\033[36m==>\033[0m %s\n' "$*"; }
warn()  { printf '\033[33m==>\033[0m %s\n' "$*"; }
die()   { printf '\033[31m==> %s\033[0m\n' "$*" >&2; exit 1; }

if [[ "${1:-}" == "--stop" ]]; then
    # The pid file holds run.sh's shell; the JVM is its child and would
    # survive killing only the shell. scripts/stop-test-server.sh walks
    # /proc and kills the java process itself.
    bash "$REPO_ROOT/scripts/stop-test-server.sh"
    rm -f "$SERVER_DIR/server.pid"
    exit 0
fi

command -v java >/dev/null || die "java not found — run this inside the dev container"
command -v pakku >/dev/null || die "pakku not found — run this inside the dev container"

# ---------------------------------------------------------------- mods
info "fetching pack mods (pakku fetch)"
(cd "$REPO_ROOT" && pakku fetch >/dev/null)

if [[ ! -f "$CORE_JAR" ]]; then
    warn "companion jar not built yet: $CORE_JAR"
    die "build it first:  cd companion && gradle :core:build"
fi

# ---------------------------------------------------------------- server
mkdir -p "$SERVER_DIR/mods"

if [[ "${1:-}" == "--fresh" ]]; then
    info "wiping world"
    rm -rf "$SERVER_DIR/world" "$SERVER_DIR/logs"
fi

# The installer lays down libraries/ + run.sh rather than a server.jar, so
# that argument file is the "already installed" sentinel.
INSTALLED_ARGS="$SERVER_DIR/libraries/net/neoforged/neoforge/${NEO_VERSION}/unix_args.txt"

if [[ ! -f "$INSTALLED_ARGS" ]]; then
    info "downloading NeoForge ${NEO_VERSION} installer"
    installer="$SERVER_DIR/neoforge-installer.jar"
    curl -fsSL -o "$installer" \
        "https://maven.neoforged.net/releases/net/neoforged/neoforge/${NEO_VERSION}/neoforge-${NEO_VERSION}-installer.jar"
    info "installing server (this takes a minute)"
    (cd "$SERVER_DIR" && java -jar "$installer" --installServer . >/dev/null 2>&1) \
        || die "NeoForge installer failed — see $SERVER_DIR/logs"
    rm -f "$installer" "$installer.log"
fi

# Sync mods: pack mods + the companion jar, nothing stale.
#
# Client-only projects are excluded: some of them (Sodium) run client-side
# checks in a pre-launch service that crashes a dedicated server before
# NeoForge's side filtering can skip them. The lockfile's `options.side`
# is the source of truth, so this stays correct as the pack changes.
info "syncing mods"
find "$SERVER_DIR/mods" -name '*.jar' -delete

client_only=$(python3 - "$REPO_ROOT/pakku-lock.json" <<'PY'
import json, sys
lock = json.load(open(sys.argv[1]))
for proj in lock.get('projects', []):
    # pakku stores this as a top-level "side" field ("CLIENT" / "SERVER" /
    # "BOTH"); older/override configs may nest it under "options".
    side = proj.get('side') or (proj.get('options') or {}).get('side')
    if side == 'CLIENT':
        for f in proj.get('files', []):
            if name := f.get('file_name'):
                print(name)
PY
)

copied=0
for jar in "$REPO_ROOT"/mods/*.jar; do
    base=$(basename "$jar")
    if grep -qxF "$base" <<< "$client_only"; then
        info "skipping client-only mod: $base"
        continue
    fi
    cp "$jar" "$SERVER_DIR/mods/"
    copied=$((copied + 1))
done
cp "$CORE_JAR" "$SERVER_DIR/mods/"
info "$copied pack mods + companion jar"
unset client_only

# Accept the EULA (you accept it by running this script).
echo "eula=true" > "$SERVER_DIR/eula.txt"

# RCON is on so a test can drive the server without a client (that is how
# the gameplay checks are run). Local throwaway world, fixed password, the
# port is only published to 127.0.0.1 by the devcontainer.
cat > "$SERVER_DIR/server.properties" <<'PROPS'
level-name=world
online-mode=false
server-port=25565
max-tick-time=-1
view-distance=8
spawn-protection=0
sync-chunk-writes=false
enable-rcon=true
rcon.port=25575
rcon.password=testserver
PROPS

# Enough heap for GregTech + AE2.
cat > "$SERVER_DIR/user_jvm_args.txt" <<'ARGS'
-Xms1G
-Xmx4G
ARGS

# ---------------------------------------------------------------- run
info "starting server (log: $SERVER_DIR/logs/latest.log)"
cd "$SERVER_DIR"
nohup ./run.sh nogui > "$SERVER_DIR/console.log" 2>&1 &
echo $! > "$SERVER_DIR/server.pid"

info "pid $(cat "$SERVER_DIR/server.pid") — tailing until the server is up"

deadline=$(( SECONDS + 300 ))
while (( SECONDS < deadline )); do
    if grep -q 'Done (' "$SERVER_DIR/console.log" 2>/dev/null; then
        info "server ready on port 25565"
        grep -E 'Done \(|Folded Horizons|Loaded [0-9]+ mods' "$SERVER_DIR/console.log" | tail -3
        echo
        info "connect to: localhost:25565"
        info "console:    tail -f $SERVER_DIR/console.log"
        info "stop with:  scripts/test-server.sh --stop"
        exit 0
    fi
    # Only fatal signals count. Mixin's "Error loading class: ...
    # (java.lang.ClassNotFoundException)" WARNs are routine for optional
    # integrations and do not stop the server, so matching bare
    # "Exception" would fail healthy boots.
    if grep -qE 'has failed to load correctly|Error initialising mixin config|Encountered an unexpected exception|FAILED TO BIND TO PORT|Exception in thread "main"|Crash report|Failed to start' "$SERVER_DIR/console.log" 2>/dev/null; then
        warn "server reported a problem:"
        grep -nE 'has failed to load correctly|Error initialising mixin config|Encountered an unexpected exception|FAILED TO BIND TO PORT|Exception in thread "main"|Caused by' "$SERVER_DIR/console.log" | head -20
        warn "full log: $SERVER_DIR/console.log"
        exit 1
    fi
    sleep 2
done

warn "server did not finish starting within 5 minutes"
tail -30 "$SERVER_DIR/console.log"
exit 1
