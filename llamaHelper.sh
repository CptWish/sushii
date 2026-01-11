#!/usr/bin/env bash
set -euo pipefail

############################################
# CONFIG
############################################
WORKDIR="$HOME/llama_local"
LLAMA_CPP_DIR="$WORKDIR/llama.cpp"
BUILD_DIR="$LLAMA_CPP_DIR/build"

MODELS_DIR="$HOME/models"
MODEL_FILE="Meta-Llama-3.1-8B-Instruct-Q2_K.gguf"
MODEL_PATH="$MODELS_DIR/$MODEL_FILE"
MODEL_URL="https://huggingface.co/bullerwins/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q2_K.gguf?download=true"

HOST="127.0.0.1"
PORT="8080"

LLAMA_SERVER_BIN="$BUILD_DIR/bin/llama-server"
BUILD_STAMP="$BUILD_DIR/.built_head"

############################################
# HELPERS
############################################
log(){ echo "[+] $1"; }
warn(){ echo "[!] $1" >&2; }
need_cmd(){ command -v "$1" >/dev/null 2>&1; }
is_file_ok(){ [ -f "$1" ] && [ -s "$1" ]; }  # exists and non-empty

install_if_missing(){
  local pkgs=()
  need_cmd cmake || pkgs+=("cmake")
  need_cmd git || pkgs+=("git")
  need_cmd g++ || pkgs+=("build-essential")
  need_cmd wget || pkgs+=("wget")
  if [ "${#pkgs[@]}" -gt 0 ]; then
    log "Installing missing packages: ${pkgs[*]}"
    sudo apt-get update
    sudo apt-get install -y "${pkgs[@]}"
  else
    log "Dependencies already installed (cmake/git/g++/wget)"
  fi
}

download_model_if_missing(){
  mkdir -p "$MODELS_DIR"
  if is_file_ok "$MODEL_PATH"; then
    log "Model already present: $MODEL_PATH"
  else
    log "Downloading GGUF model..."
    log "Source: $MODEL_URL"
    wget -O "$MODEL_PATH" "$MODEL_URL"
    is_file_ok "$MODEL_PATH" || { rm -f "$MODEL_PATH"; exit 1; }
    log "Model downloaded: $MODEL_PATH"
  fi
}

clone_llama_if_missing(){
  mkdir -p "$WORKDIR"
  if [ -d "$LLAMA_CPP_DIR/.git" ]; then
    log "llama.cpp already cloned: $LLAMA_CPP_DIR"
  else
    log "Cloning llama.cpp..."
    git clone https://github.com/ggml-org/llama.cpp "$LLAMA_CPP_DIR"
  fi
}

get_repo_head(){
  (cd "$LLAMA_CPP_DIR" && git rev-parse HEAD)
}

build_llama_if_needed(){
  # If llama-server exists, only rebuild if HEAD changed (optional smart behavior).
  mkdir -p "$BUILD_DIR"

  local head=""
  head="$(get_repo_head)"

  if [ -x "$LLAMA_SERVER_BIN" ]; then
    if [ -f "$BUILD_STAMP" ] && [ "$(cat "$BUILD_STAMP")" = "$head" ]; then
      log "llama-server already built and up-to-date (no rebuild)"
      return
    fi
    warn "llama-server exists but repo HEAD changed (rebuilding)"
  else
    log "llama-server not found (building)"
  fi

  log "Configuring build..."
  (cd "$LLAMA_CPP_DIR" && cmake -B build)

  log "Building..."
  (cd "$LLAMA_CPP_DIR" && cmake --build build -j)

  [ -x "$LLAMA_SERVER_BIN" ] || { warn "Build finished but llama-server missing"; exit 1; }

  echo "$head" > "$BUILD_STAMP"
  log "Build OK: $LLAMA_SERVER_BIN"
}

############################################
# MAIN
############################################
install_if_missing
download_model_if_missing
clone_llama_if_missing
build_llama_if_needed

log "Starting llama-server (local only)"
log "Model: $MODEL_PATH"
log "URL: http://$HOST:$PORT"

exec "$LLAMA_SERVER_BIN" \
  -m "$MODEL_PATH" \
  --host "$HOST" \
  --port "$PORT"
