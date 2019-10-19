import time

from collections import defaultdict
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from linkedrw.constants import *
from linkedrw.utils import (
    get_span_text,
    get_optional_text,
    get_description,
    scroll_to_elem,
)


def get_background_details(driver, by, section_id, section_type):
    """
    Scrape background details
    Args:
        driver: the selenium details
        by: the strategy to locate an element
        section_id: the section identifier
        section_type: the section type

    Returns:
        A list of details of all the items under the given section
    """
    # Load background section
    if section_type == EXPERIENCE:
        scroll_to_elem(driver, By.ID, "oc-background-section")

    # Load the rest of the page
    elif section_type == SKILLS:
        try:
            scroll_to_elem(
                driver,
                By.CSS_SELECTOR,
                ".pv-deferred-area.pv-deferred-area--pending.ember-view",
            )
        except NoSuchElementException:
            pass

    # Check if the section exists
    try:
        section = driver.find_element(by, section_id)
    except NoSuchElementException:
        return []

    if section_type == EXPERIENCE:
        return get_experience(section)
    elif section_type == EDUCATION:
        return get_education(section)
    elif section_type == VOLUNTEERING:
        return get_volunteering(section)
    elif section_type == SKILLS:
        return get_skills(driver, section)


def get_experience(section):
    """
    Scrape experience details
    Args:
        section: the experience section

    Returns:
        A list of details of all experiences
    """
    ul = get_section(section)
    entries = ul.find_elements_by_css_selector(
        ".pv-profile-section__sortable-item.pv-profile-section__section-info-item.relative."
        "pv-profile-section__list-item.sortable-item.ember-view"
    )
    entries += ul.find_elements_by_css_selector(
        ".pv-entity__position-group-pager.pv-profile-section__list-item.ember-view"
    )
    exps = []

    for entry in entries:
        # Check if it is a single role in a company or multiple roles in a company
        try:
            summary = entry.find_element_by_css_selector(
                ".pv-entity__summary-info.pv-entity__summary-info--background-section"
            )
            exps.append(get_single_role(entry, summary))
        except NoSuchElementException:
            summary = entry.find_element_by_css_selector(
                ".pv-profile-section__card-item-v2.pv-profile-section.pv-position-entity.ember-view"
            )
            exps.append(get_multiple_roles(entry, summary))

    return exps


def get_single_role(div, summary):
    """
    Scrape details of a single role
    Args:
        div: the div element
        summary: the summary section

    Returns:
        A dict of the details for a single role
    """
    title = summary.find_element_by_css_selector(".t-16.t-black.t-bold").text
    company = summary.find_element_by_class_name("pv-entity__secondary-title").text
    dates = get_span_text(
        summary, ".pv-entity__date-range.t-14.t-black--light.t-normal"
    )
    location = get_optional_text(
        summary, ".pv-entity__location.t-14.t-black--light.t-normal.block"
    )
    description = get_description(
        div, ".pv-entity__description.t-14.t-black.t-normal.ember-view"
    )

    results = {
        NAME: company,
        ENTRIES: [
            {TITLE: title, DATES: dates, LOCATION: location, DESCRIPTION: description}
        ],
    }

    return results


def get_multiple_roles(div, summary):
    """
    Scrape details of multiple roles
    Args:
        div: the div element
        summary: the summary section

    Returns:
        A dict of the details for multiple roles
    """
    try:
        role_sections = div.find_elements_by_class_name(
            "pv-entity__position-group-role-item"
        )
    except NoSuchElementException:
        role_sections = div.find_elements_by_class_name(
            "pv-entity__position-group-role-item-fading-timeline"
        )

    roles = []
    for role_section in role_sections:
        title = get_span_text(role_section, ".t-14.t-black.t-bold")
        dates = get_span_text(
            role_section, ".pv-entity__date-range.t-14.t-black.t-normal"
        )
        location = get_optional_text(
            role_section, ".pv-entity__location.t-14.t-black--light.t-normal.block"
        )
        description = get_description(
            role_section, ".pv-entity__description.t-14.t-black.t-normal.ember-view"
        )

        roles.append(
            {TITLE: title, DATES: dates, LOCATION: location, DESCRIPTION: description}
        )

    results = {NAME: get_span_text(summary, ".t-16.t-black.t-bold"), ENTRIES: roles}

    return results


def get_education(section):
    """
    Scrape education details
    Args:
        section: the education section

    Returns:
        A list of details of all educations
    """
    ul = get_section(section)
    edu_dict = defaultdict(list)

    for li in ul.find_elements_by_tag_name("li"):
        school = li.find_element_by_css_selector(
            ".pv-entity__school-name.t-16.t-black.t-bold"
        ).text
        degree_name = get_span_text(
            li,
            ".pv-entity__secondary-title.pv-entity__degree-name.pv-entity__secondary-title.t-14.t-black.t-normal",
        )
        dates = get_optional_text(li, ".pv-entity__dates.t-14.t-black--light.t-normal")
        description = get_description(
            li, ".pv-entity__description.t-14.t-black--light.t-normal.mt4"
        )

        # Check if there is a degree name, if not, skip this entry
        if not degree_name:
            continue

        edu_dict[school].append(
            {
                DEGREE: get_degree(li, degree_name),
                LOCATION: "",
                DATES: dates,
                DESCRIPTION: description,
            }
        )

    edu_list = []
    for school in edu_dict:
        edu_list.append({NAME: school, ENTRIES: edu_dict[school]})

    return edu_list


def get_degree(li, degree_name):
    """
    Get the full degree description
    Args:
        li: the li element
        degree_name: the degree name

    Returns:
        A string of the degree description
    """

    # Check if there is a field of study
    try:
        field = get_span_text(
            li,
            ".pv-entity__secondary-title.pv-entity__fos.pv-entity__secondary-title.t-14.t-black--light.t-normal",
        )
        degree = f"{degree_name} - {field}"
    except NoSuchElementException:
        degree = degree_name

    return degree


def get_volunteering(section):
    """
    Scrape volunteering details
    Args:
        section: the volunteering section

    Returns:
        A list of details of all volunteering
    """
    ul = get_section(section)
    vol_dict = defaultdict(list)

    for li in ul.find_elements_by_tag_name("li"):
        title = li.find_element_by_css_selector(".t-16.t-black.t-bold").text
        organisation = get_span_text(li, ".t-14.t-black.t-normal")
        dates = get_optional_text(
            li,
            ".pv-entity__date-range.detail-facet.inline-block.t-14.t-black--light.t-normal",
        )
        description = get_description(
            li, ".pv-entity__description.t-14.t-black--light.t-normal.mt4"
        )

        vol_dict[organisation].append(
            {TITLE: title, DATES: dates, LOCATION: "", DESCRIPTION: description}
        )

    vol_list = []
    for organisation in vol_dict:
        vol_list.append({NAME: organisation, ENTRIES: vol_dict[organisation]})

    return vol_list


def get_skills(driver, section):
    """
    Scrape skills
    Args:
        driver: the web driver
        section: the skills section

    Returns:
        A list of skills
    """

    # Show all skills
    try:
        btn = scroll_to_elem(
            driver, By.CLASS_NAME, "pv-skills-section__chevron-icon", align="false"
        )
        btn.click()
    except NoSuchElementException:
        pass

    # Extract top skills
    skills = []
    for top_skill in section.find_elements_by_css_selector(
        ".pv-skill-category-entity__top-skill.pv-skill-category-entity.pb3.pt4.pv-skill-endorsedSkill-entity."
        "relative.ember-view"
    ):
        skill = top_skill.find_element_by_css_selector(
            ".pv-skill-category-entity__name-text.t-16.t-black.t-bold"
        ).text
        skills.append(skill.split("\n")[0])

    # Locate Tools & Technologies section
    target_div = None
    for div in section.find_elements_by_css_selector(
        ".pv-skill-category-list.pv-profile-section__section-info.mb6.ember-view"
    ):
        header = div.find_element_by_tag_name("h3")
        if header.text.lower() == "tools & technologies":
            target_div = div
            break

    # Extract the rest of the skills
    if target_div is not None:
        for li in target_div.find_elements_by_tag_name("li"):
            skills.append(li.text.split("\n")[0])

    return skills


def get_section(section):
    """
    Get the items section
    Args:
        section: the section

    Returns:
        The items section
    """
    is_expanded = expand_section(section)
    if is_expanded:
        # The ul element can appear in two different classes
        try:
            elem = section.find_element_by_css_selector(
                ".pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-more.ember-view"
            )
        except NoSuchElementException:
            elem = section.find_element_by_css_selector(
                ".pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-more"
            )
    else:
        # The ul element can appear in two different classes
        try:
            elem = section.find_element_by_css_selector(
                ".pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more."
                "ember-view"
            )
        except NoSuchElementException:
            elem = section.find_element_by_css_selector(
                ".pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more"
            )

    return elem


def expand_section(section):
    css = ".pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link"
    btns = []
    count = 0

    all_btns = section.find_elements_by_css_selector(css)
    if all_btns:
        btns.append(all_btns[-1])

    while btns:
        btn = btns.pop()
        text = btn.text.lower()
        btn.click()
        time.sleep(1)

        if EXPERIENCE in text or EDUCATION in text:
            count += 1

        new_btns = section.find_elements_by_css_selector(css)
        if new_btns:
            btns.append(new_btns[-1])

    return count > 0
