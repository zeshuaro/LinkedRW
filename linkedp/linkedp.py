import json
import re

from globals import *


def main():
    with open('../profile.json') as f:
        profile = json.load(f)

    lines = []
    comment_line = has_summary = has_experience = False

    with open(PORTFOLIO_TEMPLATE) as f:
        for line in f:
            line = line.strip('\n')
            indent = re.match(r'\s+', line)

            if indent is not None:
                indent = indent.group()

            if 'section-headers-here' in line:
                for section in PORTFOLIO_SECTIONS:
                    if section == CONTACT or profile[section]:
                        lines += make_section_header(section, indent)

            # About section
            elif 'id="about"' in line:
                if not profile[SUMMARY]:
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_summary = True
            elif has_summary and 'summary-here' in line:
                lines += make_summary_section(profile[SUMMARY], indent)

            # Experience section
            elif 'id="experience"' in line:
                if not profile[EXPERIENCE]:
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_experience = True

            # Comment out sections
            elif comment_line and any(x in line for x in ['End #about', 'End #experience']):
                comment_line = False
            elif comment_line:
                lines += make_comment_line(line)

            # No changes to line
            else:
                lines.append(line)

    with open('index.html', 'w') as f:
        f.write('\n'.join(lines))


def make_section_header(section, indent):
    lines = [
        f'{indent}<li>',
        f'{indent}{HTML_INDENT}<a href="#{section}">{section.title()}</a>',
        f'{indent}</li>'
    ]

    return lines


def make_summary_section(summary, indent):
    text = summary.replace('\n', '<br>')
    line = [f'{indent}{text}']

    return line


def make_comment_line(line):
    return [f'<!-- {line} -->']


if __name__ == '__main__':
    main()
