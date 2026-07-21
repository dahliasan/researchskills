# Install — Manuscript Markdown

Required for `/manuscript-markdown`. Agents must **flag** a missing install
instead of pretending conversion succeeded.

## CLI (agents)

Standalone binary from GitHub Releases (preferred for terminal conversion):

1. Open [releases](https://github.com/jbearak/manuscript-markdown/releases)
2. Download the build for this OS/arch (e.g. `manuscript-markdown-darwin-arm64`)
3. Install somewhere on `PATH`:

```bash
mkdir -p "$HOME/bin"
curl -fsSL -o "$HOME/bin/manuscript-markdown" \
  "https://github.com/jbearak/manuscript-markdown/releases/download/vVERSION/manuscript-markdown-darwin-arm64"
chmod +x "$HOME/bin/manuscript-markdown"
# ensure ~/bin is on PATH
manuscript-markdown --version
```

Replace `vVERSION` and the asset name with the current release. Also available:
`darwin-x64`, `linux-arm64`, `linux-x64`, `windows-x64.exe`.

From a clone of the upstream repo:

```bash
./setup.sh   # installs ~/bin/manuscript-markdown
```

`npx manuscript-markdown` is **not** published on npm.

## VS Code / Cursor extension (humans)

Editor UI for CriticMarkup annotations, preview, and right-click
**Export to Markdown** / **Export to Word**.

- Marketplace ID: `jbearak.manuscript-markdown`
- Or install the `.vsix` from the same Releases page
- OpenVSX also lists the extension when Marketplace is unavailable

**Agent note:** Conversion can proceed with CLI alone. Still flag a missing
extension when the user expects in-editor roundtrip.

## Doctor checklist

```text
[ ] manuscript-markdown on PATH
[ ] manuscript-markdown --version prints a semver
[ ] (optional) extension jbearak.manuscript-markdown installed in the editor
```

If any required item fails, stop conversion and print install steps from this
file.
