# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import gettext
from typing import Callable


def gettext_func(domain_name):
    gettext.bindtextdomain(domain_name, 'locale')
    gettext.textdomain(domain_name)
    return gettext.gettext


class L10NResult:
    """Localized content, total number of messages, number of translations.
    If there are no messages, rate will be -1
    """
    def __init__(self, localized, total_count: int, l10n_count: int):
        self.localized = localized
        self.total_count = total_count
        self.l10n_count = l10n_count

    def __str__(self):
        return f'({self.l10n_count}/{self.total_count})'

    @property
    def rate(self):
        return self.l10n_count / self.total_count if self.total_count > 0 else -1

    def sum_rate_with(self, other: 'L10NResult'):
        l10n_count = self.l10n_count + other.l10n_count
        total_count = self.total_count + other.total_count
        return l10n_count / total_count if total_count > 0 else -1


L10NFunc = Callable[[str], str]
