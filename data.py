import sqlite3 as lite
import scraper
from scraper import ScraperException

class PhoneDataLayer:
    def __init__(self, db='numbers.db'):
        con = None
        try:
            con = lite.connect(db)
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS Numbers")
                cur.execute("CREATE TABLE Numbers(number TEXT primary key not null, count INT, comment TEXT, date TEXT)")
        except lite.Error, e:
            raise e
        finally:
            if con:
                con.close()


    def insert_entries(self, entries):
        con = lite.connect('numbers.db')
        with con:
            cur = con.cursor()
            for entry in entries:
                cur.execute('INSERT OR REPLACE INTO Numbers(number, count, comment, date) VALUES (?, ?, ?, CURRENT_TIMESTAMP);', [entry.phone_number, entry.report_count, entry.comment])
        con.close()


    def get_time_stamp_for_phone_numbers(self, phone_numbers):
        con = lite.connect('numbers.db')
        rows = None
        with con:
            cur = con.cursor()
            sql_query = 'SELECT number, date from Numbers where number IN (' + ','.join((str(ph) for ph in phone_numbers)) + ')'

            cur.execute(sql_query)
            rows = cur.fetchall()

        results = {}
        for row in rows:
            results[row[0]] = row[1]

        con.close()
        return results


    def get_all_entries(self):
        try:
            web = scraper.ValidUAOpener().open(scraper.PHONE_SITE)
            html_content = web.read()
        except Exception as exception:
            error_message = 'Exception opening site : ' + scraper.PHONE_SITE + '\n' + str(exception)
            raise ScraperException(500, 'Internal Server Error', error_message)

        parser  = scraper.Parser(html_content)
        entries = parser.parse()
        self.insert_entries(entries)

        con  = lite.connect('numbers.db')
        rows = None
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Numbers ORDER BY date;')
            rows = cur.fetchall()

        entries = []
        for row in rows:
            entries[len(entries):] = [scraper.PhoneNumberEntry(row[0], row[1], row[2])]

        con.close()
        return entries


    def get_db_entries(self, n=60):
        con  = lite.connect('numbers.db')
        rows = None
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Numbers ORDER BY date LIMIT {}'.format(n))
            rows = cur.fetchall()

        entries = []
        for row in rows:
            entries[len(entries):] = [scraper.PhoneNumberEntry(row[0], row[1], row[2])]

        con.close()
        return entries


    def get_entries(self, n=None):
        try:
            web = scraper.ValidUAOpener().open(scraper.PHONE_SITE)
            html_content = web.read()
        except Exception as exception:
            error_message = 'Exception opening site : ' + scraper.PHONE_SITE + '\n' + str(exception)
            raise ScraperException(500, 'Internal Server Error', error_message)

        parser  = scraper.Parser(html_content)

        entries = parser.parse()
        self.insert_entries(entries)

        if n is None:
            return entries
        elif n < len(entries):
            return entries[:n]
        else:
            return self.get_db_entries(n)

