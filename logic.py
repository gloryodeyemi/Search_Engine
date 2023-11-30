from whoosh.index import open_dir
from whoosh.qparser import QueryParser

# open the existing Whoosh index
index_dir = "academic_papers_index"
ix = open_dir(index_dir)

RESULTS_PER_PAGE = 25


# function to extract paper information from the search results
def get_papers(results):
    papers = [
        {
            "title": result['title'],
            "authors": result['authors'],
            "year": result['year'],
            "type": result['type'],
            "url": result['url']
        }
        for result in results
    ]
    return papers


def paper_search(query):
    # perform a search using the query
    with ix.searcher() as searcher:
        query_parser = QueryParser("title", schema=ix.schema)
        q = query_parser.parse(query)
        results = searcher.search(q)
        papers = get_papers(results)
    return papers


# function to fetch titles from the data source based on the specified alphabet
def get_titles_by_alphabet_with_pagination(alphabet, page_number):
    with ix.searcher() as searcher:
        query_parser = QueryParser("title", schema=ix.schema)
        query_string = f"{alphabet}*"
        q = query_parser.parse(query_string)
        results = searcher.search_page(q, page_number, pagelen=RESULTS_PER_PAGE)

        # extract titles from the search results that start with the specified alphabet
        titles = [result['title'] for result in results if result['title'].startswith(alphabet)]

        # get the total number of pages
        total_pages = results.pagecount

    return titles, total_pages


# function to parse the year range into start and end years
def parse_year_range(year_range):
    start_year, end_year = year_range.split('-')
    return int(start_year), int(end_year)


# function to fetch papers by a specific year
def get_papers_by_year(year, limit=None):
    with ix.searcher() as searcher:
        query_parser = QueryParser("year", schema=ix.schema)
        q = query_parser.parse(str(year))
        results = searcher.search(q, limit=limit)
        print(f"Results length: {len(results)}")
        # extract paper information from the search results for the specified year
        papers = get_papers(results)
        print(f"Paper length: {len(papers)}")
    return papers


# function to fetch papers within a specific year range
def get_papers_by_year_range(start_year, end_year, limit=None):
    with ix.searcher() as searcher:
        query_parser = QueryParser("year", schema=ix.schema)
        q = query_parser.parse(f"[{start_year} TO {end_year}]")
        results = searcher.search(q, limit=limit)
        # extract paper information from the search results within the specified year range
        papers = get_papers(results)
        print(f"Paper length: {len(papers)}")
    return papers


# function to fetch papers by paper type
def get_papers_by_type(paper_type, limit=None):
    with ix.searcher() as searcher:
        query_parser = QueryParser("type", schema=ix.schema)
        q = query_parser.parse(paper_type)
        results = searcher.search(q, limit=limit)
        # extract paper information from the search results for the specified paper type
        papers = get_papers(results)
        print(f"Paper length: {len(papers)}")
    return papers


# function to fetch paper details for the selected title
def get_paper_details(title):
    with ix.searcher() as searcher:
        query_parser = QueryParser("title", schema=ix.schema)
        q = query_parser.parse(title)
        results = searcher.search(q)

        # extract paper details based on the selected title
        if len(results) > 0:
            paper = results[0]
            paper_details = {
                "title": paper['title'],
                "authors": paper['authors'],
                "year": paper['year'],
                "type": paper['type'],
                "url": paper['url']
            }
        else:
            paper_details = None

    return paper_details


# function to provide autocomplete suggestions
def get_autocomplete_suggestions(query):
    with ix.searcher() as searcher:
        query_parser = QueryParser("title", schema=ix.schema)
        parsed_query = query_parser.parse(query)
        results = searcher.search(parsed_query, limit=10)
        suggestions = [result["title"] for result in results]
    return suggestions
