import json

from globals import *
from publication import make_publication_section
from resume import make_resume_main
from section import make_resume_section
from skill import make_skill_section


def main():
    with open('../profile.json') as f:
        profile = json.load(f)

    has_publications = make_publication_section(profile[PUBLICATIONS])
    make_skill_section(profile[SKILLS], profile[LANGUAGES])

    for section in RESUME_SECTIONS:
        make_resume_section(profile, section)

    make_resume_main(profile, has_publications)


if __name__ == '__main__':
    main()
