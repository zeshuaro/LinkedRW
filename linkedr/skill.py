from globals import SKILLS, INDENT


def make_skill_section(skills, languages):
    if skills or languages:
        lines = [f'\\cvsection{{{SKILLS}}}\n', '\\begin{cvskills}']

        if skills:
            # Get and store a set of programming languages
            prog_languages = set()
            with open('../utils/prog_languages.txt') as f:
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

        with open(f'{SKILLS}.tex', 'w') as f:
            f.write('\n'.join(lines))


def make_skill_subsection(skills, skills_type):
    lines = []
    if skills:
        lines.append(f'{INDENT}\\cvskill')
        lines.append(f'{INDENT * 2}{{{skills_type}}}')
        lines.append(f'{INDENT * 2}{{{", ".join(skills)}}}')

    return lines
