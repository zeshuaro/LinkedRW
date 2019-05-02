import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse

from accomplishment import get_accomplishment_details
from background import get_background_details
from globals import *


def main():
    with open('config.json') as f:
        credentials = json.load(f)

    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/login/')

    # Login to LinkedIn
    driver.find_element_by_id('username').send_keys(credentials['email'])
    driver.find_element_by_id('password').send_keys(credentials['password'])
    driver.find_element_by_class_name('login__form_action_container').submit()

    # Skip adding a phone number
    try:
        driver.find_element_by_css_selector('.ember-view.cp-add-phone')
        driver.find_element_by_class_name('secondary-action').click()
    except NoSuchElementException:
        pass

    # Navigate to profile page
    driver.find_element_by_xpath("//a[@data-control-name='identity_welcome_message']").click()
    WebDriverWait(driver, TIMEOUT).until(ec.presence_of_element_located((By.ID, 'oc-background-section')))

    profile = {
        'name': driver.find_element_by_css_selector('.pv-top-card-section__name.inline.t-24.t-black.t-normal').text,
        'contact': get_contact(driver),
        'summary': get_summary(driver),
        'experience': get_background_details(driver, By.ID, 'experience-section', EXPERIENCE),
        'education': get_background_details(driver, By.ID, 'education-section', EDUCATION),
        'volunteering': get_background_details(
            driver, By.CSS_SELECTOR, '.pv-profile-section.volunteering-section.ember-view', VOLUNTEERING),
        'skills': get_background_details(
            driver, By.CSS_SELECTOR,
            '.pv-profile-section.pv-skill-categories-section.artdeco-container-card.ember-view', SKILLS),
        'projects': get_accomplishment_details(driver, PROJECTS),
        'publications': get_accomplishment_details(driver, PUBLICATIONS),
        'awards': get_accomplishment_details(driver, AWARDS),
        'languages': get_accomplishment_details(driver, LANGUAGES)
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


def get_contact(driver):
    driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']").click()

    email_section = WebDriverWait(driver, TIMEOUT).until(ec.presence_of_element_located((
        By.CSS_SELECTOR, '.pv-contact-info__contact-type.ci-email')))
    email = email_section.find_element_by_tag_name('a').text

    try:
        phone_section = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-phone')
        phone = phone_section.find_element_by_css_selector('.t-14.t-black.t-normal').text
    except NoSuchElementException:
        phone = ''

    try:
        address_section = driver.find_element_by_css_selector('.pv-contact-info__contact-type.ci-address')
        address = address_section.find_element_by_tag_name('a').text
    except NoSuchElementException:
        address = ''

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


if __name__ == '__main__':
    main()
