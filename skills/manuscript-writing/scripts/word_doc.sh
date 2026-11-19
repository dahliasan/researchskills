#!/usr/bin/env bash
# Keep Microsoft Word (macOS) in step with agent edits to a .docx on disk.
#   word_doc.sh status <file.docx>   -> "open", "open-unsaved" or "closed"
#   word_doc.sh close  <file.docx>   -> save the user's changes, then close it (no-op if closed)
#   word_doc.sh open   <file.docx>   -> open (or reopen) it in Word
# Matches the open document by full path, falling back to the file name
# (documents opened from OneDrive/SharePoint report a URL as their full name).
set -euo pipefail
cmd=${1:-}; f=${2:-}
[[ -n $cmd && -n $f ]] || { sed -n '2,7p' "$0"; exit 2; }
abs=$(cd "$(dirname "$f")" && pwd)/$(basename "$f")
name=$(basename "$f")

running() { pgrep -x "Microsoft Word" >/dev/null; }

# Prints the index (1-based) of the matching open document, or nothing.
find_doc() {
  running || return 0
  osascript - "$abs" "$name" <<'OSA'
on run argv
  set want to item 1 of argv
  set wantName to item 2 of argv
  tell application "Microsoft Word"
    set n to count of documents
    repeat with i from 1 to n
      set d to document i
      set fn to full name of d
      try
        set p to POSIX path of (fn as alias)
      on error
        set p to fn
      end try
      if p is want or (name of d) is wantName then return i as text
    end repeat
  end tell
  return ""
end run
OSA
}

case $cmd in
  status)
    i=$(find_doc)
    if [[ -z $i ]]; then echo closed; exit 0; fi
    saved=$(osascript -e "tell application \"Microsoft Word\" to get saved of document $i")
    [[ $saved == true ]] && echo open || echo open-unsaved ;;
  close)
    i=$(find_doc)
    [[ -z $i ]] && { echo "not open"; exit 0; }
    osascript -e "tell application \"Microsoft Word\" to close document $i saving yes" >/dev/null
    # wait for Word to release the file (owner lock file ~$name disappears)
    lock="$(dirname "$abs")/~\$${name:2}"
    for _ in $(seq 1 20); do [[ -e $lock ]] || break; sleep 0.5; done
    echo "saved and closed" ;;
  open)
    open -a "Microsoft Word" "$abs"; echo "opened" ;;
  *) sed -n '2,7p' "$0"; exit 2 ;;
esac
