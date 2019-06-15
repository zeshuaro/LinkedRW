import os
import re

from habanero import Crossref, cn
from logbook import Logger
from requests.exceptions import HTTPError
from urllib.parse import urlparse

from linkedrw.constants import *
from linkedrw.utils import escape_latex


def make_publication_section(publications, output_dir):
    """
    Create publication latex file
    Args:
        publications: the list of publications
        output_dir: the output directory

    Returns:
        A bool if there are any publications
    """
    if publications:
        references = make_references(publications, output_dir)
        lines = [f'\\cvsection{{{PUBLICATIONS.title()}}}\n', '\\begin{refsection}']

        for reference in references:
            lines.append(f'{LATEX_INDENT}\\nocite{{{escape_latex(reference)}}}')

        lines.append(f'{LATEX_INDENT}\\printbibliography[heading=none]')
        lines.append('\\end{refsection}')

        with open(os.path.join(output_dir, f'{PUBLICATIONS}.tex'), 'w') as f:
            f.write('\n'.join(lines))

        return True

    return False


def make_references(publications, output_dir):
    """
    Create reference bib file
    Args:
        publications: the list of publications
        output_dir: the output directory

    Returns:
        A list of reference identifiers
    """
    log = Logger()
    cr = Crossref()
    lines = []
    references = []

    for i, publication in enumerate(publications):
        log.notice(f'Querying and formatting {i + 1} out of {len(publications)} publications')
        link = publication[LINK]
        title = publication[TITLE]

        # Check if it is a DOI url
        if link and 'doi.org' in link:
            doi = urlparse(link).path.strip('/')

        # Extract the DOI using the title
        else:
            results = cr.works(query_title=title, limit=1)
            if results['message']['total-results'] == 0 or \
                    results['message']['items'][0]['title'][0].lower() != title.lower():
                log.warn(f'Could not find the doi for "{title}"')

                continue

            doi = results['message']['items'][0]['DOI']

        try:
            reference = cn.content_negotiation(doi)
            lines.append(reference)
            references.append(re.sub('^@.*{', '', reference.split('\n')[0]).strip(','))
        except HTTPError:
            log.warn(f'Could not Create reference for "{title}"')

    with open(os.path.join(output_dir, 'references.bib'), 'w') as f:
        f.write('\n\n'.join(lines))

    return references
