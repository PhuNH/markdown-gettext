# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import os
import shutil
import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Tuple

from markdown_it import MarkdownIt
from mdit_py_i18n.renderer_i18n import RendererMarkdownI18N
from mdit_py_i18n.renderer_l10n import RendererMarkdownL10N
from mdit_py_i18n.utils import L10NResult
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from .domain_extraction import DomainExtraction
from .domain_generation import DomainGeneration, gettext_func


def main():
    parser = ArgumentParser(description='Markdown i18n with gettext')
    subparsers = parser.add_subparsers(description='extracting Markdown to POT and generating Markdown from PO')

    extract_cmd = subparsers.add_parser('extract',
                                        help='extract messages from a Markdown file to a POT file',
                                        formatter_class=RawTextHelpFormatter)
    extract_cmd.add_argument('md', help='path of the Markdown file to extract messages from')
    extract_cmd.add_argument('pot', help='path of the POT file to create')
    extract_cmd.add_argument('-p', '--package', default='', help='the package name in POT metadata')
    extract_cmd.add_argument('-r', '--report-addr', default='', help='the report address in POT metadata')
    extract_cmd.add_argument('-t', '--team-addr', default='', help='the team address in POT metadata')
    extract_cmd.set_defaults(func=extract)

    generate_cmd = subparsers.add_parser('generate',
                                         help='generate a Markdown file from a source Markdown file and a PO file',
                                         formatter_class=RawTextHelpFormatter)
    generate_cmd.add_argument('in_md', metavar='in-md', help='path of the source Markdown file')
    generate_cmd.add_argument('po', help='path of the PO file containing translations')
    generate_cmd.add_argument('out_md', metavar='out-md', help='path of the Markdown file to create')
    generate_cmd.add_argument('-l', '--lang', default='en', help='language of translations')
    generate_cmd.set_defaults(func=generate)

    args = parser.parse_args()
    args.func(args)


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
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    domain_e.make_pot(package, args.report_addr, args.team_addr, target)


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
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        with open(target_path, 'w+') as f_target:
            f_target.write(fm)
            f_target.write(content)

    fm_result, content_result = render_content_file(args.in_md)
    write_content_file(fm_result.localized, content_result.localized, args.out_md)
    shutil.rmtree('locale')
