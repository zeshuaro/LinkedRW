import time

from collections import defaultdict
from selenium.common.exceptions import NoSuchElementException

from linkedrw.globals import *
from linkedrw.utils import get_span_text, get_optional_text, get_description


def get_background_details(driver, by, section_identifier, section_type):
    # Load background section
    if section_type == EXPERIENCE:
        background = driver.find_element_by_id('oc-background-section')
        driver.execute_script("arguments[0].scrollIntoView(true);", background)
        time.sleep(1)

    # Load the rest of the page
    elif section_type == SKILLS:
        try:
            skills = driver.find_element_by_css_selector('.pv-deferred-area.pv-deferred-area--pending.ember-view')
            driver.execute_script("arguments[0].scrollIntoView(true);", skills)
            time.sleep(1)
        except NoSuchElementException:
            pass

    # Check if the section exists
    try:
        section = driver.find_element(by, section_identifier)
    except NoSuchElementException:
        return []

    if section_type == EXPERIENCE:
        return get_experience(section)
    elif section_type == EDUCATION:
        return get_education(section)
    elif section_type == VOLUNTEERING:
        return get_volunteering(section)
    elif section_type == SKILLS:
        return get_skills(section)


def get_experience(section):
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
        NAME: company,
        ENTRIES: [{
            TITLE: title,
            DATES: dates,
            LOCATION: location,
            DESCRIPTION: description
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
            TITLE: title,
            DATES: dates,
            LOCATION: location,
            DESCRIPTION: description
        })

    results = {
        NAME: company,
        ENTRIES: roles
    }

    return results


def get_education(section):
    try:
        ul = section.find_element_by_css_selector(
            '.pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more.ember-view')
    except NoSuchElementException:
        ul = section.find_element_by_css_selector(
            '.pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more')

    edu_dict = defaultdict(list)
    for li in ul.find_elements_by_tag_name('li'):
        school = li.find_element_by_css_selector('.pv-entity__school-name.t-16.t-black.t-bold').text
        degree_name = get_span_text(
            li, '.pv-entity__secondary-title.pv-entity__degree-name.pv-entity__secondary-title.t-14.t-black.t-normal')
        dates = get_optional_text(li, '.pv-entity__dates.t-14.t-black--light.t-normal')
        description = get_description(li, '.pv-entity__description.t-14.t-black--light.t-normal.mt4')

        # Check for field of study
        try:
            field = get_span_text(
                li,
                '.pv-entity__secondary-title.pv-entity__fos.pv-entity__secondary-title.t-14.t-black--light.t-normal')
            degree = f'{degree_name} - {field}'
        except NoSuchElementException:
            degree = degree_name

        edu_dict[school].append({
            DEGREE: degree,
            LOCATION: '',
            DATES: dates,
            DESCRIPTION: description
        })

    edu_list = []
    for school in edu_dict:
        edu_list.append({
            NAME: school,
            ENTRIES: edu_dict[school]
        })

    return edu_list


def get_volunteering(section):
    ul = section.find_element_by_css_selector(
        '.pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more.ember-view')
    vol_dict = defaultdict(list)

    for li in ul.find_elements_by_tag_name('li'):
        title = li.find_element_by_css_selector('.t-16.t-black.t-bold').text
        organisation = get_span_text(li, '.t-14.t-black.t-normal')
        dates = get_optional_text(
            li, '.pv-entity__date-range.detail-facet.inline-block.t-14.t-black--light.t-normal')
        description = get_description(li, '.pv-entity__description.t-14.t-black--light.t-normal.mt4')

        vol_dict[organisation].append({
            TITLE: title,
            DATES: dates,
            LOCATION: '',
            DESCRIPTION: description
        })

    vol_list = []
    for organisation in vol_dict:
        vol_list.append({
            NAME: organisation,
            ENTRIES: vol_dict[organisation]
        })

    return vol_list


def get_skills(section):
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
