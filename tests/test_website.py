import filecmp
import json
import os
import tempfile

from linkedrw.linkedw.website import make_website_files

WEBSITE_DIR = 'website'
PROFILE_FILE = 'profile.json'


def test_make_resume_files_full():
    with open(PROFILE_FILE) as f:
        profile = json.load(f)

    check_outputs(profile, 'full')


def test_make_resume_files_empty():
    check_outputs({}, 'empty')


def check_outputs(profile, files_dir):
    with tempfile.TemporaryDirectory() as dirname:
        make_website_files(profile, dirname)
        for filename in os.listdir(os.path.join(WEBSITE_DIR, files_dir)):
            assert filecmp.cmp(
                os.path.join(dirname, WEBSITE_DIR, filename), os.path.join(WEBSITE_DIR, files_dir, filename),
                shallow=False) is True
