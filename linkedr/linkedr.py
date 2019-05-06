import json

from urllib.parse import urlparse

from globals import *


def main():
    with open('../profile.json') as f:
        profile = json.load(f)

    resume = []
    with open('resume_template.tex') as f:
        for line in f:
            line = line.strip()
            if 'personal-info-here' in line:
                resume += make_personal_info(profile)
            elif 'resume-content-here' in line:
                resume += make_resume_content(profile)
            else:
                if line.startswith('\\makecvfooter'):
                    line += f'{{\\today}}{{{profile["name"]}~~~·~~~Resume}}{{\\thepage}}'

                resume.append(line)

    with open('resume.tex', 'w') as f:
        f.write('\n'.join(resume))

    make_resume_section(profile, EDUCATION)
    make_resume_section(profile, HONORS)
    make_resume_section(profile, PROJECTS)
    make_resume_section(profile, VOLUNTEERING)


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
    title = 'Honors \\& Awards' if section == HONORS else section.capitalize()
    lines = [f'\\cvsection{{{title}}}\n', '\\begin{cventries}']

    for entry in profile[section]:
        lines.append(f'{INDENT}\\cventry')
        for item in SECTION_ITEMS[section]:
            if item == DESCRIPTION:
                if entry[item]:
                    lines.append(f'{INDENT * 2}{{')
                    lines.append(f'{INDENT * 3}\\begin{{cvitems}}')

                    for description in entry[item].split('\n'):
                        description = description.strip('-').strip()
                        lines.append(f'{INDENT * 4}\\item{{{description}}}')

                    lines.append(f'{INDENT * 3}\\end{{cvitems}}')
                    lines.append(f'{INDENT * 2}}}\n')
                else:
                    lines.append(f'{INDENT * 2}{{}} % {item}\n')
            elif item:
                lines.append(f'{INDENT * 2}{{{entry[item]}}} % {item}')
            else:
                lines.append(f'{INDENT * 2}{{}}')

    lines.append('\\end{cventries}')

    with open(f'{section}.tex', 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    main()
