from flask import Flask, request, render_template, jsonify, url_for
import string
import logic

# initialize a Flask application
app = Flask(__name__)


# API endpoint for handling autocomplete suggestions
@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '')
    suggestions = logic.get_autocomplete_suggestions(query)
    return jsonify({'suggestions': suggestions})


# API endpoint for searching academic papers
@app.route('/')
def search_papers():
    query = request.args.get('query', '')  # Get the query from the user
    papers = logic.paper_search(query)
    return render_template('index.html', query=query, papers=papers)


@app.route('/all_papers')
def show_alphabets():
    alphabets = list(string.ascii_uppercase)
    return render_template('index.html', show_alphabets=True, alphabets=alphabets)


@app.route('/titles/<alphabet>')
def show_titles(alphabet):
    # logic to fetch titles starting with the specified alphabet
    selected_alphabet = request.args.get('alphabet', alphabet)  # get the selected alphabet
    current_page = int(request.args.get('page', '1'))  # get the page number
    titles, total_pages = logic.get_titles_by_alphabet_with_pagination(selected_alphabet, current_page)

    # calculate the page range to display in the pagination
    max_pages = 10
    page_range = range(1, min(total_pages, max_pages) + 1)
    # page_range = range(1, total_pages + 1)
    # page_range = []
    # for i in range(1, total_pages + 1):
    #     if i == 1 or i == total_pages or (i >= current_page - max_pages and i <= current_page + max_pages):
    #         page_range.append(i)

    return render_template('index.html', show_titles=True, selected_alphabet=selected_alphabet,
                           titles=titles, total_pages=total_pages, current_page=current_page, page_range=page_range)


@app.route('/paper_details/<title>')
def show_paper_details(title):
    # logic for fetching and rendering paper details
    paper_details = logic.get_paper_details(title)
    return render_template('index.html', show_paper_details=True, paper_details=paper_details)


# endpoint for handling filtering requests
@app.route('/filter_results', methods=['GET', 'POST'])
def filter_results():
    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value')
    filtered_papers = []
    limit = 25

    # logic to fetch filtered results based on the selected filter type and value
    if filter_type == 'all_papers':
        alphabets = list(string.ascii_uppercase)
        return render_template('index.html', show_alphabets=True, alphabets=alphabets)
    elif filter_type == 'year':
        filtered_papers = logic.get_papers_by_year(filter_value, limit)
    elif filter_type == 'year_range':
        start_year, end_year = logic.parse_year_range(filter_value)
        filtered_papers = logic.get_papers_by_year_range(start_year, end_year, limit)
    elif filter_type == 'paper_type':
        filtered_papers = logic.get_papers_by_type(filter_value, limit)

    # render the filtered titles in the index template
    return render_template('index.html', filter_results=True, filtered_papers=filtered_papers,
                           filter_value=filter_value)


if __name__ == '__main__':
    app.run(debug=True)
