import os
import pkg_resources
import shutil

from selenium.common.exceptions import NoSuchElementException

from linkedrw.constants import LATEX_CHARS


def make_dir(dir_name):
    """
    Make directory
    Args:
        dir_name: the directory name to be created

    Returns:
        None
    """
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass


def copy_files(mod_name, dir_name, output_dir):
    """
    Copy files under dir_name to output_dir
    Args:
        mod_name: the module name
        dir_name: the directory name of the files to be copied
        output_dir: the directory name for the files to be copied to

    Returns:
        None
    """
    files = pkg_resources.resource_filename(mod_name, dir_name)
    for filename in os.listdir(files):
        full_filename = os.path.join(files, filename)
        if os.path.isdir(full_filename):
            try:
                shutil.copytree(full_filename, os.path.join(output_dir, filename))
            except FileExistsError:
                continue
        else:
            shutil.copy(full_filename, output_dir)


def get_span_text(element, name):
    """
    Scrape text inside the span element
    Args:
        element: the element containing the text
        name: the class name

    Returns:
        A string of text
    """
    try:
        return element.find_element_by_css_selector(name).find_elements_by_tag_name('span')[1].text.replace('–', '-')
    except NoSuchElementException:
        return ''


def get_optional_text(element, name, is_span=True):
    """
    Scrape text that may or may not exist
    Args:
        element: the element containing the text
        name: the class name
        is_span: the bool if the text is wrapped inside span tags

    Returns:
        A string of text
    """
    text = ''
    try:
        if is_span:
            text = get_span_text(element, name)
        else:
            text = element.find_element_by_css_selector(name).text.replace('–', '-')
    except NoSuchElementException:
        pass

    return text


def get_optional_text_replace(element, name, text):
    """
    Scrape text that may or may not exist and remove a specific text
    Args:
        element: the element containing the text
        name: the class name
        text: the text to be removed

    Returns:
        A string of text
    """
    try:
        return element.find_element_by_class_name(name).text.replace(text, '').strip()
    except NoSuchElementException:
        return ''


def get_description(element, name):
    """
    Scrape the description
    Args:
        element: the element containing the description
        name: the class name

    Returns:
        A string of description
    """
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

    description = description.replace('•', '-')

    return description


def get_accomplishment_link(element):
    """
    Scrape the accomplishment link
    Args:
        element: the element containing the link

    Returns:
        A string of link
    """
    try:
        return element.find_element_by_class_name('pv-accomplishment-entity__external-source').get_attribute('href')
    except NoSuchElementException:
        return ''


def escape_latex(s):
    """
    Escape LaTeX special characters
    Args:
        s: the string

    Returns:
        a string with escaped LaTeX special characters
    """
    return ''.join(LATEX_CHARS.get(c, c) for c in s)
