import os
import tempfile

from linkedrw.linkedr.skill import make_skill_section, make_skill_subsection
from linkedrw.constants import SKILLS

PROG_LANGS = ['Python', 'Javascript', 'C++']
TECHS = ['AWS', 'Azure', 'GCP']
LANGS = ['English', 'Spanish', 'French']


def test_make_skill_section_empty():
    with tempfile.TemporaryDirectory() as dirname:
        make_skill_section([], [], dirname)
        assert os.path.exists(os.path.join(dirname, f'{SKILLS}.tex')) is False


def test_make_skill_section_prog_langs():
    check_skill_section('Programming', prog_langs=PROG_LANGS)


def test_make_skill_section_techs():
    check_skill_section('Technologies', techs=TECHS)


def test_make_skill_section_langs():
    check_skill_section('Languages', langs=LANGS)


def test_make_skill_section_all():
    check_skill_section('All', PROG_LANGS, TECHS, LANGS)


def check_skill_section(skills_type, prog_langs=None, techs=None, langs=None):
    __tracebackhide__ = True
    skills = None

    if skills_type == 'All':
        skills = prog_langs + techs
    elif prog_langs is not None:
        skills = prog_langs
    elif techs is not None:
        skills = techs

    if skills is None:
        skills = []

    with tempfile.TemporaryDirectory() as dirname:
        make_skill_section(skills, langs, dirname)
        with open(os.path.join(dirname, f'{SKILLS}.tex')) as f:
            for line in f:
                if '\\cvskill' in line:
                    header = next(f).strip().strip('{}')
                    skills_list = next(f).strip().strip('{}').split(', ')

                    if skills_type != 'All':
                        assert header == skills_type

                    if header == 'Programming':
                        assert skills_list == prog_langs
                    elif header == 'Technologies':
                        assert skills_list == techs
                    elif header == 'Languages':
                        assert skills_list == langs
