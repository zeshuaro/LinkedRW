import argparse

from linkedrw.scraper import scrape


def main(email, password, keep_credentials, output_dir, scrape_only, resume_only, website_only, profile, **kwargs):
    if profile is None:
        check_credentials(email, password)
        profile = scrape(email, password)


def check_credentials(email, password):
    if email is None:
        raise argparse.ArgumentError(None, 'Email must be provided')
    elif password is None:
        raise argparse.ArgumentError(None, 'Password must be provided')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates a resume and a personal website based on your LinkedIn profile')
    parser.set_defaults(method=main)

    parser.add_argument('--email', '-e', help='Your LinkedIn login email')
    parser.add_argument('--password', '-p', help='Your LinkedIn login password')
    parser.add_argument('--keep_credentials', '-k', action='store_true',
                        help='Store LinkedIn login credentials under ~/.linkedrw/credentials.json')
    parser.add_argument('--output_dir', '-o', default='.', help='The output directory (default: current directory)')
    parser.add_argument('--scrape_only', '-s', action='store_true', help='Only scrape LinkedIn profile')
    parser.add_argument('--resume_only', '-r', action='store_true', help='Only generate resume')
    parser.add_argument('--website_only', '-w', action='store_true', help='Only generate personal website')
    parser.add_argument('--profile', '-j', help='The profile json file')

    args = parser.parse_args()
    args.method(**vars(args))
