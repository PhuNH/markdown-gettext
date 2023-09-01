# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from dataclasses import dataclass

import polib


@dataclass
class Occurrence:
    src_path: str
    line_num: int

    # this is used with tuple()
    def __iter__(self):
        for key in self.__dict__:
            # polib requires an int for line number, but number 0 passed to it would be lost, so we use string
            yield str(self.__getattribute__(key))


@dataclass
class I18NEntry:
    msgid: str
    occurrence: Occurrence
    comment: str = ''

    def to_poentry(self) -> polib.POEntry:
        return polib.POEntry(msgid=self.msgid,
                             msgstr='',
                             occurrences=[tuple(self.occurrence)],
                             comment=self.comment)

    def add_to_pot(self, pot: polib.POFile):
        if self.msgid:
            if old_entry := pot.find(self.msgid):
                old_entry.occurrences.append(tuple(self.occurrence))
            else:
                try:
                    pot.append(self.to_poentry())
                except ValueError:
                    pass
