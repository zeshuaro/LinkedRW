import filecmp
import json
import os
import pkg_resources
import tempfile

from linkedrw.constants import PUBLICATIONS, TITLE, DATE, PUBLISHER, LINK
from linkedrw.linkedr.resume import make_resume_files
from linkedrw.linkedr.publication import make_publication_section, make_references

RESUME_DIR = "resume"
PROFILE_FILE = "profile.json"
TIMEOUT = 1


def test_make_resume_files_full():
    with tempfile.TemporaryDirectory() as dirname:
        with open(pkg_resources.resource_filename(__name__, PROFILE_FILE)) as f:
            profile = json.load(f)

        make_resume_files(profile, dirname, TIMEOUT)
        for filename in os.listdir(
            pkg_resources.resource_filename(__name__, RESUME_DIR)
        ):
            assert (
                filecmp.cmp(
                    os.path.join(dirname, RESUME_DIR, filename),
                    pkg_resources.resource_filename(
                        __name__, f"{RESUME_DIR}/{filename}"
                    ),
                    shallow=False,
                )
                is True
            )


def test_make_publication_section_empty():
    with tempfile.TemporaryDirectory() as dirname:
        assert make_publication_section([], dirname) is False
        assert os.path.exists(os.path.join(dirname, f"{PUBLICATIONS}.tex")) is False


def test_make_resume_files_no_pub():
    with tempfile.TemporaryDirectory() as dirname:
        with open(pkg_resources.resource_filename(__name__, PROFILE_FILE)) as f:
            profile = json.load(f)

        del profile[PUBLICATIONS]
        make_resume_files(profile, dirname, TIMEOUT)
        assert (
            os.path.exists(os.path.join(dirname, RESUME_DIR, f"{PUBLICATIONS}.tex"))
            is False
        )


def test_make_references_no_doi():
    pub = {
        TITLE: "A rapid and sensitive method for the quantitation of microgram quantities of protein utilizing the "
        "principle of protein-dye binding",
        DATE: "May 7, 1976",
        PUBLISHER: "Science Direct",
        LINK: "",
    }

    with tempfile.TemporaryDirectory() as dirname:
        assert make_references([pub], dirname) == ["Bradford_1976"]
        with open(os.path.join(dirname, "references.bib")) as f:
            assert f.read() != ""


def test_make_references_not_found():
    pub = {TITLE: "Some random title", DATE: "", PUBLISHER: "", LINK: ""}

    with tempfile.TemporaryDirectory() as dirname:
        assert make_references([pub], dirname) == []
        with open(os.path.join(dirname, "references.bib")) as f:
            assert f.read() == ""
