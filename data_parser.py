import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from lxml import etree

# schema for the search index
schema = Schema(
    title=TEXT(stored=True),
    authors=TEXT(stored=True),
    year=NUMERIC(stored=True),
    url=ID(unique=True, stored=True),
    type=TEXT(stored=True)
)

# Whoosh index
index_dir = "academic_papers_index"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)
ix = create_in(index_dir, schema)


# function to index academic papers
def index_paper(title, authors, year, url, paper_type):
    writer = ix.writer()
    writer.add_document(
        title=title,
        authors=authors,
        year=year,
        url=url,
        type=paper_type
    )
    writer.commit()


# function to parse and index an entry
def parse_and_index_entry(entry):
    title = entry.findtext('title')
    authors = [author.text for author in entry.xpath('author')]
    year = int(entry.findtext('year'))

    # handle both types of URL elements
    url = entry.findtext('ee[@type="oa"]')

    if url is None:
        url = entry.findtext('url')

    # handle articles without a URL
    if url is None:
        url = "URL not available"

    paper_type = entry.tag

    index_paper(title, ", ".join(authors), year, url, paper_type)


# function to fetch and index academic papers from a source
def fetch_and_index_papers(xml_file):
    # specify the DTD file to be used during parsing
    dtd_file = 'dblp.dtd'

    # create a custom parser with DTD validation
    parser = etree.XMLParser(dtd_validation=True, no_network=False)

    # parse the XML document and specify the DTD file
    tree = etree.parse(xml_file, parser=parser)

    # get all entries from the XML (articles, books, inproceedings, etc.)
    entries = tree.xpath('//article | //book | //inproceedings | //www | //phdthesis | //proceedings | //incollection |'
                         ' //mastersthesis')

    # iterate through articles within the specified range
    for entry in entries:
        parse_and_index_entry(entry)


if __name__ == '__main__':
    fetch_and_index_papers('dblp.xml')  # fetch and index papers on startup
