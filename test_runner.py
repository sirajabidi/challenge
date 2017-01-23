import ast
import requests
from datetime import datetime
from app import data


SCRAPER_SERVICE_BASE_URL = 'http://localhost:5000'
STATUS_CODE_OK = 200


def test_api_v1_0_get_results():
    test_api = '/interview/api/v1.0/results'
    url = SCRAPER_SERVICE_BASE_URL + test_api
    response = requests.get(url)

    try:
        if response.status_code == STATUS_CODE_OK:
            validate_schema(response)
        else:
            raise Exception('Error processing : ' + test_api)

    except Exception as exception:
        print 'FAIL : ' + test_api
        print 'ERROR : ' + str(exception)
    else:
        print 'PASS : ' + test_api


def test_api_v1_0_get_results_by_quantity():
    test_api = '/interview/api/v1.0/results/40'
    url = SCRAPER_SERVICE_BASE_URL + test_api
    response = requests.get(url)

    try:
        if response.status_code == STATUS_CODE_OK:
            validate_schema(response)
        else:
            raise Exception('Error processing : ' + test_api)

    except Exception as exception:
        print 'FAIL : ' + test_api
        print 'ERROR : ' + str(exception)
    else:
        print 'PASS : ' + test_api


def test_api_v1_0_get_results_by_area_code():
    test_api = '/interview/api/v1.0/resultsForArea/320'
    url = SCRAPER_SERVICE_BASE_URL + test_api
    response = requests.get(url)

    try:
        if response.status_code == STATUS_CODE_OK:
            validate_schema(response)
        else:
            raise Exception('Error processing : ' + test_api)

    except Exception as exception:
        print 'FAIL : ' + test_api
        print 'ERROR : ' + str(exception)
    else:
        print 'PASS : ' + test_api


def test_scraped_data_getting_saved():
    star_time_stamp = datetime.now()
    test_api = '/interview/api/v1.0/results'
    url = SCRAPER_SERVICE_BASE_URL + test_api
    response = requests.get(url)

    try:
        if response.status_code == STATUS_CODE_OK:
            validate_db_time_stamps_for_scraped_data(response, star_time_stamp)
        else:
            raise Exception('Error processing : ' + test_api)

    except Exception as exception:
        print 'FAIL : Scraped data getting stored in database'
        print 'ERROR : ' + str(exception)
    else:
        print 'PASS : Scraped data getting stored in database'


# test to validate the response schema in case of wring area code. Response schema should be correct with no element in
# entries list.
def test_api_v1_0_get_results_by_area_code_for_wrong_area_code():
    test_api = '/interview/api/v1.0/resultsForArea/x+z'
    url = SCRAPER_SERVICE_BASE_URL + test_api
    response = requests.get(url)

    try:
        if response.status_code == STATUS_CODE_OK:
            validate_schema(response)
        else:
            raise Exception('Error processing : ' + test_api)

    except Exception as exception:
        print 'FAIL : ' + test_api
        print 'ERROR : ' + str(exception)


def validate_db_time_stamps_for_scraped_data(response, star_time_stamp):
    response_json = response.json()
    entries_unicode = response_json['entries']
    entries = ast.literal_eval(entries_unicode)
    all_phone_numbers = [entry['phone_number'] for entry in entries]
    result = data.get_time_stamp_for_phone_numbers(all_phone_numbers)

    if len(result) != len(all_phone_numbers) :
        raise Exception('Not all Scraped Phone Numbers found in DB.')

    for phone_number in result:
        ts = result[phone_number]
        if ts < star_time_stamp:
            raise Exception('Time Stamp for ' + phone_number + ' has not been updated in DB.')


def validate_schema(response):
    print 'Validating Response Schema'
    response_json = response.json()

    if 'status_code' not in response_json:
        raise Exception('Invalid Schema. status_code not found in response json')

    if 'status_code_desc' not in response_json:
        raise Exception('Invalid Schema. status_code_desc not found in response json')

    if 'entries' not in response_json:
        raise Exception('Invalid Schema. entries not found in response json')

    entries_unicode = response_json['entries']
    entries = ast.literal_eval(entries_unicode)

    if type(entries) is not list:
        raise Exception('Invalid Schema. entries key should be of type list.')

    if len(entries) > 0:
        for entry in entries:
            if type(entry) is not dict:
                raise Exception('Invalid Schema. All entry in entries should be of type dict.')
            for key in entry:
                if key not in ['area_code', 'phone_number', 'comment', 'report_count']:
                    raise Exception('Invalid Schema. ' + key + ' is not a valid key type for entry.')

    print 'Response Schema Valid.'


if __name__ == '__main__':

    test_api_v1_0_get_results()

    test_api_v1_0_get_results_by_quantity()

    test_api_v1_0_get_results_by_area_code()

    test_scraped_data_getting_saved()

    test_api_v1_0_get_results_by_area_code_for_wrong_area_code()


