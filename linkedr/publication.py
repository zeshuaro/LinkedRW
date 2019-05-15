import re

from habanero import Crossref, cn
from urllib.parse import urlparse

from globals import *


def make_publication_section(publications):
    if publications:
        references = make_references(publications)
        lines = [f'\\cvsection{{{PUBLICATIONS.title()}}}\n', '\\begin{refsection}']

        for reference in references:
            lines.append(f'{LATEX_INDENT}\\nocite{{{reference}}}')

        lines.append(f'{LATEX_INDENT}\\printbibliography[heading=none]')
        lines.append('\\end{refsection}')

        with open(f'{PUBLICATIONS}.tex', 'w') as f:
            f.write('\n'.join(lines))

        return True

    return False


def make_references(publications):
    cr = Crossref()
    lines = []
    references = []

    for i, publication in enumerate(publications):
        print(f'Querying and formatting {i + 1} out of {len(publications)} publications...')
        link = publication[LINK]

        # Check if it is a DOI url
        if link and 'doi.org' in link:
            doi = urlparse(link).path.strip('/')

        # Extract the DOI using the title
        else:
            title = publication[TITLE]
            results = cr.works(query_title=title, limit=1)

            if results['message']['total-results'] == 0 or \
                    results['message']['items'][0]['title'][0].lower() != title.lower():
                print(f'Could not find the doi for "{title}"')

                continue

            doi = results['message']['items'][0]['DOI']

        reference = cn.content_negotiation(doi)
        lines.append(reference)
        references.append(re.sub('^@.*{', '', reference.split('\n')[0]).strip(','))

    with open('references.bib', 'w') as f:
        f.write('\n\n'.join(lines))

    return references
