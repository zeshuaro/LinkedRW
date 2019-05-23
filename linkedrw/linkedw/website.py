import arrow
import os
import pkg_resources
import re
import shutil

from datetime import datetime
from logbook import Logger
from queue import PriorityQueue

from linkedrw.globals import *
from linkedrw.utils import make_dir, copy_files


def make_website_files(profile, output_dir):
    """
    Generate website files
    Args:
        profile: the dict of the profile
        output_dir: the output directory

    Returns:
        None
    """
    log = Logger()
    log.notice('Generate website files...')

    output_dir = os.path.join(output_dir, 'website')
    make_dir(output_dir)
    copy_files(__name__, 'dev_portfolio_files', output_dir)

    lines = []
    comment_line = has_sum = has_exp = has_edu = has_prj = has_skl = has_con = False

    with open(pkg_resources.resource_filename(__name__, PORTFOLIO_TEMPLATE)) as f:
        for line in f:
            line = line.strip('\n')
            indent = re.match(r'\s+', line)

            if indent is not None:
                indent = indent.group()

            if 'section-headers-here' in line:
                for section in PORTFOLIO_SECTIONS:
                    if section == CONTACT or profile[section]:
                        lines += make_section_header(section, indent)
            elif 'name-here' in line:
                lines.append(line.replace('name-here', profile[NAME]))
            elif 'title-here' in line:
                lines.append(line.replace('title-here', profile[POSITION]))
            elif 'copyright-here' in line:
                lines.append(line.replace('copyright-here', f'{arrow.now().year} {profile[NAME]}'))

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

            # Projects section
            elif 'id="projects"' in line:
                if not profile[PROJECTS]:
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_prj = True
                    lines.append(line)
            elif has_prj and 'projects-here' in line:
                lines += make_projects_section(profile[PROJECTS], indent)

            # Skills section
            elif 'id="skills"' in line:
                if not profile[SKILLS]:
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_skl = True
                    lines.append(line)
            elif has_skl and 'skills-here' in line:
                lines += make_skills_section(profile[SKILLS], indent)

            # Contact section
            elif 'email-here' in line:
                lines.append(line.replace('email-here', profile[CONTACT][EMAIL]))
            elif 'col-sm-5 social' in line:
                if all(not profile[CONTACT][x] for x in CONTACTS):
                    comment_line = True
                    lines += make_comment_line(line)
                else:
                    has_con = True
                    lines.append(line)
            elif has_con and 'contact-here' in line:
                lines += make_contact_section(profile[CONTACT], indent)

            # Comment out sections
            elif comment_line and any(x in line for x in ['End #about', 'End #experience', 'End #education']):
                comment_line = False
            elif comment_line:
                lines += make_comment_line(line)

            # No changes to line
            else:
                lines.append(line)

    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write('\n'.join(lines))


def make_section_header(section, indent):
    """
    Generate the lines for the section header
    Args:
        section: the section
        indent: the original indentation

    Returns:
        A list of lines for the section header
    """
    lines = [
        f'{indent}<li>',
        f'{indent}{HTML_INDENT}<a href="#{section}">{section.title()}</a>',
        f'{indent}</li>'
    ]

    return lines


def make_summary_section(summary, indent):
    """
    Generate the summary line
    Args:
        summary: the summary text
        indent: the original indentation

    Returns:
        A string of the summary line
    """
    text = summary.replace('\n', '<br>')
    line = [f'{indent}{text}']

    return line


def make_experience_section(exps, indent):
    """
    Generate the lines of the experience section
    Args:
        exps: the list of experiences
        indent: the original indentation

    Returns:
        A list of lines of the experience section
    """
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
    """
    Generate the lines of the education section
    Args:
        edus: the list of educations
        indent: the original indentation

    Returns:
        A list of lines of the education section
    """
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


def make_projects_section(prjs, indent):
    """
    Generate the lines of the project section
    Args:
        prjs: the list of projects
        indent: the original indentation

    Returns:
        A list of lines of the project section
    """
    lines = []
    for prj in prjs:
        lines += [
            f'{indent}<div class="project shadow-large">',
            f'{indent}{HTML_INDENT}<div class="project no-image">',
            f'{indent}{HTML_INDENT * 2}<div class="project-info">',
            f'{indent}{HTML_INDENT * 3}<h3>{prj[NAME]}</h3>'
        ]

        lines += get_description(prj[DESCRIPTION], indent + HTML_INDENT * 2)
        if prj[LINK]:
            lines.append(f'{indent}{HTML_INDENT * 3}<a href="{prj[LINK]}" target="_blank">View Project</a>')

        lines += [f'{indent}{HTML_INDENT * x}</div>' for x in range(2, -1, -1)] + ['']

    return lines


def make_skills_section(skls, indent):
    """
    Generate the liens of the skill section
    Args:
        skls: the list of skills
        indent: the original indentation

    Returns:
        A list of lines of the skill section
    """
    lines = []
    for skl in skls:
        lines.append(f'{indent}<li>{skl}</li>')

    return lines


def make_contact_section(cons, indent):
    """
    Generate the lines of the contact section
    Args:
        cons: the list of contacts
        indent: the original indentation

    Returns:
        A list of lines of the contact section
    """
    lines = []
    for con in CONTACTS:
        if cons[con]:
            lines += [
                f'{indent}<li>',
                f'{indent}{HTML_INDENT}'
                f'<a href="{cons[con]}" target="_blank"><i class="fa fa-{con}" aria-hidden="true"></i></a>',
                f'{indent}</li>'
            ]

    return lines


def sort_entries(entries, date_format='MMM YYYY'):
    """
    Sort entries by date
    Args:
        entries: the list of entries to be sorted
        date_format: the format of the date in the entries

    Returns:
        A list of sorted entries
    """
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
    """
    Generate the lines of the description
    Args:
        descs: the list of descriptions
        indent: the original indentation

    Returns:
        A list of lines of the description
    """
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
