# LinkedRW

[![PyPi Package Version](https://img.shields.io/pypi/v/linkedrw.svg)](https://pypi.org/project/linkedrw/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/linkedrw.svg)](https://pypi.org/project/linkedrw/)
[![MIT License](https://img.shields.io/pypi/l/linkedrw.svg)](https://github.com/zeshuaro/LinkedRW/blob/master/LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/04b86b6463f749f79378ca580257fbb7)](https://www.codacy.com/app/zeshuaro/LinkedRW?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zeshuaro/LinkedRW&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/zeshuaro/LinkedRW.svg?style=svg)](https://circleci.com/gh/zeshuaro/LinkedRW)

A simple CLI for you to create your resume using the [Awesome CV](https://github.com/posquit0/Awesome-CV) template, 
and your personal website using the [Dev Portfolio](https://github.com/RyanFitzgerald/devportfolio) template, 
based on your LinkedIn profile.

## Installation

Install through pip:

```bash
pip install linkedrw
```

You will also need to download a web driver and put it in path (e.g. `/usr/local/bin/`), `linkedrw` supports the following: 

* [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* [Firefox Driver](https://github.com/mozilla/geckodriver/releases)
* [Opera Driver](https://github.com/operasoftware/operachromiumdriver/releases)
* Safari Driver ([Instructions](https://webkit.org/blog/6900/webdriver-support-in-safari-10/) to configure Safari to allow automation)

## Usage

Simply run `linkedrw` to create your resume and personal webiste:

This will create three outputs:

`profile.json` - Your LinkedIn profile is being scraped and stored in this file

`resume/` - The directory containing your resume files

`website/` - The directory containing your personal website files

### Running Without LinkedIn

Scraping from LinkedIn allows you to only manage and update your profile there 
while keeping your resume and personal website up-to-date. 
However, you can also create your resume and personal website by using a JSON file.
Check out the example [here](example.json) for the JSON format that `linkedrw` accepts.
Once you have your JSON profile ready, run the following command to create your resume and personal website:

```bash
linkedrw -j example.json
```

### Compiling Your Resume

The `resume/` directory contains a list of LaTex files that can be compiled into a PDF resume file. 
As per the instructions and requirements from [Awesome-CV](https://github.com/posquit0/Awesome-CV), 
a full TeX distribution needs to be installed to compile the LaTex files. 
You can download and install it from [here](https://www.latex-project.org/get/#tex-distributions).

Please note that `linkedrw` will try to compile the LaTex files for you if the requirements are met.

After installing the TeX distribution, run the following commands to compile your resume:

```bash
cd resume/
xelatex resume.tex
```

This should create your PDF resume file `resume.pdf`

If your resume contains a publication section, 
[**BibLaTeX**](https://www.ctan.org/pkg/biblatex) and [**biber**](https://www.ctan.org/pkg/biber) should also be available. 
And run the following commands instead:

```bash
cd resume/
xelatex resume.tex
biber resume
xelatex resume.tex
```

### Personal Website

Simply navigate to the `website/` directory and open `index.html` in a web browser, 
and you should be able to see your personal website.

### Options

Below is the list of options:

```text
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
  --resume_only, -r     Only create resume
  --website_only, -w    Only create personal website
  --profile PROFILE_FILE, -j PROFILE_FILE
                        The profile json file
  --driver DRIVER, -d DRIVER
                        The web driver: chrome, firefox, safari, opera
                        (default: chrome)
  --timeout TIMEOUT, -t TIMEOUT
                        The timeout value (default: 10)
```

## Customisation

### Customising Your Resume

The comments in `resume.pdf` give you guidelines on customising your resume.

### Customising Your Personal Website

Run the following commands to install the dependencies first:

```bash
cd website/
npm install
```

Then run the following command so that it can be auto compiled when there are changes made to `js/scripts.js` or `sass/styles.css`:

```bash
npm run watch
```

For more customisation instructions, please refer to the original [repo](https://github.com/RyanFitzgerald/devportfolio).

## Issues

If `NoSuchElementException` is raised, try increasing the timeout value by specifying `-t/--timeout` option.
If the problem remains, please raise an issue.