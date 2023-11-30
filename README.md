# Search_Engine
Basic search engine for Computer Science related academic papers.

## Dataset
The dataset is obtained from the DBLP computer science bibliography. It provides open bibliographic information on 
major computer science journals and proceedings.

The dataset is an XML file with a corresponding DTD (document type definition) file for validation. You can find 
it [here](https://dblp.uni-trier.de/xml/).

## Structure
* **[static](https://github.com/gloryodeyemi/Search_Engine/tree/main/static):** Folder containing the CSS and JavaScript
codes.

* **[templates](https://github.com/gloryodeyemi/Search_Engine/tree/main/templates):** Folder containing the index.html 
file.

* **[data_parser.py](https://github.com/gloryodeyemi/Search_Engine/blob/main/data_parser.py):** Python script containing
the functions for parsing the XML file and indexing the academic papers.

* **[logic.py](https://github.com/gloryodeyemi/Search_Engine/blob/main/logic.py):** Python script containing the 
functions for search and retrieval.

* **[main.py](https://github.com/gloryodeyemi/Search_Engine/blob/main/main.py)** Python script containing the flask
application to render the search result on the web page.

## Guideline
Run the [data_parser.py](https://github.com/gloryodeyemi/Search_Engine/blob/main/data_parser.py) file first to create an 
index directory for the academic papers, or skip this process and use the index directory already created. You can find 
the index directory [here](https://drive.google.com/file/d/1hos03WxYXfzqRpQL9_ceP8_ioeScxGfr/view?usp=sharing).