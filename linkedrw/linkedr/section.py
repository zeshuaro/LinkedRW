import os

from linkedrw.constants import *
from linkedrw.utils import escape_latex


def make_resume_section(profile, section, output_dir):
    """
    Create the latex file for the given section
    Args:
        profile: the dict of the profile
        section: the section to Create
        output_dir: the output directory

    Returns:
        None
    """
    if section in SECTION_ITEMS and section in profile and profile[section]:
        title = 'Honors \\& Awards' if section == HONORS else section.title()
        cv_type = 'cvhonors' if section == HONORS else 'cventries'
        lines = [f'\\cvsection{{{title}}}\n', f'\\begin{{{cv_type}}}']

        if section in (EDUCATION, EXPERIENCE, VOLUNTEERING):
            lines += make_grouped_section(profile, section)
        else:
            lines += make_ungrouped_section(profile, section)

        lines.append(f'\\end{{{cv_type}}}')
        with open(os.path.join(output_dir, f'{section}.tex'), 'w') as f:
            f.write('\n'.join(lines))


def make_grouped_section(profile, section):
    """
    Create the lines for grouped entries
    Args:
        profile: the dict of the profile
        section: the section

    Returns:
        A list of lines for the given section
    """
    lines = []
    for entry in profile[section]:
        name = entry[NAME]
        for i, item in enumerate(entry[ENTRIES]):
            lines.append(f'{LATEX_INDENT}\\cventry')
            for key in SECTION_ITEMS[section]:
                if key == NAME and i == 0:
                    lines.append(f'{LATEX_INDENT * 2}{{{escape_latex(name)}}} % {NAME}')
                elif key == DESCRIPTION:
                    lines += get_descriptions(item)
                elif key and key != NAME:
                    lines.append(f'{LATEX_INDENT * 2}{{{escape_latex(item[key])}}} % {key}')
                else:
                    lines.append(f'{LATEX_INDENT * 2}{{}}')

    return lines


def make_ungrouped_section(profile, section):
    """
    Create the lines for ungrouped entries
    Args:
        profile: the dict of the profile
        section: the section

    Returns:
        A list of lines for the given section
    """
    lines = []
    for entry in profile[section]:
        if section == HONORS:
            lines.append(f'{LATEX_INDENT}\\cvhonor')
        else:
            lines.append(f'{LATEX_INDENT}\\cventry')

        for key in SECTION_ITEMS[section]:
            if key == DESCRIPTION:
                lines += get_descriptions(entry)
            elif key:
                lines.append(f'{LATEX_INDENT * 2}{{{escape_latex(entry[key])}}} % {key}')
            else:
                lines.append(f'{LATEX_INDENT * 2}{{}}')

    return lines


def get_descriptions(item):
    """
    Create the lines for the description
    Args:
        item: the item

    Returns:
        A list of lines for the description
    """
    lines = []
    if item[DESCRIPTION]:
        lines.append(f'{LATEX_INDENT * 2}{{')
        lines.append(f'{LATEX_INDENT * 3}\\begin{{cvitems}}')

        for description in item[DESCRIPTION].split('\n'):
            description = description.strip('-').strip()
            if description:
                description = escape_latex(description)
                lines.append(f'{LATEX_INDENT * 4}\\item{{{description}}}')

        lines.append(f'{LATEX_INDENT * 3}\\end{{cvitems}}')
        lines.append(f'{LATEX_INDENT * 2}}}\n')
    else:
        lines.append(f'{LATEX_INDENT * 2}{{}} % {DESCRIPTION}\n')

    return lines
