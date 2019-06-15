import os
import tempfile

from linkedrw.constants import *
from linkedrw.linkedr.publication import make_publication_section, make_references

PUBS = [
    {
        TITLE: 'A rapid and sensitive method for the quantitation of microgram quantities of protein utilizing the '
               'principle of protein-dye binding',
        DATE: '',
        PUBLISHER: '',
        LINK: 'https://doi.org/10.1016/0003-2697(76)90527-3'
    },
    {
        TITLE: 'DNA sequencing with chain-terminating inhibitors',
        DATE: '',
        PUBLISHER: '',
        LINK: 'https://doi.org/10.1073/pnas.74.12.5463'
    },
    {
        TITLE: 'Electrophoretic transfer of proteins from polyacrylamide gels to nitrocellulose sheets: procedure and '
               'some applications.',
        DATE: '',
        PUBLISHER: '',
        LINK: 'https://doi.org/10.1073/pnas.76.9.4350'
    }
]
CITES = ['Bradford\\_1976', 'Sanger\\_1977', 'Towbin\\_1979']


def test_make_publication_section_empty():
    with tempfile.TemporaryDirectory() as dirname:
        assert make_publication_section([], dirname) is False
        assert os.path.exists(os.path.join(dirname, f'{PUBLICATIONS}.tex')) is False


def test_make_publication_section():
    with tempfile.TemporaryDirectory() as dirname:
        assert make_publication_section(PUBS, dirname) is True

        cites = set()
        with open(os.path.join(dirname, f'{PUBLICATIONS}.tex')) as f:
            for line in f:
                if '\\nocite' in line:
                    cites.add(line.strip().lstrip('\\nocite').strip('{}'))

        assert cites == set(CITES)


def test_make_references_no_doi():
    pub = PUBS[0]
    pub[LINK] = ''

    with tempfile.TemporaryDirectory() as dirname:
        assert make_references([pub], dirname) == CITES[:1]
        with open(os.path.join(dirname, 'references.bib')) as f:
            assert f.read() != ''


def test_make_references_not_found():
    pub = {
        TITLE: 'Some random title',
        DATE: '',
        PUBLISHER: '',
        LINK: ''
    }

    with tempfile.TemporaryDirectory() as dirname:
        assert make_references([pub], dirname) == []
        with open(os.path.join(dirname, 'references.bib')) as f:
            assert f.read() == ''
