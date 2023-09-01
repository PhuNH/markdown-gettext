# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import os
import subprocess
from typing import Tuple

from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from .g_domain import DomainGeneration
from .g_utils import L10NResult, gettext_func
from .renderer_l10n import RendererMarkdownL10N


def compile_po(lang: str, po_path: str):
    target_dir = f'locale/{lang}/LC_MESSAGES'
    os.makedirs(target_dir, exist_ok=True)
    po_basename = os.path.basename(po_path)
    mo_path = f'{target_dir}/{po_basename[:-2]}mo'
    command = f'msgfmt {po_path} -o {mo_path}'
    subprocess.run(command, shell=True, check=True)


def generate(args):
    lang = args.lang
    po_path = args.po

    compile_po(lang, po_path)
    os.environ['LANGUAGE'] = lang

    domain_name = os.path.splitext(os.path.basename(po_path))[0]
    l10n_func = gettext_func(domain_name)

    mdi = MarkdownIt(renderer_cls=RendererMarkdownL10N).use(front_matter_plugin)\
        .enable('table').use(deflist_plugin)
    domain_g = DomainGeneration(l10n_func)

    def render_content_file(src_path: str) -> Tuple[L10NResult, L10NResult]:
        with open(src_path) as f_content:
            env = {
                'domain_generation': domain_g
            }
            return mdi.render(f_content.read(), env)

    def write_content_file(fm: str, content: str, target_path: str):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w+') as f_target:
            f_target.write(fm)
            f_target.write(content)

    fm_result, content_result = render_content_file(args.in_md)
    write_content_file(fm_result.localized, content_result.localized, args.out_md)
