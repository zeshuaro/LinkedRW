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

| Options | Descriptions |
| --- | --- |
| -h, --help | Show help message and exit |
| -e, --email | Your LinkedIn login email |
| -p, --password | Your LinkedIn login password |
| -k, --keep_creds | Store your LinkedIn login credentials under ~/.linkedrw/credentials.json |
| -o, --output_dir | The output directory (default: current directory) |
| -s, --scrape_only | Only scrape LinkedIn profile |
| -r, --resume_only | Only create resume files |
| -w, --website_only | Only create personal website files |
| -j, --profile | Your profile json file |
