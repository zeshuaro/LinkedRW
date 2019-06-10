from selenium.common.exceptions import NoSuchElementException

from linkedrw.constants import *
from linkedrw.utils import get_optional_text, get_optional_text_replace, get_description, get_accomplishment_link


def get_accomplishment_details(driver, section_type):
    """
    Scrape accomplishment details
    Args:
        driver: the selenium driver
        section_type: the section type

    Returns:
        A list of details of all the items under the given section
    """
    # Check if the section exists
    try:
        section = driver.find_element_by_css_selector(
            f'.accordion-panel.pv-profile-section.pv-accomplishments-block.{section_type}.ember-view')
        if 'display: none' in section.get_attribute('style'):
            return []
    except NoSuchElementException:
        return []

    if section_type in (PROJECTS, PUBLICATIONS, HONORS):
        # Expand the section
        section.find_element_by_xpath(f"//button[@aria-controls='{section_type}-expandable-content']").click()
        section = driver.find_element_by_css_selector(
            f'.accordion-panel.pv-profile-section.pv-accomplishments-block.{section_type}.'
            f'pv-accomplishments-block--expanded.ember-view')

        # Show all items
        try:
            section.find_element_by_xpath(f"//button[@aria-controls='{section_type}-accomplishment-list']").click()
            ul = section.find_element_by_css_selector(
                '.pv-accomplishments-block__list.pv-accomplishments-block__list--has-more')
        except NoSuchElementException:
            ul = section.find_element_by_class_name('pv-accomplishments-block__list ')

        if section_type == PROJECTS:
            return get_projects(ul)
        elif section_type == PUBLICATIONS:
            return get_publications(ul)
        elif section_type == HONORS:
            return get_honors(ul)
    elif section_type == LANGUAGES:
        return get_languages(section)


def get_projects(ul):
    """
    Scrape projects details
    Args:
        ul: the ul element

    Returns:
        A list of details of all projects
    """
    projects = []
    for li in ul.find_elements_by_tag_name('li'):
        name = li.find_element_by_class_name('pv-accomplishment-entity__title').text.replace('Project name', '').strip()
        dates = get_optional_text(li, '.pv-accomplishment-entity__date.pv-accomplishment-entity__subtitle',
                                  is_span=False)
        description = get_description(li, '.pv-accomplishment-entity__description.t-14.t-black--light.t-normal').\
            lstrip('Project description\n')
        link = get_accomplishment_link(li)

        projects.append({
            NAME: name,
            DATES: dates,
            DESCRIPTION: description,
            LINK: link
        })

    return projects


def get_publications(ul):
    """
    Scrape publications details
    Args:
        ul: the ul element

    Returns:
        A list of details of all publications
    """
    publications = []
    for li in ul.find_elements_by_tag_name('li'):
        title = li.find_element_by_class_name('pv-accomplishment-entity__title').text.\
            replace('publication title', '').strip()
        date = get_optional_text_replace(li, 'pv-accomplishment-entity__date', 'publication date')
        publisher = get_optional_text_replace(li, 'pv-accomplishment-entity__publisher', 'publication description')
        link = get_accomplishment_link(li)

        publications.append({
            TITLE: title,
            DATE: date,
            PUBLISHER: publisher,
            LINK: link
        })

    return publications


def get_honors(ul):
    """
    Scrape honors/awards details
    Args:
        ul: the ul element

    Returns:
        A list of details of all honors/awards
    """
    awards = []
    for li in ul.find_elements_by_tag_name('li'):
        title = li.find_element_by_class_name('pv-accomplishment-entity__title').text.\
            replace('honor title', '').strip()
        date = get_optional_text_replace(li, 'pv-accomplishment-entity__date', 'honor date')
        issuer = get_optional_text_replace(li, 'pv-accomplishment-entity__issuer', 'honor issuer')

        awards.append({
            TITLE: title,
            DATE: date,
            LOCATION: '',
            ISSUER: issuer
        })

    return awards


def get_languages(section):
    """
    Scrape languages
    Args:
        section: the languages section

    Returns:
        A list of languages
    """
    return [x.text for x in section.find_elements_by_tag_name('li')]
