import os
import re
import tempfile

from linkedrw.constants import *
from linkedrw.linkedr.section import make_resume_section


def test_make_resume_section_empty():
    with tempfile.TemporaryDirectory() as dirname:
        make_resume_section({EXPERIENCE: []}, EXPERIENCE, dirname)
        assert os.path.exists(os.path.join(dirname, f'{EXPERIENCE}.tex')) is False


def test_make_resume_section_grouped():
    entry = {
        TITLE: 'title',
        DATES: 'Jan 2019 - Present',
        LOCATION: '',
        DESCRIPTION: ''
    }
    profile = {
        EXPERIENCE: [{NAME: 'name', ENTRIES: [entry]}]
    }

    with tempfile.TemporaryDirectory() as dirname:
        make_resume_section(profile, EXPERIENCE, dirname)
        with open(os.path.join(dirname, f'{EXPERIENCE}.tex')) as f:
            for line in f:
                if '\\cventry' in line:
                    title = get_text(next(f))
                    name = get_text(next(f))
                    location = get_text(next(f))
                    dates = get_text(next(f))

                    assert title == entry[TITLE]
                    assert name == profile[EXPERIENCE][0][NAME]
                    assert location == entry[LOCATION]
                    assert dates == entry[DATES]

                    break


def test_make_resume_section_ungrouped():
    entry = {
        NAME: 'name',
        DATES: 'Jan 2019 - Present',
        DESCRIPTION: 'description',
        LINK: ''
    }
    profile = {
        PROJECTS: [entry]
    }

    with tempfile.TemporaryDirectory() as dirname:
        make_resume_section(profile, PROJECTS, dirname)
        with open(os.path.join(dirname, f'{PROJECTS}.tex')) as f:
            for line in f:
                if '\\cventry' in line:
                    next(f)
                    name = get_text(next(f))
                    next(f)
                    dates = get_text(next(f))

                    assert name == entry[NAME]
                    assert dates == entry[DATES]

                    break


def test_make_resume_section_honors():
    entry = {
        TITLE: 'title',
        ISSUER: 'issuer',
        LOCATION: '',
        DATE: ''
    }
    profile = {
        HONORS: [entry]
    }

    with tempfile.TemporaryDirectory() as dirname:
        make_resume_section(profile, HONORS, dirname)
        with open(os.path.join(dirname, f'{HONORS}.tex')) as f:
            for line in f:
                if '\\cvhonor' in line:
                    title = get_text(next(f))
                    issuer = get_text(next(f))
                    location = get_text(next(f))
                    dates = get_text(next(f))

                    assert title == entry[TITLE]
                    assert issuer == entry[ISSUER]
                    assert location == entry[LOCATION]
                    assert dates == entry[DATE]

                    break


def get_text(line):
    return re.sub(r'[}%].*', '', line.strip().strip('{}')).strip()
