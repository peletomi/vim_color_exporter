#! env python2.7

import re
import sys
import os
import argparse

from jinja2 import Environment, PackageLoader

HI_RES = re.compile('^\s*hi\s+(\w+)')

GUI_RES = [
        re.compile('guifg\s*=\s*(#[\da-f]+|none)', re.IGNORECASE),
        re.compile('guibg\s*=\s*(#[\da-f]+|none)', re.IGNORECASE),
        re.compile('gui\s*=\s*(\S+)', re.IGNORECASE)
]

def get_re_val(line, regexp):
    m = regexp.search(line)
    if m:
        v = m.group(1).lower()
        if v != 'none':
            return v.replace('#', '')
    else:
        return ''



def get_colors(vim_color_def):
    colors = {}
    with open(vim_color_def, 'r') as f:
        for line in f:
            name = get_re_val(line, HI_RES)
            if name:
                values = []
                for regexp in GUI_RES:
                    values.append(get_re_val(line, regexp))
                colors[name] = values
    return colors

def fill_idea_template(colors, color_schema_name):
    env = Environment(loader=PackageLoader('__main__', '.'))
    template = env.get_template('idea.xml')
    return template.render(colors, name = color_schema_name)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('color_file', metavar='C', help='vim color file to process')
    parser.add_argument('-icd', '--idea-config-dir', help='config directory for IntelliJ IDEA')

    args = parser.parse_args()

    name = os.path.basename(args.color_file).replace('.vim', '')
    colors = get_colors(args.color_file)

    if args.idea_config_dir:
        idea_color_file = os.path.join(args.idea_config_dir, 'colors', name + '.xml')
        icd_config = fill_idea_template(colors, name).replace(' value=""', '')
        with open(idea_color_file, 'w') as f:
            f.write(icd_config)

main()
