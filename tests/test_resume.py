import os
import re
import tempfile

from linkedrw.constants import *
from linkedrw.linkedr.resume import make_resume_files

TIMEOUT = 10


def test_make_resume_files_empty():
    with tempfile.TemporaryDirectory() as dirname:
        make_resume_files({}, dirname, TIMEOUT)
        assert os.path.exists(os.path.join(dirname, 'resume', 'awesome-cv.cls')) is True
        assert os.path.exists(os.path.join(dirname, 'resume', 'fontawesome.sty')) is True
        assert os.path.exists(os.path.join(dirname, 'resume', 'fonts')) is True

        for section in RESUME_SECTIONS:
            assert os.path.exists(os.path.join(dirname, 'resume', section)) is False


def test_make_resume_files():
    profile = {
        NAME: 'name',
        PUBLICATIONS: [
            {
                TITLE: 'Something',
                DATE: '',
                PUBLISHER: '',
                LINK: ''
            }
        ],
        SKILLS: ['Python'],
        LANGUAGES: ['English']
    }
    sections = {PUBLICATIONS, SKILLS, LANGUAGES}

    with tempfile.TemporaryDirectory() as dirname:
        make_resume_files(profile, dirname, TIMEOUT)
        for section in RESUME_SECTIONS:
            if section in sections:
                assert os.path.exists(os.path.join(dirname, 'resume', section)) is True
            else:
                assert os.path.exists(os.path.join(dirname, 'resume', section)) is False

        count = 0
        with open(os.path.join(dirname, 'resume', 'resume.tex')) as f:
            for line in f:
                if '.tex' in line:
                    count += 1

        assert count == len(sections) - 1


def test_make_resume_files_contacts():
    stack_id = 'stack-id'
    stack_username = 'stack-username'
    scholar_id = 'scholar-id'
    profile = {
        CONTACT: {
            LINKEDIN: 'linkedin-id',
            SKYPE: 'skype-id',
            GITHUB: 'github-id',
            GITLAB: 'gitlab-id',
            STACKOVERFLOW: f'/users/{stack_id}/{stack_username}',
            TWITTER: 'twitter-id',
            REDDIT: 'reddit-id',
            MEDIUM: 'medium-id',
            GOOGLE_SCHOLAR: f'/citations?user={scholar_id}'
        }
    }

    is_contact = False
    contacts = {}

    with tempfile.TemporaryDirectory() as dirname:
        make_resume_files(profile, dirname, TIMEOUT)
        with open(os.path.join(dirname, 'resume', 'resume.tex')) as f:
            for line in f:
                if f'\\{HOMEPAGE}' in line:
                    is_contact = True
                elif is_contact:
                    line = line.strip()
                    key = re.sub(r'{.*', '', line).lstrip('\\')

                    if key in [STACKOVERFLOW, GOOGLE_SCHOLAR]:
                        contact_id = re.sub(r'^.*?{', '', line)
                        contact_id = re.sub(r'}.*', '', contact_id)

                        if key == STACKOVERFLOW:
                            contact_username = re.sub(r'^.*{', '', line).rstrip('}')
                            value = (contact_id, contact_username)
                        else:
                            value = contact_id
                    elif key == TWITTER:
                        value = re.sub(r'^.*{', '', line).rstrip('}').lstrip('@')
                    else:
                        value = re.sub(r'^.*{', '', line).rstrip('}')

                    contacts[key] = value
                    if key == GOOGLE_SCHOLAR:
                        break

    for key in contacts:
        if key == STACKOVERFLOW:
            assert contacts[key][0] == stack_id
            assert contacts[key][1] == stack_username
        elif key == GOOGLE_SCHOLAR:
            assert contacts[key] == scholar_id
        else:
            assert contacts[key] == profile[CONTACT][key]
