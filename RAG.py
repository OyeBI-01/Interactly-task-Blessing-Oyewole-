from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        # Build Elasticsearch query based on search_term
        query = {
            "query": {
                "multi_match": {
                    "query": search_term,
                    "fields": ["name", "skills", "experience.title"]
                }
            }
        }
        response = es.search(index="resumes", body=query)
        results = response['hits']['hits']
        return render_template('results.html', results=results)
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
