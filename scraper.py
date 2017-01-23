from urllib import FancyURLopener
from bs4 import BeautifulSoup

PHONE_SITE = 'http://800notes.com/'


class ValidUAOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)'


class PhoneNumberEntry:
    def __init__(self, phone_number, report_count, comment):
        self.area_code    = phone_number[:3]
        self.phone_number = phone_number
        self.report_count = report_count
        self.comment      = comment.replace('"', '\\"')

    def __unicode__(self):
        skeleton = u'{{ "area_code": "{}", "phone_number": "{}", "report_count": "{}", "comment": "{}" }}'
        return skeleton.format(self.area_code, self.phone_number, self.report_count, self.comment)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return unicode(self).encode('utf-8')


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def entry_parse(self, html):
        num_of_reports = html.find(class_='oos_previewSide').getText()
        number         = html.find(class_='oos_previewHeader').getText()
        comment        = html.find('div', class_='oos_previewBody').getText()
        return PhoneNumberEntry(number, num_of_reports, comment)

    def parse(self):
        try:
            latest_entries = self.soup.find('ul', id='previews').find_all('li', class_='oos_listItem')
        except Exception as exception:
            error_message = 'Exception parsing html.' + '\n' + str(exception)
            raise ScraperException(500, 'Internal Server Error', error_message)

        print latest_entries
        return map(self.entry_parse, latest_entries)


class ScraperException(Exception):
    def __init__(self, status_code, status_code_desc, error_message):
        self.status_code = status_code
        self.status_code_desc = status_code_desc
        self.error_message = error_message


## Main

if __name__ == "__main__":
    parser = Parser(ValidUAOpener().open(PHONE_SITE).read())
    print parser.parse()
