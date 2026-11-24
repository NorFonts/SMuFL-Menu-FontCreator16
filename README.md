# SMuFL Menu for FontCreator 16

**Organized SMuFL Glyph Sets for FontCreator 16**, developed by **Nor Eddine Bahha** — [NorFonts](https://norfont.com/).

This free, community-developed project adds a structured **SMuFL** group to FontCreator's **Categories → Glyph Sets** panel. It generates **23 musical groups with 218 subcollections** from approximately **2,940 SMuFL glyph definitions**, including clefs, notes and rests, accidentals, microtonal notation, ornaments, historical notation, percussion, and more.

### Compatibility

> _**Tested on FontCreator 16 for macOS 27 Golden Gate.** Other macOS versions have not been verified. **Windows compatibility has not been tested**; the generated `.glyphset` collections might also work with the Windows edition of FontCreator, but the supplied `.command` launcher and installation directory are **macOS-only**. A separate Windows installer and user-folder verification would be required._

## Screenshots — verified in FontCreator 16 on macOS

The following are **authentic FontCreator screenshots**, not renderings or simulated sidebar previews. They show the native **Categories → Glyph Sets → SMuFL** panel.

**Dark appearance**

![SMuFL Glyph Sets in the FontCreator 16 Categories panel, dark appearance](https://norfont.com/en/wp-content/uploads/2026/11/cleanshot-2026-11-24-at-10-f17b5911.png)

<details>
<summary>Light appearance and installed files</summary>

**Light appearance**

![SMuFL Glyph Sets in FontCreator 16, light appearance](https://norfont.com/en/wp-content/uploads/2026/11/cleanshot-2026-11-24-at-10-3fa994c3.png)

**Installed category files in the personal GlyphSets folder**

![23 SMuFL glyphset files in the user's FontCreator 16 settings folder on macOS](https://norfont.com/en/wp-content/uploads/2026/11/cleanshot-2026-11-24-at-10-4c794337.png)

</details>

## Install (macOS)

Requirements: FontCreator **16** (run at least once), **Python 3.9+** available as `python3`, and internet access to retrieve the SMuFL source JSON metadata. The optional `--source-dir` argument allows a local metadata checkout instead.

1. Quit **FontCreator 16**.
2. Download this repository as a ZIP (GitHub **Code → Download ZIP**) and extract it.
3. Keep the two `.py` files next to **`Install SMuFL Glyph Sets in FontCreator 16.command`**.
4. Double-click the `.command` file (or run it from Terminal). If macOS blocks a downloaded script, inspect it first and follow macOS's standard open/trust controls.
5. Select **1 — PREVIEW** to inspect planned changes without writing anything.
6. Run again and select **3 — ADD ALL** to add missing collections. **2 — ADD ONE** installs only Accidentals for testing.
7. Restart FontCreator and expand **Categories → Glyph Sets → SMuFL**.

**Target directory (automatically created when the parent settings folder exists):**

```text
~/Library/High-Logic/FontCreator/16.0/GlyphSets/
```

## Important safety behavior

The generator uses **exclusive creation** (`O_EXCL`) for new `.glyphset` files. It **never overwrites, renames, deletes, or backs up** existing Glyph Sets. It checks for existing filenames and recognized SMuFL categories—including older names with prefixes—and skips them instead of creating replacements or duplicates.

The installer writes **only** to the personal FontCreator 16 settings folder, `~/Library/High-Logic/FontCreator/16.0/GlyphSets/`. It requires the `16.0` user-data directory to exist, rejects symlinked or invalid destination paths, and creates **only the missing `GlyphSets` folder** when necessary. It does not write inside `FontCreator.app`, change FontCreator preferences, or edit font files or glyph outlines. **PREVIEW** is read-only.

Previous SMuFL collections, including any older copies inside the application bundle, **remain untouched**. The installer cannot restore missing custom Glyph Sets or automatically remove legacy duplicates. Do not run older experimental installers or uninstallers as part of this process.


## Terminal commands

```bash
python3 smufl_fontcreator16.py --preview
python3 smufl_fontcreator16.py --add-one
python3 smufl_fontcreator16.py --add-all
```

The implementation uses `smufl_organized.py` to derive the catalog and `smufl_fontcreator16.py` to generate and safely install FontCreator-native Glyph Set files. Generated filenames are short, for example `Quick.glyphset`, `Accidentals.glyphset`, and `Notes-Rests.glyphset`. These are displayed under one parent **SMuFL** group; they are not installed into the app bundle.

> **Important:** Browsing glyph sets does not modify font outlines. FontCreator's **Complete Category** command can add missing glyphs to the open font; do not use it unless that is what you intend.

## Author

**Nor Eddine Bahha** — [NorFonts](https://norfont.com/)

This is an **independent FontCreator 16 adaptation**, not an official FontCreator Glyph Set or a product endorsed by High-Logic or the W3C Music Notation Community Group. See [NOTICE.md](NOTICE.md) for source attribution and third-party licensing.

## License and attribution

**© 2026 Nor Eddine Bahha — [NorFonts](https://norfont.com/). All rights reserved except as expressly licensed.**

The original project code is distributed under [Apache License 2.0](LICENSE). Source classification data is retrieved from [SMuFL-Glyphs4](https://github.com/Shinianqi/SMuFL-Glyphs4) and follows its own applicable licenses and notices; see [NOTICE.md](NOTICE.md). This independent project is not officially affiliated with High-Logic, FontCreator, or the SMuFL specification maintainers.