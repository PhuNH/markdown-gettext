# SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
# SPDX-License-Identifier: LGPL-2.1-or-later

import re

SPACES_PATTERN = re.compile(r'\s+')
SINGLE_COMMENT_PATTERN = re.compile('(// *)(.*)')
