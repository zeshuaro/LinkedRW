from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse

from globals import *


def get_personal_details(driver, section_type):
    if section_type == NAME:
        return driver.find_element_by_css_selector('.pv-top-card-section__name.inline.t-24.t-black.t-normal').text
    elif section_type == CONTACT:
        return get_contact(driver)
    elif section_type == SUMMARY:
        return get_summary(driver)


def get_contact(driver):
    driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']").click()

    # Extract email
    email_section = WebDriverWait(driver, TIMEOUT).until(ec.presence_of_element_located((
        By.CSS_SELECTOR, '.pv-contact-info__contact-type.ci-email')))
    email = email_section.find_element_by_tag_name('a').text

    # Extract phone
    try:
        phone_section = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-phone')
        phone = phone_section.find_element_by_css_selector('.t-14.t-black.t-normal').text
    except NoSuchElementException:
        phone = ''

    # Extract address
    try:
        address_section = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-address')
        address = address_section.find_element_by_tag_name('a').text
    except NoSuchElementException:
        address = ''

    # Extract social media
    github_id = scholar_id = ''
    websites_section = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-websites')

    for li in websites_section.find_elements_by_tag_name('li'):
        link = li.find_element_by_tag_name('a').get_attribute('href')
        if 'github' in link:
            github_id = urlparse(link).path.strip('/')
        elif 'scholar' in link:
            scholar_id = urlparse(link).query.lstrip('user=')

    driver.find_element_by_class_name('artdeco-dismiss').click()
    results = {
        'phone': phone,
        'address': address,
        'email': email,
        'github_id': github_id,
        'scholar_id': scholar_id
    }

    return results


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

    return driver.find_element_by_css_selector(
        '.pv-top-card-section__summary-text.text-align-left.mt4.ember-view').text
