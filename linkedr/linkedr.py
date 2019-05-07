import json
import re

from habanero import Crossref, cn
from urllib.parse import urlparse

from globals import *


def main():
    with open('../profile.json') as f:
        profile = json.load(f)

    has_publications = make_publication_section(profile)
    make_resume_main(profile, has_publications)

    for section in RESUME_SECTIONS:
        make_resume_section(profile, section)


def make_publication_section(profile):
    if profile[PUBLICATIONS]:
        references = make_references(profile[PUBLICATIONS])
        lines = [f'\\cvsection{{{PUBLICATIONS.title()}}}\n', '\\begin{refsection}']

        for reference in references:
            lines.append(f'{INDENT}\\nocite{{{reference}}}')

        lines.append(f'{INDENT}\\printbibligraphy[heading=none]')
        lines.append('\\end{refsection}')

        with open(f'{PUBLICATIONS}.tex', 'w') as f:
            f.write('\n'.join(lines))

        return True

    return False


def make_references(publications):
    cr = Crossref()
    lines = []
    references = []

    for i, publication in enumerate(publications):
        print(f'Querying and formatting {i + 1} out of {len(publications)} publications...')
        link = publication[LINK]

        if link and 'doi.org' in link:
            doi = urlparse(link).path.strip('/')
        else:
            title = publication[TITLE]
            results = cr.works(query_title=title, limit=1)

            if results['message']['total-results'] == 0 or \
                    results['message']['items'][0]['title'][0].lower() != title.lower():
                print(f'Could not find the doi for "{title}"')

                continue

            doi = results['message']['items'][0]['DOI']

        reference = cn.content_negotiation(doi)
        lines.append(reference)
        references.append(re.sub('^@.*\{', '', reference.split('\n')[0]).strip(','))

    with open('references.bib', 'w') as f:
        f.write('\n\n'.join(lines))

    return references


def make_resume_main(profile, has_publications):
    lines = []
    with open('resume_template.tex') as f:
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

    with open('resume.tex', 'w') as f:
        f.write('\n'.join(lines))


def make_personal_info(profile):
    lines = []
    for info_type in PERSONAL_INFO:
        if info_type in (NAME, POSITION):
            value = profile[info_type]
        else:
            value = profile['contact'][info_type]

        line = f'\\{info_type}'
        if value:
            if info_type == NAME:
                names = value.split()
                line += f'{{{names[0]}}}{{{names[-1]}}}'
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
    lines = []
    for section in RESUME_CONTENT:
        if profile[section]:
            lines.append(f'\\input{{{section}.tex}}')

    return lines


def make_resume_section(profile, section):
    title = 'Honors \\& Awards' if section == HONORS else section.title()
    lines = [f'\\cvsection{{{title}}}\n', '\\begin{cventries}']

    if section in (EDUCATION, EXPERIENCE, VOLUNTEERING):
        lines += make_resume_section_grouped(profile, section)
    else:
        lines += make_resume_section_ungrouped(profile, section)

    lines.append('\\end{cventries}')
    with open(f'{section}.tex', 'w') as f:
        f.write('\n'.join(lines))


def make_resume_section_grouped(profile, section):
    lines = []
    for entry in profile[section]:
        lines.append(f'{INDENT}\\cventry')
        name = entry[NAME]

        for i, item in enumerate(entry[ENTRIES]):
            for key in SECTION_ITEMS[section]:
                if key == NAME and i == 0:
                    lines.append(f'{INDENT * 2}{{{name}}} % {NAME}')
                elif key == DESCRIPTION:
                    if item[key]:
                        lines.append(f'{INDENT * 2}{{')
                        lines.append(f'{INDENT * 3}\\begin{{cvitems}}')

                        for description in item[key].split('\n'):
                            description = description.strip('-').strip()
                            lines.append(f'{INDENT * 4}\\item{{{description}}}')

                        lines.append(f'{INDENT * 3}\\end{{cvitems}}')
                        lines.append(f'{INDENT * 2}}}\n')
                    else:
                        lines.append(f'{INDENT * 2}{{}} % {key}\n')
                elif key and key != NAME:
                    lines.append(f'{INDENT * 2}{{{item[key]}}} % {key}')
                else:
                    lines.append(f'{INDENT * 2}{{}}')

    return lines


def make_resume_section_ungrouped(profile, section):
    lines = []
    for entry in profile[section]:
        lines.append(f'{INDENT}\\cventry')
        for key in SECTION_ITEMS[section]:
            if key == DESCRIPTION:
                if entry[key]:
                    lines.append(f'{INDENT * 2}{{')
                    lines.append(f'{INDENT * 3}\\begin{{cvitems}}')

                    for description in entry[key].split('\n'):
                        description = description.strip('-').strip()
                        lines.append(f'{INDENT * 4}\\item{{{description}}}')

                    lines.append(f'{INDENT * 3}\\end{{cvitems}}')
                    lines.append(f'{INDENT * 2}}}\n')
                else:
                    lines.append(f'{INDENT * 2}{{}} % {key}\n')
            elif key:
                lines.append(f'{INDENT * 2}{{{entry[key]}}} % {key}')
            else:
                lines.append(f'{INDENT * 2}{{}}')

    return lines


if __name__ == '__main__':
    main()
