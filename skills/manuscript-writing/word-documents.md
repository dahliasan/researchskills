# Editing a Word manuscript the user may have open

When the manuscript is a `.docx` on disk (often on OneDrive or Google Drive), the user may have it open in Microsoft Word. Word does not reload a file changed underneath it, and AutoSave can overwrite the agent's edits, or the agent can overwrite edits the user has not saved. So bracket every write to the file with a close and a reopen.

Helper (macOS): `scripts/word_doc.sh status|close|open <file.docx>` and `scripts/word_doc.sh list`.

## Procedure

0. **Confirm which file is the working draft.** Draft filenames change between passes, and project docs can name an older file. List the draft folder (newest first) and run `word_doc.sh list` to see what Word has open. If a newer `.docx` exists than the one you were pointed to, or Word has a different version open, ask which is current before editing. Editing a stale copy leaves the user looking at a draft without your changes.
1. **Before EVERY edit pass** (including tiny follow-up fixes in the same session), check the open file: `word_doc.sh status <file>`.
   - `open` or `open-unsaved`: run `word_doc.sh close <file>`. This saves the user's changes first (`saving yes`), then closes the document, so the file on disk is the latest version. **Never** close with `saving no` before reading, and **never** skip saving/closing just because you edited the file a minute ago. Tell the user in one line that you closed it to apply edits.
   - `closed`: continue.
2. **Always re-read the live file from disk after saving/closing and check for user edits**, NEVER edit a cached `/tmp/` or earlier intermediate copy. The user may have edited text, resolved/added comments, or refreshed Zotero in Word between turns. Diff the freshly saved file against your last output if helpful, and build every new edit strictly on top of the user's latest saved file so zero manual edits are ever lost.
3. **Write the edits.** If the project keeps versions, archive the previous file first, then save the new file under the current name.
4. **Reopen it** when done: `word_doc.sh open <file>`, whether or not it was open before, so the user sees the edited version. Skip this only if the user asked you not to.

## Tracked changes: use the shared tool

Write edits to a `.docx` with `scripts/track_edit.py`. Don't write your own OOXML
editing script. Earlier sessions each rebuilt one from scratch, which was slow
and produced coarse, paragraph-sized changes.

```bash
python scripts/track_edit.py IN.docx OUT.docx --edits edits.json --author "Name"
```

`edits.json` is a list of `{"find": "text in exactly one paragraph", "text": "whole new paragraph"}`
objects. `find` matches the paragraph with all tracked changes accepted. Write
italics as `*text*`. To keep a live citation, copy its displayed text exactly,
for example `(Boyd, 1993; Boveng et al., 1998)`. The tool:

- diffs word by word, so only changed words become insertions and deletions;
- keeps existing revisions, comments, citation fields and formatting;
- refuses citation-like text that matches no field, because Zotero would stop
  managing it (`--allow-plain-citations` overrides this; prefer inserting the citation in Word);
- writes nothing unless accepting all changes gives exactly the requested text
  and rejecting this run's changes gives back the input.

Write to a new file, with the user's real name as `--author` (never an agent
name in tracked changes or comments) unless they say otherwise. When rebasing
tracked changes from a shared baseline to a revised draft, coalesce tiny 1–2
word unchanged bridges sandwiched between adjacent edits into clean phrase-level
replacements so coauthors are not faced with choppy word-by-word fragments.
Requires `lxml`. The tool edits paragraph text only. Leave tables, figures and
reference lists to Word, or ask.

## Figure and table references: link them

Cite figures and tables in the text with Word cross-references, not typed
numbers, so numbering follows the captions when figures move. Captions use
`SEQ` fields (`Figure {SEQ Figure}`, `Table {SEQ Table}`, `Supplementary Fig.
{SEQ Supplementary_Figure}`, `Supplementary Table {SEQ Supplementary_Table}`).
In-text references keep the journal label as text ("Fig. ", "Table ") and link
only the number with a `REF _Ref… \h` field to a bookmark around the caption's
`SEQ` field.

After any edit that adds or renumbers a figure or table, run
`python scripts/link_xrefs.py IN.docx OUT.docx`. It bookmarks every caption
number, adds `SEQ` fields to plain-text "Supplementary Fig. N." captions, and
turns typed references into `REF` fields. It writes nothing unless the visible
text is unchanged. When writing new text with `track_edit.py`, type the
reference as text first, then run `link_xrefs.py`. After rebasing or rewriting
captions, strip any stale/empty `_Ref*` bookmarks and unwrap stale `REF _Ref*`
fields before re-running `link_xrefs.py`, then verify `0` empty `_Ref` bookmarks
(an empty target bookmark causes Word to display `Error! Reference source not
found.`). Remind the user to update fields in Word (select all, F9) after
reordering figures.

**Model fallback.** If you find yourself struggling with the technical `.docx`
work (OOXML structure, tracked changes, embedded figures, comments or citation
fields), write the edit list and delegate the `.docx` step to an Opus 5.5
sub-agent.

## Notes

- Never close or reopen documents other than the one being edited.
- When checking a file in Word by AppleScript, open a scratch copy and address it by name (`document "copy.docx"`), never `active document`, which may be another manuscript the user has open.
- `close` always saves (`saving yes`), so the user's unsaved work is kept. If Word shows a dialog (for example a OneDrive conflict), stop and tell the user rather than retrying.
- Documents opened from OneDrive or SharePoint report a URL as their full name; the helper falls back to matching the file name.
- On other platforms, ask the user to close the document before editing.
