import os
import pkg_resources

from logbook import Logger
from urllib.parse import urlparse

from linkedrw.constants import *
from linkedrw.utils import make_dir, copy_files
from linkedrw.linkedr.publication import make_publication_section
from linkedrw.linkedr.section import make_resume_section
from linkedrw.linkedr.skill import make_skill_section


def make_resume_files(profile, output_dir):
    """
    Generate resume files
    Args:
        profile: the dict of the profile
        output_dir: the output directory

    Returns:
        None
    """
    log = Logger()
    log.notice('Generating resume files...')

    output_dir = os.path.join(output_dir, 'resume')
    make_dir(output_dir)
    copy_files(__name__, 'awesome_cv_files', output_dir)

    has_publications = make_publication_section(profile[PUBLICATIONS], output_dir)
    make_skill_section(profile[SKILLS], profile[LANGUAGES], output_dir)

    for section in RESUME_SECTIONS:
        make_resume_section(profile, section, output_dir)

    make_resume_main(profile, has_publications, output_dir)


def make_resume_main(profile, has_publications, output_dir):
    """
    Generate the main resume file
    Args:
        profile: the dict of the profile
        has_publications: the bool if there are publications
        output_dir: the output directory

    Returns:
        None
    """
    lines = []
    with open(pkg_resources.resource_filename(__name__, RESUME_TEMPLATE)) as f:
        for line in f:
            line = line.strip()
            if 'personal-info-here' in line:
                lines += make_personal_info(profile)
            elif 'resume-content-here' in line:
                lines += make_resume_content(profile)
            elif 'addbibresource' in line and has_publications:
                lines.append(line.lstrip('% '))
            else:
                if line.startswith('\\makecvfooter'):
                    line += f'{{\\today}}{{{profile["name"]}~~~·~~~Resume}}{{\\thepage}}'

                lines.append(line)

    with open(os.path.join(output_dir, 'resume.tex'), 'w') as f:
        f.write('\n'.join(lines))


def make_personal_info(profile):
    """
    Generate lines about the personal info
    Args:
        profile: the dict of the profile

    Returns:
        A list of lines about the personal info
    """
    lines = []
    for info_type in PERSONAL_INFO:
        if info_type in (NAME, POSITION):
            value = profile[info_type]
        else:
            value = profile[CONTACT][info_type]

        line = f'\\{info_type}'
        if value:
            if info_type == NAME:
                names = value.split()
                line += f'{{{names[0]}}}{{{names[1:]}}}'
            elif info_type == STACKOVERFLOW:
                user_id, username = urlparse(value).path.lstrip('/users/').strip('/').split('/')
                line += f'{{{user_id}}}{{{username}}}'
            elif info_type == GOOGLE_SCHOLAR:
                queries = urlparse(value).query.split('&')
                for query in queries:
                    if 'user=' in query:
                        user_id = query.lstrip('user=').strip('/')
                        line += f'{{{user_id}}}{{}}'

                        break
            else:
                url_path = urlparse(value).path
                if info_type in (GITHUB, GITLAB):
                    value = url_path.strip('/')
                elif info_type == LINKEDIN:
                    value = url_path.lstrip('/in/').strip('/')
                elif info_type == TWITTER:
                    user_id = url_path.strip('/')
                    value = f'@{user_id}'
                elif info_type == REDDIT:
                    value = url_path.lstrip('/user/').strip('/')
                elif info_type == MEDIUM:
                    value = url_path.lstrip('/@').strip('/')

                line += f'{{{value}}}'
        else:
            line = f'% {line}{{}}'

        lines.append(line)

    return lines


def make_resume_content(profile):
    """
    Generate lines about additional section
    Args:
        profile: the dict of the profile

    Returns:
        A list of lines about additional section
    """
    lines = []
    for section in RESUME_CONTENT:
        if profile[section]:
            lines.append(f'\\input{{{section}.tex}}')

    return lines
