from flask import Flask
from flask import jsonify
import data
from scraper import ScraperException

app  = Flask(__name__)
data = data.PhoneDataLayer()


def get_results(n=None):
    return u'[' + u', '.join(map(unicode, data.get_entries(n))) + u']'


def get_results_by_area(area_code, n=None):
    d = filter(lambda entry: entry.area_code == area_code, data.get_all_entries())
    if n:
        return u'[' + u', '.join(map(unicode, d[:n])) + u']'
    else:
        return u'[' + u', '.join(map(unicode, d)) + u']'


def create_success_response(entries):
    data = {'status_code':200, 'status_code_desc': 'OK', 'entries': entries}
    response = jsonify(data)
    response.status_code = 200
    return response


def create_failure_response(exception):
    if type(exception) is ScraperException:
        data = {'status_code': exception.status_code, 'status_code_desc': exception.status_code_desc,
                'error_message': exception.error_message}
        response = jsonify(data)
        response.status_code = exception.status_code
    else :
        response = jsonify({'status_code': 500, 'status_code_desc': 'Internal Server Error',
                            'error_message': str(exception)})
        response.status_code = 500

    return response


@app.route('/interview/api/v1.0/results', methods=['GET'])
def results():
    try :
        entries = get_results()
        response = create_success_response(entries)
    except ScraperException as scraper_exception:
        response = create_failure_response(scraper_exception)
    except Exception as exception:
        response = create_failure_response(exception)

    return response


@app.route('/interview/api/v1.0/results/<int:number>', methods=['GET'])
def results_with_limit(number):
    try :
        entries = get_results(number)
        response = create_success_response(entries)
    except ScraperException as scraper_exception:
        response = create_failure_response(scraper_exception)
    except Exception as exception:
        response = create_failure_response(exception)

    return response


@app.route('/interview/api/v1.0/resultsForArea/<string:area_code>', methods=['GET'])
def results_by_area(area_code):
    try :
        entries = get_results_by_area(area_code)
        response = create_success_response(entries)
    except ScraperException as scraper_exception:
        response = create_failure_response(scraper_exception)
    except Exception as exception:
        response = create_failure_response(exception)

    return response


@app.route('/interview/api/v1.0/resultsForArea/<string:area_code>/<int:number>', methods=['GET'])
def results_by_area_with_limit(area_code, number):
    try :
        entries = get_results_by_area(area_code)
        response = create_success_response(entries)
    except ScraperException as scraper_exception:
        response = create_failure_response(scraper_exception)
    except Exception as exception:
        response = create_failure_response(exception)

    return response


if __name__ == '__main__':
    app.run(debug=True)
