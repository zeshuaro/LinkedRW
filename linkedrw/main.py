import argparse
import json
import logbook
import os
import sys

from getpass import getpass
from logbook import Logger, StreamHandler

from linkedrw.constants import PACKAGE_NAME, CREDENTIALS_FILE, CHROME, DRIVERS
from linkedrw.utils import make_dir
from linkedrw.scraper import scrape
from linkedrw.linkedr import make_resume_files
from linkedrw.linkedw import make_website_files


def main():
    parser = argparse.ArgumentParser(
        description='Creates a resume and a personal website based on your LinkedIn profile')
    parser.set_defaults(method=run)

    parser.add_argument('--email', '-e', help='Your LinkedIn login email')
    parser.add_argument('--password', '-p', help='Your LinkedIn login password')
    parser.add_argument('--keep_creds', '-k', action='store_true',
                        help=f'Store LinkedIn login credentials under {CREDENTIALS_FILE}')
    parser.add_argument('--output_dir', '-o', default='.', help='The output directory (default: current directory)')
    parser.add_argument('--scrape_only', '-s', action='store_true', help='Only scrape LinkedIn profile')
    parser.add_argument('--resume_only', '-r', action='store_true', help='Only create resume')
    parser.add_argument('--website_only', '-w', action='store_true', help='Only create personal website')
    parser.add_argument('--profile', '-j', dest='profile_file', help='The profile json file')
    parser.add_argument('--driver', '-d', default=CHROME,
                        help=f'The web driver: {", ".join(DRIVERS)} (default: %(default)s)')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='The timeout value (default: %(default)s)')

    args = parser.parse_args()
    args.method(**vars(args))


def run(driver, email, password, keep_creds, output_dir, scrape_only, resume_only, website_only, profile_file, timeout,
        **kwargs):
    # Setup logging
    logbook.set_datetime_format('local')
    format_string = '[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.message}'
    StreamHandler(sys.stdout, format_string=format_string).push_application()
    log = Logger()

    # Create output directory
    make_dir(output_dir)

    # Check if user has provided the profile json file
    if profile_file is None:
        if driver.lower() not in DRIVERS:
            raise ValueError(f'Browser driver has to be one of these: {", ".join(DRIVERS)}')

        # Check if credentials file exists
        credentials_file = os.path.expanduser(CREDENTIALS_FILE)
        if os.path.exists(credentials_file):
            with open(credentials_file) as f:
                credentials = json.load(f)
                email = credentials['email']
                password = credentials['password']
        else:
            if email is None:
                email = input('Enter your LinkedIn login email: ')
            if password is None:
                password = getpass('Enter your LinkedIn login password: ')

        log.notice('Scraping LinkedIn profile')
        log.notice('Please keep the browser window on top')
        profile = scrape(driver.lower(), email, password, output_dir, timeout)

        if keep_creds:
            store_creds(email, password, credentials_file)
    else:
        with open(profile_file) as f:
            profile = json.load(f)

    if not scrape_only:
        if resume_only:
            make_resume_files(profile, output_dir, timeout)
        elif website_only:
            make_website_files(profile, output_dir)
        else:
            make_resume_files(profile, output_dir, timeout)
            make_website_files(profile, output_dir)


def store_creds(email, password, creds_file):
    """
    Store login credentials
    Args:
        email: the LinkedIn login email
        password: the LinkedIn login password
        creds_file: the credentials file to store the login credentials

    Returns:
        None
    """
    log = Logger()
    log.warn(f'It is highly NOT recommended to keep your login credentials, '
             f'you can always remove the file {CREDENTIALS_FILE} to remove them')

    make_dir(os.path.expanduser(f'~/.{PACKAGE_NAME}'))
    credentials = {'email': email, 'password': password}

    with open(creds_file, 'w') as f:
        json.dump(credentials, f)
