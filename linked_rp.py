import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

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
    driver.find_element(
        By.CSS_SELECTOR,
        '.tap-target.profile-rail-card__actor-link.block.link-without-hover-visited.ember-view').click()

    summary = get_summary(driver)
    print(summary)

    driver.quit()


def get_summary(driver):
    # Check if summary section exists
    try:
        driver.find_element(
            By.CSS_SELECTOR, '.pv-top-card-section__summary.pv-top-card-section__summary--with-content.mt4.ember-view')
    except NoSuchElementException:
        return ''

    # Check if there is a show more button
    try:
        driver.find_element_by_class_name('pv-top-card-section__summary-toggle-button-icon').click()
    except NoSuchElementException:
        pass

    return driver.find_element(
        By.CSS_SELECTOR, '.pv-top-card-section__summary-text.text-align-left.mt4.ember-view').text


if __name__ == '__main__':
    main()
