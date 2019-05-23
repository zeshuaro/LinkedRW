import argparse
import json
import logbook
import os
import sys

from logbook import Logger, StreamHandler

from linkedrw.globals import PACKAGE_NAME, CREDENTIALS_FILE
from linkedrw.scraper import scrape


def main(email, password, keep_credentials, output_dir, scrape_only, resume_only, website_only, profile, **kwargs):
    logbook.set_datetime_format('local')
    format_string = '[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.message}'
    StreamHandler(sys.stdout, format_string=format_string).push_application()
    log = Logger()

    if profile is None:
        credentials_file = os.path.expanduser(CREDENTIALS_FILE)
        if os.path.exists(credentials_file):
            with open(credentials_file) as f:
                credentials = json.load(f)
                email = credentials['email']
                password = credentials['password']
        else:
            check_credentials(email, password)

        log.notice('Scraping LinkedIn profile...')
        log.notice('Please keep the browser window on top')
        profile = scrape(email, password)

        if keep_credentials:
            store_credentials(email, password, credentials_file)


def check_credentials(email, password):
    if email is None:
        raise argparse.ArgumentError(None, 'Email must be provided')
    elif password is None:
        raise argparse.ArgumentError(None, 'Password must be provided')


def store_credentials(email, password, credentials_file):
    log = Logger()
    log.warn(f'It is highly NOT recommended to keep your login credentials, '
             f'you can always remove the file {CREDENTIALS_FILE} to remove them')
    credentials = {'email': email, 'password': password}

    try:
        os.mkdir(os.path.expanduser(f'~/.{PACKAGE_NAME}'))
    except FileExistsError:
        pass

    with open(credentials_file, 'w') as f:
        json.dump(credentials, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates a resume and a personal website based on your LinkedIn profile')
    parser.set_defaults(method=main)

    parser.add_argument('--email', '-e', help='Your LinkedIn login email')
    parser.add_argument('--password', '-p', help='Your LinkedIn login password')
    parser.add_argument('--keep_credentials', '-k', action='store_true',
                        help=f'Store LinkedIn login credentials under {CREDENTIALS_FILE}')
    parser.add_argument('--output_dir', '-o', default='.', help='The output directory (default: current directory)')
    parser.add_argument('--scrape_only', '-s', action='store_true', help='Only scrape LinkedIn profile')
    parser.add_argument('--resume_only', '-r', action='store_true', help='Only generate resume')
    parser.add_argument('--website_only', '-w', action='store_true', help='Only generate personal website')
    parser.add_argument('--profile', '-j', help='The profile json file')

    args = parser.parse_args()
    args.method(**vars(args))
