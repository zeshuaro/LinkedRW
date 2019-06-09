import os
import pkg_resources
import shlex

from logbook import Logger
from subprocess import Popen, PIPE, TimeoutExpired
from urllib.parse import urlparse

from linkedrw.constants import *
from linkedrw.utils import make_dir, copy_files
from linkedrw.linkedr.publication import make_publication_section
from linkedrw.linkedr.section import make_resume_section
from linkedrw.linkedr.skill import make_skill_section


def make_resume_files(profile, output_dir, timeout):
    """
    Create resume files
    Args:
        profile: the dict of the profile
        output_dir: the output directory
        timeout: the timeout value

    Returns:
        None
    """
    log = Logger()
    log.notice('Creating resume files')

    output_dir = os.path.join(output_dir, 'resume')
    make_dir(output_dir)
    copy_files(__name__.split('.')[0], 'templates/awesome_cv_files', output_dir)

    if PUBLICATIONS in profile:
        has_publications = make_publication_section(profile[PUBLICATIONS], output_dir)
    else:
        has_publications = False

    if SKILLS in profile and LANGUAGES in profile:
        make_skill_section(profile[SKILLS], profile[LANGUAGES], output_dir)

    for section in RESUME_SECTIONS:
        make_resume_section(profile, section, output_dir)

    make_resume_main(profile, has_publications, output_dir)
    compile_resume(output_dir, has_publications, timeout)


def make_resume_main(profile, has_publications, output_dir):
    """
    Create the main resume file
    Args:
        profile: the dict of the profile
        has_publications: the bool if there are publications
        output_dir: the output directory

    Returns:
        None
    """
    lines = []
    with open(pkg_resources.resource_filename(__name__.split('.')[0], RESUME_TEMPLATE)) as f:
        for line in f:
            line = line.strip()
            if 'personal-info-here' in line:
                lines += make_personal_info(profile)
            elif 'resume-content-here' in line:
                lines += make_resume_content(profile)
            elif 'addbibresource' in line and has_publications:
                lines.append(line.lstrip('% '))
            else:
                if line.startswith('\\makecvfooter') and NAME in profile:
                    line += f'{{\\today}}{{{profile[NAME]}~~~·~~~Resume}}{{\\thepage}}'

                lines.append(line)

    with open(os.path.join(output_dir, 'resume.tex'), 'w') as f:
        f.write('\n'.join(lines))


def make_personal_info(profile):
    """
    Create lines about the personal info
    Args:
        profile: the dict of the profile

    Returns:
        A list of lines about the personal info
    """
    lines = []
    for info_type in PERSONAL_INFO:
        if info_type in (NAME, POSITION) and info_type in profile:
            value = profile[info_type]
        elif CONTACT in profile and info_type in profile[CONTACT]:
            value = profile[CONTACT][info_type]
        else:
            value = ''

        line = f'\\{info_type}'
        if value:
            if info_type == NAME:
                names = value.split()
                last_name = ' '.join(names[1:])
                line += f'{{{names[0]}}}{{{last_name}}}'
            elif info_type == STACKOVERFLOW:
                user_id, username = urlparse(value).path.replace('/users/', '').strip('/').split('/')
                line += f'{{{user_id}}}{{{username}}}'
            elif info_type == GOOGLE_SCHOLAR:
                queries = urlparse(value).query.split('&')
                for query in queries:
                    if 'user=' in query:
                        user_id = query.replace('user=', '').strip('/')
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
                    value = url_path.replace('/user/', '').strip('/')
                elif info_type == MEDIUM:
                    value = url_path.lstrip('/@').strip('/')

                line += f'{{{value}}}'
        else:
            line = f'% {line}{{}}'

        lines.append(line)

    return lines


def make_resume_content(profile):
    """
    Create lines about additional section
    Args:
        profile: the dict of the profile

    Returns:
        A list of lines about additional section
    """
    lines = []
    for section in RESUME_CONTENT:
        if section in profile and profile[section]:
            lines.append(f'\\input{{{section}.tex}}')

    return lines


def compile_resume(output_dir, has_pubs, timeout):
    """
    Compile resume files
    Args:
        output_dir: the resume output directory
        has_pubs: the boolean whether there is a publication section
        timeout: the timeout value

    Returns:
        None
    """
    log = Logger()
    log.notice('Compiling resume files')
    curr_dir = os.getcwd()
    os.chdir(output_dir)

    if run_cmd('xelatex resume.tex', timeout):
        if has_pubs and (not run_cmd('biber resume', timeout) or not run_cmd('xelatex resume.tex', timeout)):
            log.warn('Failed to compile resume files, please compile them manually')
    else:
        log.warn('Failed to compile resume files, please compile them manually')

    os.chdir(curr_dir)


def run_cmd(cmd, timeout):
    """
    Run a shell command
    Args:
        cmd: the string of command to run
        timeout: the timeout value

    Returns:
        A boolean whether the command has been successful or not
    """
    success = True
    try:
        proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate(timeout=timeout)

        if proc.returncode != 0 or err:
            success = False
    except (FileNotFoundError, TimeoutExpired):
        success = False

    return success
