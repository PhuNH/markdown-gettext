# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

from argparse import ArgumentParser, RawTextHelpFormatter

from .extraction import extract
from .generation import generate


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
