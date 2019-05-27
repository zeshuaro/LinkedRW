# LinkedRW

A simple CLI for you to create your resume using the [Awesome CV](https://github.com/posquit0/Awesome-CV) template, 
and your personal website using the [Dev Portfolio](https://github.com/RyanFitzgerald/devportfolio) template, 
based on your LinkedIn profile.

## Installation

Install through pip:

```bash
pip install linkedrw
```

You will also need to download the ChromeDriver from 
[here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and put it in path (e.g. `/usr/local/bin/`)


## Usage

Simply run `linkedrw` to create your resume and personal webiste:

This will create three outputs:

`profile.json` - Your LinkedIn profile is being scraped and stored in this file

`resume/` - The directory containing your resume files

`website/` - The directory containing your personal website files

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

If your resume contains a publication section, run the following commands instead:

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

```
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
