from selenium.common.exceptions import NoSuchElementException


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