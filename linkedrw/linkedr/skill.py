import os
import pkg_resources

from linkedrw.constants import SKILLS, LATEX_INDENT, PACKAGE_NAME
from linkedrw.utils import escape_latex


def make_skill_section(skills, languages, output_dir):
    """
    Create skill latex files
    Args:
        skills: the list of skills
        languages: the list of languages
        output_dir: the output directory

    Returns:
        None
    """
    if skills or languages:
        lines = [f'\\cvsection{{{SKILLS}}}\n', '\\begin{cvskills}']

        if skills:
            # Get and store a set of programming languages
            prog_languages = set()
            with open(pkg_resources.resource_filename(PACKAGE_NAME, 'utils/prog_languages.txt')) as f:
                for line in f:
                    prog_languages.add(line.strip())

            prog = []
            tech = []

            # Check if skill is a programming language
            for skill in skills:
                if skill.lower() in prog_languages:
                    prog.append(skill)
                else:
                    tech.append(skill)

            lines += make_skill_subsection(prog, 'Programming')
            lines += make_skill_subsection(tech, 'Technologies')

        lines += make_skill_subsection(languages, 'Languages')
        lines.append('\\end{cvskills}')

        with open(os.path.join(output_dir, f'{SKILLS}.tex'), 'w') as f:
            f.write('\n'.join(lines))


def make_skill_subsection(skills, skills_type):
    """
    Create the lines for the skill subsection
    Args:
        skills: the list of skills
        skills_type: the skill type

    Returns:
        A list of lines for the skill subsection
    """
    lines = []
    if skills:
        lines.append(f'{LATEX_INDENT}\\cvskill')
        lines.append(f'{LATEX_INDENT * 2}{{{skills_type}}}')
        lines.append(f'{LATEX_INDENT * 2}{{{escape_latex(", ".join(skills))}}}')

    return lines
