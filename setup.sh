#!/usr/bin/env bash
EXTERNAL_DIR=src/external

echo "== ds-crazyflies setup =="

mkdir -p "$EXTERNAL_DIR"

# Core dependencies
echo "== Import core repos =="
vcs import "$EXTERNAL_DIR" < repos/core.repos

# Mode specific
for MODE in "$@"; do
    echo "== Setup mode: $MODE =="

    case "$MODE" in
    webots)
        echo "== Checking Webots =="
        if ! command -v webots >/dev/null 2>&1; then
        echo "Webots not installed!"
        exit 1
        fi
        

        echo "== Import webots =="
        vcs import "$EXTERNAL_DIR" < repos/webots.repos
        ;;

    sim)
        echo "== Import simulation =="
        vcs import "$EXTERNAL_DIR" < repos/sim.repos
        ;;

    hardware)
        echo "== Import hardware =="
        vcs import "$EXTERNAL_DIR" < repos/hardware.repos
        ;;
        
    *)
        echo "Usage: ./setup.sh [webots|sim|hardware]"
        exit 1
        ;;
    esac
done

# Update submodules for all imported repositories
echo "== Init git submodules (recursive) =="

find "$EXTERNAL_DIR" -name ".git" -type d | while read gitdir; do
  repo_dir=$(dirname "$gitdir")
  echo "-> submodules in $repo_dir"
  git -C "$repo_dir" submodule update --init --recursive
done

echo "== Setup complete =="
echo "Now run:"
echo "  colcon build"