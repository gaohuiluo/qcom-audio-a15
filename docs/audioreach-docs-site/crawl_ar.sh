#!/usr/bin/env bash
set -u
BASE="https://audioreach.github.io"
DEST="e:/Android/qcom-audio-a15/qcom-audio/qualcomm-audioreach-blog/audioreach-docs-site/raw"
mkdir -p "$DEST"

declare -A SEEN
QUEUE=("index.html")

norm() {
  local p="$1"; p="${p%%#*}"; p="${p%%\?*}"
  local IFS='/'; read -ra parts <<< "$p"; local stack=()
  for part in "${parts[@]}"; do
    if [ "$part" = "." ] || [ -z "$part" ]; then continue
    elif [ "$part" = ".." ]; then unset 'stack[${#stack[@]}-1]' 2>/dev/null
    else stack+=("$part"); fi
  done
  local out=""; for s in "${stack[@]}"; do out="$out/$s"; done; echo "${out#/}"
}

while [ ${#QUEUE[@]} -gt 0 ]; do
  cur="${QUEUE[0]}"; QUEUE=("${QUEUE[@]:1}")
  [ -n "${SEEN[$cur]:-}" ] && continue
  SEEN[$cur]=1
  case "$cur" in *.html) ;; *) continue ;; esac
  outfile="$DEST/$cur"; mkdir -p "$(dirname "$outfile")"
  code=$(curl -sL -m 30 -o "$outfile" -w "%{http_code}" "$BASE/$cur")
  echo "[$code] $cur"
  [ "$code" != "200" ] && continue
  curdir="$(dirname "$cur")"; [ "$curdir" = "." ] && curdir=""
  links=$(grep -oE 'href="[^"]+"' "$outfile" | sed 's/href="//;s/"//')
  for l in $links; do
    case "$l" in http*|//*|mailto:*|\#*|javascript:*) continue ;; esac
    case "$l" in *.html|*.html\#*|*.html\?*) ;; *) continue ;; esac
    if [ -n "$curdir" ]; then cand="$curdir/$l"; else cand="$l"; fi
    n=$(norm "$cand"); [ -z "$n" ] && continue
    if [ -z "${SEEN[$n]:-}" ]; then QUEUE+=("$n"); fi
  done
done
echo "=== DONE ==="
find "$DEST" -name '*.html' | sort
