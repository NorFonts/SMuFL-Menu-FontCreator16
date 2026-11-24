#!/usr/bin/env python3
"""SMuFL organized glyph sets for FontCreator 16 (macOS): preview and add-only install.

Copyright © 2026 Nor Eddine Bahha — NorFonts. https://norfont.com

Uses local smufl_organized.py to obtain the same verified SMuFL catalog as the
FontLab project. Installs only new .glyphset files in the personal
FontCreator 16 GlyphSets directory, never in the app bundle. No overwrites,
renames, deletions or backup files. Writes use exclusive file creation.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import os
from pathlib import Path
import re
import sys

import smufl_organized as source

# The native Glyph Set already appears below FontCreator's `SMuFL` folder.
# Keep the filenames and set labels short (e.g. Accidentals.glyphset).
UNICODE_NAME = re.compile(r'(?:uni([0-9A-Fa-f]{4})|u([0-9A-Fa-f]{5,6}))\Z')


def unicode_from_fontlab(name: str) -> int:
    match = UNICODE_NAME.fullmatch(name)
    if match is None:
        raise ValueError('Unexpected glyph name from source: ' + name)
    cp = int(match.group(1) or match.group(2), 16)
    if cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
        raise ValueError('Invalid Unicode codepoint for glyph: ' + name)
    return cp


def safe_title(name: str) -> str:
    # FontCreator section headings are one physical line, within [square brackets].
    if not name or any(c in name for c in '[]\r\n'):
        raise ValueError('Unsafe section title: ' + repr(name))
    return name.strip()


def short_group(group: str) -> str:
    if not group.startswith('SMuFL '):
        raise ValueError('Unexpected group name: ' + repr(group))
    tail = group[len('SMuFL '):].strip()
    return safe_title(tail)


def filename(group: str) -> str:
    tail = short_group(group)
    slug = re.sub(r'[^A-Za-z0-9]+', '-', tail).strip('-')
    if not slug:
        raise ValueError('Empty group name')
    return f'{slug}.glyphset'


def grouped_catalog(entries):
    groups = defaultdict(list)
    for group, title, names, origin in entries:
        if group not in source.GROUP_ORDER:
            raise ValueError('Unexpected group: ' + group)
        if not names:
            raise ValueError('Empty group entry: ' + title)
        groups[group].append((safe_title(title), tuple(unicode_from_fontlab(x) for x in names)))
    if not groups:
        raise ValueError('No glyph collections generated')
    for name in groups:
        titles = [title.casefold() for title, codes in groups[name]]
        if len(titles) != len(set(titles)):
            raise ValueError('Duplicate glyph-set section in ' + name)
    return groups


def render_glyphset(group: str, members, order: int) -> bytes:
    """Use the grammar specified in the bundled FontCreator 16 GlyphSets/ReadMe.txt."""
    safe_title(group)
    lines = [
        '# SMuFL Glyph Sets for FontCreator 16',
        '# Copyright © 2026 Nor Eddine Bahha — NorFonts',
        '# Website: https://norfont.com',
        '# Generated from the same metadata catalog as SMuFL Menus for FontLab 8 & 9.',
        '# Source metadata: https://github.com/Shinianqi/SMuFL-Glyphs4',
        '# Third-party materials retain their applicable licenses.',
        '# Select a Glyph Set to browse; avoid "Complete Category" unless you intend to add glyphs.',
        f'name = {short_group(group)}',
        'folder = SMuFL',
        f'order = {order}',
    ]
    for title, codepoints in members:
        lines.append(f'[{safe_title(title)}]')
        # Keep the original source ordering (Unicode order in original converter).
        lines.extend(f'0x{cp:04X}' for cp in dict.fromkeys(codepoints))
    return ('\n'.join(lines) + '\n').encode('utf-8')


def prepare_catalog(source_dir=None):
    data = source.load_sources(source_dir)
    codes = source.validate_sources(data)
    entries, aliases, missing = source.make_catalog(data, codes)
    groups = grouped_catalog(entries)
    return codes, groups, aliases, missing



USER_DATA_ROOT = Path.home() / 'Library' / 'High-Logic' / 'FontCreator' / '16.0'
USER_GLYPHSETS = USER_DATA_ROOT / 'GlyphSets'


def safe_user_folder(folder: Path) -> None:
    """Affects only ~/Library/High-Logic/FontCreator/16.0/GlyphSets."""
    expected = Path.home() / 'Library' / 'High-Logic' / 'FontCreator' / '16.0' / 'GlyphSets'
    if folder != expected:
        raise ValueError('Destination must be the personal FontCreator 16.0 GlyphSets folder')
    if 'FontCreator.app' in folder.parts:
        raise ValueError('Cannot write inside an application bundle')
    if not USER_DATA_ROOT.is_dir():
        raise ValueError('FontCreator 16.0 user data folder not found: ' + str(USER_DATA_ROOT))
    # Reject indirection through any component of the user-data path.
    for part in (USER_DATA_ROOT, *USER_DATA_ROOT.parents):
        if part.is_symlink():
            raise ValueError('Symlinked user-data path is not allowed: ' + str(part))
    if folder.is_symlink():
        raise ValueError('GlyphSets is a symlink; refusing to write')
    if folder.exists() and not folder.is_dir():
        raise ValueError('GlyphSets path exists but is not a directory: ' + str(folder))


def normalized_category(s: str) -> str:
    """Match old and new display names to avoid duplicate SMuFL groups."""
    s = re.sub(r'[^a-z0-9]+', ' ', s.casefold()).strip()
    if s.startswith('norfonts '):
        s = s[len('norfonts '):]
    if s.startswith('smufl '):
        s = s[len('smufl '):]
    return s


def old_glyphsets(folder: Path):
    """Read only small text headers of existing .glyphset files."""
    found = {}
    by_name = {}
    if not folder.exists():
        return found, by_name
    for item in sorted(folder.iterdir(), key=lambda p: p.name.casefold()):
        by_name.setdefault(item.name.casefold(), item)
        if item.suffix.casefold() != '.glyphset' or item.is_symlink() or not item.is_file():
            continue
        try:
            with item.open('rb') as f:
                header = f.read(16384).decode('utf-8-sig', errors='replace')
        except (OSError, UnicodeError):
            continue
        metadata = {}
        for line in header.splitlines():
            line = line.strip()
            if line.startswith('#') or line.startswith('['):
                continue
            m = re.fullmatch(r'(name|folder)\s*=\s*(.*)', line, flags=re.I)
            if m:
                metadata[m.group(1).casefold()] = m.group(2).strip()
            if 'name' in metadata and 'folder' in metadata:
                break
        if metadata.get('folder', '').casefold() == 'smufl':
            title = metadata.get('name', item.stem)
            key = normalized_category(title)
            if key:
                found.setdefault(key, item)
    return found, by_name


def plan_entries(files: dict[str, bytes], folder: Path):
    """Return [(filename, payload, decision, existing_path)] without writing."""
    safe_user_folder(folder)
    existing_groups, existing_names = old_glyphsets(folder)
    plan = []
    for name, payload in files.items():
        name_key = name.casefold()
        group_key = normalized_category(Path(name).stem)
        if name_key in existing_names:
            plan.append((name, payload, 'skip-existing-name', existing_names[name_key]))
        elif group_key in existing_groups:
            plan.append((name, payload, 'skip-existing-category', existing_groups[group_key]))
        else:
            plan.append((name, payload, 'add', None))
    return plan


def direct_install(files: dict[str, bytes], folder: Path, preview: bool) -> tuple[int, int]:
    plan = plan_entries(files, folder)
    if not folder.exists():
        print('GlyphSets folder:', 'WILL CREATE' if preview else 'CREATING', folder)
    print('Destination:', folder)
    if not preview:
        # Create ONLY the missing GlyphSets leaf directory, not user-data ancestors.
        # EEXIST is harmless if another process created the directory concurrently.
        folder.mkdir(mode=0o755, exist_ok=True)
        safe_user_folder(folder)
    added = skipped = 0
    for name, payload, decision, existing in plan:
        if decision != 'add':
            skipped += 1
            print('SKIP:', name, '— existing:', existing.name)
            continue
        if preview:
            print('WOULD ADD:', name)
            added += 1
            continue
        path = folder / name
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, 'O_NOFOLLOW'):
            flags |= os.O_NOFOLLOW
        try:
            fd = os.open(path, flags, 0o644)
        except FileExistsError:
            skipped += 1
            print('SKIP (created concurrently):', name)
            continue
        with os.fdopen(fd, 'wb') as output:
            output.write(payload)
        added += 1
        print('ADDED:', name)
    verb = 'would add' if preview else 'added'
    print(f'Finished: {added} {verb}; {skipped} existing categories/files skipped.')
    print('No existing files were replaced, renamed, deleted, or backed up.')
    return added, skipped


def warn_app_bundle_copies():
    """Read-only advisory: old experimental files may still be in the app bundle."""
    builtin = Path('/Applications/FontCreator.app/Contents/Resources/GlyphSets')
    if builtin.is_dir():
        try:
            extras = [p.name for p in builtin.iterdir()
                      if p.suffix.casefold() == '.glyphset' and (
                        p.name.casefold().startswith(('smufl-', 'norfonts-smufl-')))]
        except OSError:
            extras = []
        if extras:
            print('NOTE: Found earlier experimental SMuFL Glyph Sets in the APP bundle:')
            for name in extras[:12]:
                print('  ', name)
            if len(extras) > 12:
                print(f'  ... and {len(extras) - 12} more')
            print('They were NOT changed. App-bundle duplicates can affect the Categories panel.')


def main():
    p = argparse.ArgumentParser(description='SMuFL native Glyph Sets for FontCreator 16: safe add-only personal-folder installer')
    action = p.add_mutually_exclusive_group(required=True)
    action.add_argument('--preview', action='store_true', help='Read-only: show planned additions to personal GlyphSets folder')
    action.add_argument('--add-one', action='store_true', help='Install the Accidentals set only, if absent')
    action.add_argument('--add-all', action='store_true', help='Install all 23 missing Glyph Sets; skip existing')
    p.add_argument('--source-dir', help='Optional local source repository for offline use')
    args = p.parse_args()
    print('SMuFL Glyph Sets for FontCreator 16 — Nor Eddine Bahha / NorFonts')
    print('https://norfont.com — © 2026 Nor Eddine Bahha')
    print('ADD ONLY • NO OVERWRITES • NO DELETIONS • NO BACKUPS')
    print('FontCreator must be closed during installation; fonts and app bundles are never modified.')
    codes, groups, aliases, missing = prepare_catalog(args.source_dir)
    print(f'Catalog: {len(codes)} glyph definitions, {len(groups)} groups, '
          f'{sum(len(v) for v in groups.values())} subcollections.')
    for n in source.GROUP_ORDER:
        if n in groups:
            print(f'  {short_group(n)}: {len(groups[n])} sections')
    if missing:
        print(f'Note: {len(missing)} empty data sets skipped')
    print(f'Consolidated {len(aliases)} identical detailed collections')
    if len(groups) != 23:
        raise ValueError('Expected 23 groups; refusing to install incomplete collection')
    if args.add_one:
        selected = ['SMuFL Accidentals']
    else:
        selected = [g for g in source.GROUP_ORDER if g in groups]
    outputs = {filename(g): render_glyphset(g, groups[g], (source.GROUP_ORDER.index(g) + 1) * 10)
               for g in selected}
    if len(outputs) != len(selected):
        raise ValueError('Generated filenames not unique; refusing to install')
    direct_install(outputs, USER_GLYPHSETS, preview=args.preview)
    warn_app_bundle_copies()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}: {exc}', file=sys.stderr)
        sys.exit(1)
