import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from globals import *


def get_personal_details(driver, section_type):
    if section_type == NAME:
        return driver.find_element_by_css_selector('.pv-top-card-section__name.inline.t-24.t-black.t-normal').text
    elif section_type == POSITION:
        return get_position(driver)
    elif section_type == CONTACT:
        return get_contact(driver)
    elif section_type == SUMMARY:
        return get_summary(driver)


def get_position(driver):
    position = driver.find_element_by_css_selector('.pv-top-card-section__headline.mt1.t-18.t-black.t-normal').text

    return re.sub('\s+at.*', '', position)


def get_contact(driver):
    driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']").click()

    linkedin_id = WebDriverWait(driver, TIMEOUT).until(ec.presence_of_element_located((
        By.CLASS_NAME, 'pv-contact-info__ci-container'))).find_element_by_tag_name('a').get_attribute('href')
    email = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-email').\
        find_element_by_tag_name('a').text

    try:
        mobile = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-phone').\
            find_element_by_css_selector('.t-14.t-black.t-normal').text
    except NoSuchElementException:
        mobile = ''

    try:
        address = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-address').\
            find_element_by_tag_name('a').text
    except NoSuchElementException:
        address = ''

    # Extract social media
    github = gitlab = stackoverflow = twitter = reddit = medium = scholar = ''
    try:
        websites_section = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-websites')
        for li in websites_section.find_elements_by_tag_name('li'):
            link = li.find_element_by_tag_name('a').get_attribute('href')
            if 'github.com' in link:
                github = link
            elif 'scholar.google.com' in link:
                scholar = link
            elif 'gitlab.com' in link:
                gitlab = link
            elif 'stackoverflow.com' in link:
                stackoverflow = link
            elif 'twitter.com' in link:
                twitter = link
            elif 'reddit' in link:
                reddit = link
            elif 'medium.com' in link:
                medium = link
    except NoSuchElementException:
        pass

    driver.find_element_by_class_name('artdeco-dismiss').click()
    results = {
        ADDRESS: address,
        MOBILE: mobile,
        EMAIL: email,
        HOMEPAGE: '',
        GITHUB: github,
        LINKEDIN: linkedin_id,
        GITLAB: gitlab,
        STACKOVERFLOW: stackoverflow,
        TWITTER: twitter,
        SKYPE: '',
        REDDIT: reddit,
        MEDIUM: medium,
        GOOGLE_SCHOLAR: scholar
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
