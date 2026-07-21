# Install — Manuscript Markdown

Required for `/manuscript-markdown`. Agents must **flag** a missing install
instead of pretending conversion succeeded.

**Product:** [Manuscript Markdown](https://marketplace.visualstudio.com/items?itemName=jbearak.manuscript-markdown)
(`jbearak.manuscript-markdown`) from
[jbearak/manuscript-markdown](https://github.com/jbearak/manuscript-markdown).
The Cursor / VS Code **extension** and the **CLI** are two surfaces of that
same product (same releases). This skill does not ship a separate converter.

## Cursor / VS Code extension (primary for humans)

In-editor CriticMarkup, preview, and right-click **Export to Markdown** /
**Export to Word**.

- Marketplace ID: `jbearak.manuscript-markdown`
- Or install the `.vsix` from the same [Releases](https://github.com/jbearak/manuscript-markdown/releases) page
- OpenVSX also lists the extension when Marketplace is unavailable

In Cursor:

```bash
cursor --install-extension jbearak.manuscript-markdown
```

**Agent note:** If the user already has the extension installed, say so and do
not reinstall. Agent terminal conversion still needs the CLI below.

## CLI (agents / terminal)

Standalone binary from GitHub Releases (same upstream as the extension;
preferred for scripted conversion):

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

## Doctor checklist

```text
[ ] extension jbearak.manuscript-markdown installed in Cursor / VS Code
    (primary for human in-editor Export)
[ ] manuscript-markdown on PATH
[ ] manuscript-markdown --version prints a semver
    (required for agent / terminal conversion)
```

- Human-only editor roundtrip: extension alone is enough.
- Agent conversion: CLI required; still report extension status.

If a required item for the requested mode fails, stop conversion and print
install steps from this file.
