import os
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


def test_make_resume_files_contact():
    profile = {
        CONTACT: {
            LINKEDIN: "linkedin-id",
            SKYPE: "skype-id",
            GITHUB: "github-id",
            GITLAB: "gitlab-id",
            STACKOVERFLOW: "/users/stack-id/stack-username",
            TWITTER: "twitter-id",
            REDDIT: "reddit-id",
            MEDIUM: "medium-id",
            GOOGLE_SCHOLAR: "/citations?user=scholar-id"
        }
    }

    count = 0
    with tempfile.TemporaryDirectory() as dirname:
        make_resume_files(profile, dirname, TIMEOUT)
        with open(os.path.join(dirname, 'resume', 'resume.tex')) as f:
            for line in f:
                if '.tex' in line:
                    count += 1