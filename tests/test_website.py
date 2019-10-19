import filecmp
import json
import os
import pkg_resources
import tempfile

from linkedrw.constants import (
    EDUCATION,
    NAME,
    ENTRIES,
    DEGREE,
    LOCATION,
    DATES,
    DESCRIPTION,
)
from linkedrw.linkedw.website import make_website_files

WEBSITE_DIR = "website"
PROFILE_FILE = "profile.json"


def test_make_resume_files_full():
    with open(pkg_resources.resource_filename(__name__, PROFILE_FILE)) as f:
        profile = json.load(f)

    check_outputs(profile, "full")


def test_make_resume_files_empty():
    check_outputs({}, "empty")


def test_make_resume_files_no_date():
    profile = {
        EDUCATION: [
            {
                NAME: "Name",
                ENTRIES: [
                    {
                        DEGREE: "Degree 1",
                        DATES: "",
                        LOCATION: "Location 1",
                        DESCRIPTION: "Description 1",
                    },
                    {
                        DEGREE: "Degree 2",
                        DATES: "2018 - 2019",
                        LOCATION: "Location 2",
                        DESCRIPTION: "Description 2",
                    },
                ],
            }
        ]
    }
    check_outputs(profile, "no_date")


def check_outputs(profile, files_dir):
    with tempfile.TemporaryDirectory() as dirname:
        make_website_files(profile, dirname)
        for filename in os.listdir(
            pkg_resources.resource_filename(__name__, f"{WEBSITE_DIR}/{files_dir}")
        ):
            assert (
                filecmp.cmp(
                    os.path.join(dirname, WEBSITE_DIR, filename),
                    pkg_resources.resource_filename(
                        __name__, f"{WEBSITE_DIR}/{files_dir}/{filename}"
                    ),
                    shallow=False,
                )
                is True
            )
