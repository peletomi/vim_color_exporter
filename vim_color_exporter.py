#! env python2.7

import re
import os
import argparse
import tempfile

from jinja2 import Environment, PackageLoader

HI_RES = re.compile('^(\w+)')

GUI_RES = [
        re.compile('guifg\s*=\s*(#[\da-f]+|none)', re.IGNORECASE),
        re.compile('guibg\s*=\s*(#[\da-f]+|none)', re.IGNORECASE),
        re.compile('gui\s*=\s*(\S+)', re.IGNORECASE)
]

COLOR_RE = re.compile('[a-zA-Z\d]*')


def get_re_val(line, regexp):
    m = regexp.search(line)
    if m:
        v = m.group(1).lower()
        if v == 'none':
            return ''
        else:
            return v.replace('#', '')
    else:
        return ''


def get_colors(color_scheme):
    colors = {
            'normal':       ['e2e2e5', '202020', None],
            'cursorcolumn': [None,     '2d2d2d', None],
            'cursorline':   [None,     '2d2d2d', None],
            'nontext':      ['808080', '303030', None],
            'linenr':       ['808080', '000000', None],
            'colorcolumn':  ['808080', None,     None],
            'comment':      ['808080', None,     None],
            'visual':       ['faf4c6', '3c414c',     None],
    }

    # Read the highlights from vim directly as some color schemes use functions to
    # set the colors. The current settings are re-directed into a temp file and
    # then read back.
    (f_script, path_script) = tempfile.mkstemp()
    (f_color, path_color) = tempfile.mkstemp()

    script = """
colorscheme %s
redir! > %s
hi
redir END
quit""" % (color_scheme, path_color)

    with open(path_script, 'w') as f:
        f.write(script)

    os.system('vim -S %s' % path_script)

    with open(path_color, 'r') as f:
        for line in f:
            name = get_re_val(line, HI_RES)
            if name:
                values = []
                for regexp in GUI_RES:
                    color_value = get_re_val(line, regexp)
                    if not COLOR_RE.search(color_value):
                        raise Exception('not allowed color format [%s]'  % color_value)
                    values.append(color_value)
                colors[name] = values

    os.remove(path_script)
    os.remove(path_color)

    return colors

def fill_idea_template(colors, color_schema_name):
    env = Environment(loader=PackageLoader('__main__', '.'))
    template = env.get_template('idea.xml')
    return template.render(colors, name = color_schema_name)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('color_scheme', metavar='C', help='vim color scheme to process')
    parser.add_argument('-icd', '--idea-config-dir', help='config directory for IntelliJ IDEA')

    args = parser.parse_args()

    name = args.color_scheme
    colors = get_colors(name)

    if args.idea_config_dir:
        idea_color_file = os.path.join(args.idea_config_dir, 'colors', name + '.xml')
        icd_config = fill_idea_template(colors, name).replace(' value=""', '')
        with open(idea_color_file, 'w') as f:
            f.write(icd_config)

main()
