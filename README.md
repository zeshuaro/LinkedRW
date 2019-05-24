# LinkedRW

A simple CLI for you to create your resume using the [Awesome CV](https://github.com/posquit0/Awesome-CV) template, 
and your personal website using the [Dev Portfolio](https://github.com/RyanFitzgerald/devportfolio) template 
based on your LinkedIn profile.

## Installation

Install through pip:

`pip install linkedrw`

Install through Github:

`pip install git+https://github.com/zeshuaro/LinkedRW`

Or

```bash
git clone https://github.com/zeshuaro/LinkedRW
cd LinkedRW
python setup.py install
```

## Usage

Simply run the following command to create your resume and personal webiste:

```
linkedrw -e example@email.com -p password
```

This will create three outputs:

`profile.json` - Your LinkedIn profile is scraped and stored in this file

`resume/` - The directory containing your resume files

`website/` - The directory containing your personal website files


### Options

```bash
  -h, --help            show this help message and exit
  --email EMAIL, -e EMAIL
                        Your LinkedIn login email
  --password PASSWORD, -p PASSWORD
                        Your LinkedIn login password
  --keep_creds, -k      Store LinkedIn login credentials under
                        ~/.linkedrw/credentials.json
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        The output directory (default: current directory)
  --scrape_only, -s     Only scrape LinkedIn profile
  --resume_only, -r     Only generate resume
  --website_only, -w    Only generate personal website
  --profile PROFILE_FILE, -j PROFILE_FILE
                        The profile json file
```
