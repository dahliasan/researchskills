# Editing a Word manuscript the user may have open

When the manuscript is a `.docx` on disk (often on OneDrive or Google Drive), the user may have it open in Microsoft Word. Word does not reload a file changed underneath it, and AutoSave can overwrite the agent's edits, or the agent can overwrite edits the user has not saved. So bracket every write to the file with a close and a reopen.

Helper (macOS): `scripts/word_doc.sh status|close|open <file.docx>`.

## Procedure

1. **Before reading the file**, check it: `word_doc.sh status <file>`.
   - `open` or `open-unsaved`: run `word_doc.sh close <file>`. This saves the user's changes first, then closes the document, so the file on disk is the latest version. Tell the user in one line that you closed it to apply edits.
   - `closed`: continue.
2. **Read the file from disk after closing**, never from an earlier copy. The user may have changed it since (resolved comments, edited text). Edit that version in place rather than rebuilding it from an older source.
3. **Write the edits.** If the project keeps versions, archive the previous file first, then save the new file under the current name.
4. **Reopen it** if it was open before: `word_doc.sh open <file>`. Reopen it also when the user asks to see the result.

## Notes

- Never close or reopen documents other than the one being edited.
- `close` always saves (`saving yes`), so the user's unsaved work is kept. If Word shows a dialog (for example a OneDrive conflict), stop and tell the user rather than retrying.
- Documents opened from OneDrive or SharePoint report a URL as their full name; the helper falls back to matching the file name.
- On other platforms, ask the user to close the document before editing.
