PACKAGE_NAME = 'linkedrw'
LATEX_INDENT = '  '
HTML_INDENT = '    '
CREDENTIALS_FILE = f'~/.{PACKAGE_NAME}/credentials.json'

CHROME = 'chrome'
FIREFOX = 'firefox'
SAFARI = 'safari'
OPERA = 'opera'
DRIVERS = [CHROME, FIREFOX, SAFARI, OPERA]

NAME = 'name'
POSITION = 'position'
CONTACT = 'contact'
SUMMARY = 'about'
EXPERIENCE = 'experience'
EDUCATION = 'education'
VOLUNTEERING = 'volunteering'
SKILLS = 'skills'
PROJECTS = 'projects'
PUBLICATIONS = 'publications'
HONORS = 'honors'
LANGUAGES = 'languages'

ADDRESS = 'address'
MOBILE = 'mobile'
EMAIL = 'email'
HOMEPAGE = 'homepage'
GITHUB = 'github'
LINKEDIN = 'linkedin'
GITLAB = 'gitlab'
STACKOVERFLOW = 'stack-overflow'
TWITTER = 'twitter'
SKYPE = 'skype'
REDDIT = 'reddit'
MEDIUM = 'medium'
GOOGLE_SCHOLAR = 'googlescholar'

DATES = 'dates'
LOCATION = 'location'
DESCRIPTION = 'description'
DEGREE = 'degree'
TITLE = 'title'
ENTRIES = 'entries'
DATE = 'date'
LINK = 'link'
PUBLISHER = 'publisher'
ISSUER = 'issuer'

RESUME_TEMPLATE = 'templates/resume_template.tex'
PERSONAL_INFO = [NAME, POSITION, ADDRESS, MOBILE, EMAIL, HOMEPAGE, GITHUB, LINKEDIN, GITLAB, STACKOVERFLOW, TWITTER,
                 SKYPE, REDDIT, MEDIUM, GOOGLE_SCHOLAR]
RESUME_CONTENT = [EXPERIENCE, EDUCATION, PUBLICATIONS, HONORS, PROJECTS, VOLUNTEERING, SKILLS]
RESUME_SECTIONS = [EXPERIENCE, EDUCATION, HONORS, PROJECTS, VOLUNTEERING]
SECTION_ITEMS = {
    EDUCATION: [DEGREE, NAME, LOCATION, DATES, DESCRIPTION],
    EXPERIENCE: [TITLE, NAME, LOCATION, DATES, DESCRIPTION],
    HONORS: [TITLE, ISSUER, LOCATION, DATE],
    PROJECTS: ['', NAME, '', DATES, DESCRIPTION],
    VOLUNTEERING: [TITLE, NAME, LOCATION, DATES, DESCRIPTION]
}

LATEX_CHARS = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '\n': '\\newline%\n',
    '-': r'{-}',
    '\xA0': '~',  # Non-breaking space
    '[': r'{[}',
    ']': r'{]}',
}

PORTFOLIO_TEMPLATE = 'templates/index_template.html'
PORTFOLIO_SECTIONS = [SUMMARY, EXPERIENCE, EDUCATION, PROJECTS, SKILLS, CONTACT]
CONTACTS = [GITHUB, LINKEDIN, GITLAB, STACKOVERFLOW, TWITTER, REDDIT, MEDIUM]
