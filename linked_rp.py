import json
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 10


def main():
    with open('config.json') as f:
        credentials = json.load(f)

    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/login/')

    # Login to LinkedIn
    driver.find_element_by_id('username').send_keys(credentials['email'])
    driver.find_element_by_id('password').send_keys(credentials['password'])
    driver.find_element_by_class_name('login__form_action_container').submit()

    # Navigate to profile page
    driver.find_element_by_xpath("//a[@data-control-name='identity_welcome_message']").click()
    background = WebDriverWait(driver, TIMEOUT).until(ec.presence_of_element_located((By.ID, 'oc-background-section')))

    profile = {
        'summary': get_summary(driver),
        'experience': get_experience(driver, background),
        'education': get_education(background),
        'volunteering': get_volunteering(background),
        'skills': get_skills(driver),
        'projects': get_projects(driver),
        'publications': get_publications(driver),
        'languages': get_languages(driver)
    }

    with open('profile.json', 'w') as f:
        json.dump(profile, f, indent=4)

    driver.quit()


def get_summary(driver):
    # Check if summary section exists
    try:
        driver.find_element_by_css_selector(
            '.pv-top-card-section__summary.pv-top-card-section__summary--with-content.mt4.ember-view')
    except NoSuchElementException:
        return ''

    # Check if there is a show more button
    try:
        driver.find_element_by_class_name('pv-top-card-section__summary-toggle-button-icon').click()
    except NoSuchElementException:
        pass

    return driver.find_element_by_css_selector('.pv-top-card-section__summary-text.text-align-left.mt4.ember-view').text


def get_experience(driver, background):
    # Load experience section
    driver.execute_script("arguments[0].scrollIntoView(true);", background)
    time.sleep(1)

    # Locate individual experiences
    section = background.find_element_by_id('experience-section')
    divs = section.find_elements_by_css_selector(
        '.pv-entity__position-group-pager.pv-profile-section__list-item.ember-view')
    exps = []

    for div in divs:
        # Check if it is a single role in a company or multiple roles in a company
        try:
            summary = div.find_element_by_css_selector(
                '.pv-entity__summary-info.pv-entity__summary-info--background-section')
            exps.append(get_single_role(div, summary))
        except NoSuchElementException:
            summary = div.find_element_by_class_name('pv-entity__company-summary-info-v2')
            exps.append(get_multiple_roles(div, summary))

    return exps


def get_single_role(div, summary):
    title = summary.find_element_by_css_selector('.t-16.t-black.t-bold').text
    company = summary.find_element_by_class_name('pv-entity__secondary-title').text
    dates = get_span_text(summary, '.pv-entity__date-range.t-14.t-black--light.t-normal')
    location = get_optional_text(summary, '.pv-entity__location.t-14.t-black--light.t-normal.block')
    description = get_description(div, '.pv-entity__description.t-14.t-black.t-normal.ember-view')

    results = {
        'company': company,
        'roles': [{
            'title': title,
            'dates': dates,
            'location': location,
            'description': description
        }]
    }

    return results


def get_multiple_roles(div, summary):
    company = get_span_text(summary, '.t-16.t-black.t-bold')

    # Show all roles
    try:
        div.find_element_by_class_name('pv-profile-section__toggle-detail-icon').click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    roles = []
    for role_section in div.find_elements_by_class_name('pv-entity__position-group-role-item'):
        title = get_span_text(role_section, '.t-14.t-black.t-bold')
        dates = get_span_text(role_section, '.pv-entity__date-range.t-14.t-black.t-normal')
        location = get_optional_text(role_section, '.pv-entity__location.t-14.t-black--light.t-normal.block')
        description = get_description(role_section, '.pv-entity__description.t-14.t-black.t-normal.ember-view')

        roles.append({
            'title': title,
            'dates': dates,
            'location': location,
            'description': description
        })

    results = {
        'company': company,
        'roles': roles
    }

    return results


def get_education(background):
    section = background.find_element_by_id('education-section')
    ul = section.find_element_by_css_selector(
        '.pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more.ember-view')
    edus = []

    for li in ul.find_elements_by_tag_name('li'):
        school = li.find_element_by_css_selector('.pv-entity__school-name.t-16.t-black.t-bold').text
        degree_name = get_span_text(
            li, '.pv-entity__secondary-title.pv-entity__degree-name.pv-entity__secondary-title.t-14.t-black.t-normal')

        # Check for field of study
        try:
            field = get_span_text(
                li,
                '.pv-entity__secondary-title.pv-entity__fos.pv-entity__secondary-title.t-14.t-black--light.t-normal')
            degree = f'{degree_name} - {field}'
        except NoSuchElementException:
            degree = degree_name

        dates = get_optional_text(li, '.pv-entity__dates.t-14.t-black--light.t-normal')
        description = get_description(li, '.pv-entity__description.t-14.t-black--light.t-normal.mt4')

        edus.append({
            'school': school,
            'degree': degree,
            'dates': dates,
            'description': description
        })

    return edus


def get_volunteering(background):
    section = background.find_element_by_css_selector('.pv-profile-section.volunteering-section.ember-view')
    ul = section.find_element_by_css_selector(
        '.pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more.ember-view')
    vols = []

    for li in ul.find_elements_by_tag_name('li'):
        role = li.find_element_by_css_selector('.t-16.t-black.t-bold').text
        organisation = get_span_text(li, '.t-14.t-black.t-normal')
        dates = get_optional_text(
            li, '.pv-entity__date-range.detail-facet.inline-block.t-14.t-black--light.t-normal')
        description = get_description(li, '.pv-entity__description.t-14.t-black--light.t-normal.mt4')

        vols.append({
            'role': role,
            'organisation': organisation,
            'dates': dates,
            'description': description
        })

    return vols


def get_skills(driver):
    section = driver.find_element_by_css_selector(
        '.pv-profile-section.pv-skill-categories-section.artdeco-container-card.ember-view')

    # Show all skills
    try:
        section.find_element_by_class_name('pv-skills-section__chevron-icon').click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # Extract top skills
    skills = []
    for top_skill in section.find_elements_by_css_selector(
            '.pv-skill-category-entity__top-skill.pv-skill-category-entity.pb3.pt4.pv-skill-endorsedSkill-entity.'
            'relative.ember-view'):
        skill = top_skill.find_element_by_css_selector('.pv-skill-category-entity__name-text.t-16.t-black.t-bold').text
        skills.append(skill)

    # Locate Tools & Technologies section
    target_div = None
    for div in section.find_elements_by_css_selector(
            '.pv-skill-category-list.pv-profile-section__section-info.mb6.ember-view'):
        header = div.find_element_by_tag_name('h3')
        if header.text.lower() == 'tools & technologies':
            target_div = div
            break

    # Extract the rest of the skills
    if target_div is not None:
        for li in target_div.find_elements_by_tag_name('li'):
            skills.append(li.text)

    return skills


def get_projects(driver):
    # Locate and expand projects section
    section = driver.find_element_by_css_selector(
        '.accordion-panel.pv-profile-section.pv-accomplishments-block.projects.ember-view')
    section.find_element_by_xpath("//button[@aria-label='Expand projects section']").click()
    section = driver.find_element_by_css_selector(
        '.accordion-panel.pv-profile-section.pv-accomplishments-block.projects.pv-accomplishments-block--expanded.'
        'ember-view')

    # Show all projects
    try:
        section.find_element_by_xpath("//button[@aria-controls='projects-accomplishment-list']").click()
        ul = section.find_element_by_css_selector(
            '.pv-accomplishments-block__list.pv-accomplishments-block__list--has-more')
    except NoSuchElementException:
        ul = section.find_element_by_class_name('pv-accomplishments-block__list ')

    projects = []
    for li in ul.find_elements_by_tag_name('li'):
        name = li.find_element_by_class_name('pv-accomplishment-entity__title').text.replace('Project name', '').strip()
        dates = get_optional_text(li, '.pv-accomplishment-entity__date.pv-accomplishment-entity__subtitle',
                                  is_span=False)
        description = get_description(li, '.pv-accomplishment-entity__description.t-14.t-black--light.t-normal')
        link = get_accomplishment_link(li)

        projects.append({
            'name': name,
            'dates': dates,
            'description': description,
            'link': link
        })

    return projects


def get_publications(driver):
    # Locate and expand publications section
    section = driver.find_element_by_css_selector(
        '.accordion-panel.pv-profile-section.pv-accomplishments-block.publications.ember-view')
    section.find_element_by_xpath("//button[@aria-label='Expand publications section']").click()
    section = driver.find_element_by_css_selector(
        '.accordion-panel.pv-profile-section.pv-accomplishments-block.publications.pv-accomplishments-block--expanded.'
        'ember-view')

    # Show all publications
    try:
        section.find_element_by_xpath("//button[@aria-controls='publications-accomplishment-list']").click()
        ul = section.find_element_by_css_selector(
            '.pv-accomplishments-block__list.pv-accomplishments-block__list--has-more')
    except NoSuchElementException:
        ul = section.find_element_by_class_name('pv-accomplishments-block__list ')

    projects = []
    for li in ul.find_elements_by_tag_name('li'):
        title = li.find_element_by_class_name('pv-accomplishment-entity__title').text.\
            replace('publication title', '').strip()
        date = get_optional_text_replace(li, 'pv-accomplishment-entity__date', 'publication date')
        publisher = get_optional_text_replace(li, 'pv-accomplishment-entity__publisher', 'publication description')
        link = get_accomplishment_link(li)

        projects.append({
            'title': title,
            'date': date,
            'publisher': publisher,
            'link': link
        })

    return projects


def get_languages(driver):
    section = driver.find_element_by_css_selector(
        '.accordion-panel.pv-profile-section.pv-accomplishments-block.languages.ember-view')
    languages = [x.text for x in section.find_elements_by_tag_name('li')]

    return languages


def get_span_text(element, name):
    return element.find_element_by_css_selector(name).find_elements_by_tag_name('span')[1].text


def get_optional_text(element, name, is_span=True):
    text = ''
    try:
        if is_span:
            text = get_span_text(element, name)
        else:
            text = element.find_element_by_css_selector(name).text
    except NoSuchElementException:
        pass

    return text.replace('–', '-')


def get_optional_text_replace(element, name, text):
    try:
        return element.find_element_by_class_name(name).text.replace(text, '').strip()
    except NoSuchElementException:
        return ''


def get_description(element, name):
    try:
        section = element.find_element_by_css_selector(name)
        btn_section = section.find_elements_by_class_name('lt-line-clamp__ellipsis')

        # Check if there is a more button
        if not btn_section or 'lt-line-clamp__ellipsis--dummy' in btn_section[0].get_attribute('class'):
            description = section.text
        else:
            btn_section[0].find_element_by_class_name('lt-line-clamp__more').click()
            description = section.find_element_by_class_name('lt-line-clamp__raw-line').text
    except NoSuchElementException:
        description = ''

    return description


def get_accomplishment_link(element):
    try:
        return element.find_element_by_class_name('pv-accomplishment-entity__external-source').get_attribute('href')
    except NoSuchElementException:
        return ''


if __name__ == '__main__':
    main()
