from selenium.common.exceptions import NoSuchElementException

from globals import *
from utils import get_optional_text, get_optional_text_replace, get_description, get_accomplishment_link


def get_accomplishment_details(driver, section_type):
    # Check if the section exists
    try:
        section = driver.find_element_by_css_selector(
            f'.accordion-panel.pv-profile-section.pv-accomplishments-block.{section_type}.ember-view')
    except NoSuchElementException:
        return []

    if section_type in (PROJECTS, PUBLICATIONS):
        # Expand the section section
        section.find_element_by_xpath(f"//button[@aria-label='Expand {section_type} section']").click()
        section = driver.find_element_by_css_selector(
            f'.accordion-panel.pv-profile-section.pv-accomplishments-block.{section_type}.'
            f'pv-accomplishments-block--expanded.ember-view')

        if section_type == PROJECTS:
            return get_projects(section)
        elif section_type == PUBLICATIONS:
            return get_publications(section)
    elif section_type == LANGUAGES:
        return get_languages(section)


def get_projects(section):
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


def get_publications(section):
    # Show all publications
    try:
        section.find_element_by_xpath("//button[@aria-controls='publications-accomplishment-list']").click()
        ul = section.find_element_by_css_selector(
            '.pv-accomplishments-block__list.pv-accomplishments-block__list--has-more')
    except NoSuchElementException:
        ul = section.find_element_by_class_name('pv-accomplishments-block__list ')

    publications = []
    for li in ul.find_elements_by_tag_name('li'):
        title = li.find_element_by_class_name('pv-accomplishment-entity__title').text.\
            replace('publication title', '').strip()
        date = get_optional_text_replace(li, 'pv-accomplishment-entity__date', 'publication date')
        publisher = get_optional_text_replace(li, 'pv-accomplishment-entity__publisher', 'publication description')
        link = get_accomplishment_link(li)

        publications.append({
            'title': title,
            'date': date,
            'publisher': publisher,
            'link': link
        })

    return publications


def get_languages(section):
    return [x.text for x in section.find_elements_by_tag_name('li')]
