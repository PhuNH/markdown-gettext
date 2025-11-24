# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple
from pathlib import Path

import polib
import yaml
from mdit_py_i18n import utils


@dataclass
class I18NEntry:
    msgid: str
    occurrences: List[Tuple[str, int]] = field(default_factory=list)
    comment: str = ''
    msgctxt: str = ''

    def to_poentry(self) -> polib.POEntry:
        return polib.POEntry(msgid=self.msgid,
                             msgstr='',
                             # 0 passed to polib will be lost, use `str` to keep 0
                             occurrences=[(o[0], str(o[1])) for o in self.occurrences],
                             comment=self.comment,
                             msgctxt=self.msgctxt if self.msgctxt != '' else None)


class DomainExtraction:
    """
    Implements `DomainExtractionProtocol`
    """
    def __init__(self):
        self.entries: List[I18NEntry] = []

    def add_entry(self, path: str, msgid: str, line_num: int, comment: str = '', msgctxt: str = ''):
        if not msgid:
            return
        for e in self.entries:
            if msgid == e.msgid and msgctxt == e.msgctxt:
                e.occurrences.append((path, line_num))
                return
        self.entries.append(I18NEntry(msgid, [(path, line_num)], comment, msgctxt))

    def i12ize_front_matter(self, o, path: str):
        """Internationalize an object in front matter.
        :param o: the object being processed
        :param path: path of the source file
        :return: None. Messages are added to the `entries` list.
        """
        if isinstance(o, str) and o and not utils.SPACES_PATTERN.fullmatch(o):
            self.add_entry(path, o, 0)
        elif isinstance(o, list) or isinstance(o, dict):
            for _, value in (enumerate(o) if isinstance(o, list) else o.items()):
                self.i12ize_front_matter(value, path)

    def render_front_matter(self, path: str, content: str, _markup: str):
        fm = yaml.safe_load(content)
        self.i12ize_front_matter(fm, path)

    def open_existing_pot(self, dest_path: str):
        """
        Open existing pot file if present and create a map to fast access to
        messages by msgid
        """
        if not Path(dest_path).exists():
            return None
        existing_pot = polib.pofile(dest_path)
        existing_pot.map_by_id = {e.msgid: e for e in existing_pot}
        return existing_pot

    def make_pot(self, package: str, report_address: str, team_address: str, dest_path: str):
        pot = polib.POFile()
        pot.metadata = {
            'Project-Id-Version': f'{package} 1.0',
            'Report-Msgid-Bugs-To': report_address,
            'POT-Creation-Date': datetime.now().astimezone().strftime('%Y-%m-%d %H:%M%z'),
            'PO-Revision-Date': 'YEAR-MO-DA HO:MI+ZONE',
            'Last-Translator': 'FULL NAME <EMAIL@ADDRESS>',
            'Language-Team': f'LANGUAGE <{team_address}>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

        existing_pot = self.open_existing_pot(dest_path)
        for e in self.entries:
            # preserve existing comments
            if (
                not e.comment
                and existing_pot
                and e.msgid in existing_pot.map_by_id
            ):
                e.comment = existing_pot.map_by_id[e.msgid].comment

            pot.append(e.to_poentry())
        pot.save(dest_path)
