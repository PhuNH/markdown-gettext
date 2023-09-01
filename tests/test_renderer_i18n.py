# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import importlib.resources as pkg_resources
import unittest

from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from markdown_gettext.extraction.e_domain import DomainExtraction
from markdown_gettext.extraction.renderer_i18n import RendererMarkdownI18N


class RendererMarkdownI18NTestCase(unittest.TestCase):
    mdi = MarkdownIt(renderer_cls=RendererMarkdownI18N).use(front_matter_plugin)\
        .enable('table').use(deflist_plugin)

    def test_renderer(self):
        path = 'renderer.md'
        domain_e = DomainExtraction()
        with pkg_resources.open_text('tests.resources', path) as f_obj:
            env = {
                'path': path,
                'domain_extraction': domain_e
            }
            tokens = self.mdi.parse(f_obj.read(), env)
        self.mdi.renderer.render(tokens, self.mdi.options, env)
        self.assertEqual(19, len(domain_e.entries))


if __name__ == '__main__':
    unittest.main()
