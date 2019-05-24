import argparse
import json
import logbook
import os
import sys

from logbook import Logger, StreamHandler

from globals import PACKAGE_NAME, CREDENTIALS_FILE
from linkedr import make_resume_files
from scraper import scrape
from utils import make_dir
from linkedw import make_website_files


def main():
    parser = argparse.ArgumentParser(
        description='Generates a resume and a personal website based on your LinkedIn profile')
    parser.set_defaults(method=run)

    parser.add_argument('--email', '-e', help='Your LinkedIn login email')
    parser.add_argument('--password', '-p', help='Your LinkedIn login password')
    parser.add_argument('--keep_creds', '-k', action='store_true',
                        help=f'Store LinkedIn login credentials under {CREDENTIALS_FILE}')
    parser.add_argument('--output_dir', '-o', default='.', help='The output directory (default: current directory)')
    parser.add_argument('--scrape_only', '-s', action='store_true', help='Only scrape LinkedIn profile')
    parser.add_argument('--resume_only', '-r', action='store_true', help='Only generate resume')
    parser.add_argument('--website_only', '-w', action='store_true', help='Only generate personal website')
    parser.add_argument('--profile', '-j', dest='profile_file', help='The profile json file')

    args = parser.parse_args()
    args.method(**vars(args))


def run(email, password, keep_creds, output_dir, scrape_only, resume_only, website_only, profile_file, **kwargs):
    # Setup logging
    logbook.set_datetime_format('local')
    format_string = '[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.message}'
    StreamHandler(sys.stdout, format_string=format_string).push_application()
    log = Logger()

    # Create output directory
    make_dir(output_dir)

    # Check if user has provided the profile json file
    if profile_file is None:
        credentials_file = os.path.expanduser(CREDENTIALS_FILE)

        # Check if credentials file exists
        if os.path.exists(credentials_file):
            with open(credentials_file) as f:
                credentials = json.load(f)
                email = credentials['email']
                password = credentials['password']
        else:
            check_creds(email, password)

        log.notice('Scraping LinkedIn profile...')
        log.notice('Please keep the browser window on top')
        profile = scrape(email, password, output_dir)

        if keep_creds:
            store_creds(email, password, credentials_file)
    else:
        with open(profile_file) as f:
            profile = json.load(f)

    if not scrape_only:
        if resume_only:
            make_resume_files(profile, output_dir)
        elif website_only:
            make_website_files(profile, output_dir)
        else:
            make_resume_files(profile, output_dir)
            make_website_files(profile, output_dir)


def check_creds(email, password):
    """
    Check login credentials arguments
    Args:
        email: the LinkedIn login email
        password: the LinkedIn login password

    Returns:
        Raise an exception if any of the parameters is None
    """
    if email is None:
        raise argparse.ArgumentError(None, 'Email must be provided')
    elif password is None:
        raise argparse.ArgumentError(None, 'Password must be provided')


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


if __name__ == '__main__':
    main()
