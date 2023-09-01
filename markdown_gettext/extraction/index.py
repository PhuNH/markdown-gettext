# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import os

from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from .e_domain import DomainExtraction
from .renderer_i18n import RendererMarkdownI18N


def extract(args):
    md_path = args.md
    mdi = MarkdownIt(renderer_cls=RendererMarkdownI18N).use(front_matter_plugin)\
        .enable('table').use(deflist_plugin)
    domain_e = DomainExtraction()
    with open(md_path) as f_md:
        env = {
            'path': md_path,
            'domain_extraction': domain_e
        }
        mdi.render(f_md.read(), env)
    package = args.package or md_path
    target = args.pot
    os.makedirs(os.path.dirname(target), exist_ok=True)
    domain_e.make_pot(package, args.report_addr, args.team_addr, target)
