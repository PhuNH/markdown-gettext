# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import gettext

import yaml
from mdit_py_i18n import utils
from mdit_py_i18n.utils import L10NFunc, L10NResult


def gettext_func(domain_name):
    gettext.bindtextdomain(domain_name, 'locale')
    gettext.textdomain(domain_name)
    return gettext.gettext


class DomainGeneration:
    """
    Implements `DomainGenerationProtocol`
    """
    def __init__(self, l10n_func: L10NFunc):
        self.l10n_func = l10n_func

    def localize_front_matter(self, o) -> L10NResult:
        """Localize an object in front matter.
        :param o: the object being processed
        :return: an `L10NResult`. Translations are made in-place.
        """
        total_count, l10n_count = 0, 0
        if isinstance(o, str) and o and not utils.SPACES_PATTERN.fullmatch(o):
            localized_o = self.l10n_func(o)
            # in front matters only count translations that are different from source messages
            l10n_count = 1 if o != localized_o else 0
            return L10NResult(localized_o, 1, l10n_count)
        if isinstance(o, list) or isinstance(o, dict):
            for key, value in (enumerate(o) if isinstance(o, list) else o.items()):
                item_result = self.localize_front_matter(value)
                total_count += item_result.total_count
                l10n_count += item_result.l10n_count
                o[key] = item_result.localized
            return L10NResult(o, total_count, l10n_count)
        return L10NResult(o, total_count, l10n_count)

    def render_front_matter(self, content: str, markup: str) -> L10NResult:
        fm = yaml.safe_load(content)
        fm_result = self.localize_front_matter(fm)
        rendered_localized_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
        fm_result.localized = f'{markup}\n{rendered_localized_fm}\n{markup}\n'
        return fm_result
