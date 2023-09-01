# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from datetime import datetime
from typing import Any, Protocol, List

import polib
import yaml

from .e_utils import I18NEntry, Occurrence
from .. import utils


class DomainExtractionProtocol(Protocol):
    entries: List[I18NEntry]

    def add_entry(self, src_path: str, msgid: str, line_num: int, comment: str = ''):
        occ = Occurrence(src_path, line_num)
        self.entries.append(I18NEntry(msgid, occ, comment))

    def make_pot(self, package: str, report_address: str, team_address: str, dest_path: str):
        pot = polib.POFile(check_for_duplicates=True)
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
        for e in self.entries:
            e.add_to_pot(pot)
        pot.save(dest_path)

    def render_front_matter(self, path: str, content: str, markup: str) -> Any:
        ...


class DomainExtraction(DomainExtractionProtocol):
    def __init__(self):
        self.entries = []

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

    def render_front_matter(self, path: str, content: str, markup: str):
        fm = yaml.safe_load(content)
        self.i12ize_front_matter(fm, path)
