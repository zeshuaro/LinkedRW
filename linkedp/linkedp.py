import arrow
import json
import re

from datetime import datetime
from queue import PriorityQueue

from globals import *


def main():
    with open('../profile.json') as f:
        profile = json.load(f)

    lines = []
    comment_line = has_sum = has_exp = has_edu = False

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
                    has_sum = True
                    lines.append(line)
            elif has_sum and 'summary-here' in line:
                lines += make_summary_section(profile[SUMMARY], indent)

            # Experience section
            elif 'id="experience"' in line:
                if not profile[EXPERIENCE]:
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_exp = True
                    lines.append(line)
            elif has_exp and 'experience-here' in line:
                lines += make_experience_section(profile[EXPERIENCE], indent)

            # Education section
            elif 'id="education"' in line:
                if not profile[EDUCATION]:
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_edu = True
                    lines.append(line)
            elif has_edu and 'education-here' in line:
                lines += make_education_section(profile[EDUCATION], indent)

            # Comment out sections
            elif comment_line and any(x in line for x in ['End #about', 'End #experience', 'End #education']):
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


def make_experience_section(exps, indent):
    sorted_exps = sort_entries(exps)
    lines = []

    while sorted_exps:
        exp = sorted_exps.pop()
        lines += [
            f'{indent}<div data-date="{exp[DATES]}">',
            f'{indent}{HTML_INDENT}<h3>{exp[NAME]}</h3>',
            f'{indent}{HTML_INDENT}<h4>{exp[TITLE]}</h4>',
        ]
        lines += get_description(exp[DESCRIPTION], indent)
        lines += [f'{indent}</div>', '']

    return lines


def make_education_section(edus, indent):
    sorted_edus = sort_entries(edus, date_format='YYYY')
    lines = []

    while sorted_edus:
        edu = sorted_edus.pop()
        lines += [
            f'{indent}<div class="education-block">',
            f'{indent}{HTML_INDENT}<h3>{edu[NAME]}</h3>',
            f'{indent}{HTML_INDENT}<span class="education-date">{edu[DATES]}</span>',
            f'{indent}{HTML_INDENT}<h4>{edu[DEGREE]}</h4>'
        ]
        lines += get_description(edu[DESCRIPTION], indent)
        lines += [f'{indent}</div>', '']

    return lines


def sort_entries(entries, date_format='MMM YYYY'):
    sorted_entries = PriorityQueue()
    for exp in entries:
        name = exp[NAME]
        for entry in exp[ENTRIES]:
            entry[NAME] = name
            date = entry[DATES].split(' - ')[-1]

            if date.lower() == 'present':
                arrow_date = arrow.utcnow()
            elif date:
                arrow_date = arrow.get(date, date_format)
            else:
                arrow_date = arrow.get(datetime.min)

            sorted_entries.put((arrow_date, entry))

    all_entries = []
    while not sorted_entries.empty():
        all_entries.append(sorted_entries.get()[1])

    return all_entries


def get_description(descs, indent):
    lines = []
    if descs:
        lines.append(f'{indent}{HTML_INDENT}<ul>')
        for desc in descs.split('\n'):
            desc = desc.strip('-').strip()
            lines.append(f'{indent}{HTML_INDENT * 2}<li>{desc}')

        lines.append(f'{indent}{HTML_INDENT}</ul>')

    return lines


def make_comment_line(line):
    return [f'<!-- {line} -->']


if __name__ == '__main__':
    main()
