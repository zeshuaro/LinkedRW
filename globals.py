TIMEOUT = 10
INDENT = '  '

NAME = 'name'
POSITION = 'position'
CONTACT = 'contact'
SUMMARY = 'summary'
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
STACKOVERFLOW = 'stackoverflow'
TWITTER = 'twitter'
SKYPE = 'skype'
REDDIT = 'reddit'
MEDIUM = 'medium'
GOOGLE_SCHOLAR = 'googlescholar'

DATES = 'dates'
LOCATION = 'location'
DESCRIPTION = 'description'
SCHOOL = 'school'
DEGREE = 'degree'
COMPANY = 'company'
TITLE = 'title'
ENTRIES = 'entries'
ORGANISATION = 'organisation'
DATE = 'date'
LINK = 'link'
PUBLISHER = 'publisher'
ISSUER = 'issuer'

PERSONAL_INFO = [NAME, POSITION, ADDRESS, MOBILE, EMAIL, HOMEPAGE, GITHUB, LINKEDIN, GITLAB, STACKOVERFLOW, TWITTER,
                 SKYPE, REDDIT, MEDIUM, GOOGLE_SCHOLAR]
RESUME_CONTENT = [EDUCATION, EXPERIENCE, HONORS, PROJECTS, VOLUNTEERING, SKILLS]

SECTION_ITEMS = {
    EDUCATION: [DEGREE, SCHOOL, LOCATION, DATES, DESCRIPTION],
    EXPERIENCE: [TITLE, COMPANY, LOCATION, DATES, DESCRIPTION],
    HONORS: [TITLE, ISSUER, LOCATION, DATE],
    PROJECTS: ['', NAME, '', DATES, DESCRIPTION],
    VOLUNTEERING: [TITLE, ORGANISATION, LOCATION, DATES, DESCRIPTION]
}
