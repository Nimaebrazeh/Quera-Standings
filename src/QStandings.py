#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup

PY_VER = sys.version_info[0]
if PY_VER > 2:
    import urllib as urllib2
else:
    from urllib2 import urlopen


class Standings:

    def __init__(self, contest_id):

        self.contest_id = contest_id

        self.contest_href = "/course/assignments/" + contest_id + "/scoreboard/"

        self.contest_url = "https://quera.ir/course/assignments/" + contest_id + "/scoreboard/"

        self.soup = None

        self.accept_style = ''

        self.problem_number = 0

        self.page_number = 0

        self.accepted_submissions = []

        self.run()


    def run(self):

        self.check_link()

        self.set_html_data(1)

        self.set_accept_style()

        self.set_problem_number()

        self.set_submission_page_number()

        self.set_accepted_submissions()


    def check_link(self):

        r = requests.head(self.contest_url)

        if r.status_code != 200:
            raise Exception("contest link is not valid!")


    def show(self):

        for i in range(0, len(self.accepted_submissions)):
            print("    [#] Problem " + str(i + 1) + " : " + str(self.accepted_submissions[i]) + " Solved")


    def show_barcharts(self):

        import matplotlib.pyplot as plt

        plt.bar(range(1, self.problem_number + 1), self.accepted_submissions, align = 'center')

        plt.xlabel('Problem')

        plt.ylabel('Accepted Submissions')

        plt.title('Submission Status')

        plt.tight_layout()

        plt.show()


    def set_html_data(self, page_index):

        url = self.get_url_by_page(page_index)

        if PY_VER > 2:
            html_page = urllib2.request.urlopen(url)
        else:
            html_page = urlopen(url)

        self.soup = BeautifulSoup(html_page, 'html.parser')


    def get_html_data(self, page_index):

        url = self.get_url_by_page(page_index)

        html_page = urllib2.urlopen(url)

        soup = BeautifulSoup(html_page, 'html.parser')

        return soup


    def set_accept_style(self):

        for row in self.soup.findAll('table')[0].tbody.findAll('tr'):
            try:
                if len(row.findAll('td', attrs = {'style' : 'color: #002e07;background-color: #c1eebe;'})) > 0:
                    self.accept_style = 'color: #002e07;background-color: #c1eebe;'
                    break

                find_string = '''background-color: rgb(162,208,153) !important;
                    color: rgb(0,0,0) !important;'''

                if len(row.findAll('td', attrs = {'style' : find_string})) > 0:
                    self.accept_style = find_string
                    break

            except:
                pass



    def get_url_by_page(self, page_index):

        course_url = self.contest_url + str(page_index)

        return course_url


    def set_problem_number(self):

        self.problem_number = len(self.soup.findAll('table')[0].thead.findAll('tr')[1].findAll('th'))

        self.accepted_submissions = [ 0 for i in range(0, self.problem_number) ]


    def get_problem_number(self):

        return self.problem_number


    def set_submission_page_number(self):

        page_index = 1

        while True:
            page_href = self.contest_href + str(page_index) + "/"

            if self.soup.find('a', attrs = {'href': page_href}) == None:
                break

            page_index += 1

        self.page_number = page_index - 1


    def get_submission_page_number(self):

        return self.page_number


    def set_accepted_submissions(self):

        for page_index in range (0, self.page_number):
            self.set_html_data(page_index + 1)

            for problem_index in range(0, self.problem_number):
                for row in self.soup.findAll('table')[0].tbody.findAll('tr'):

                    col = row.findAll('td')[problem_index + 2]

                    if col.attrs == {'style': self.accept_style}:
                        self.accepted_submissions[problem_index] += 1


    def get_accepted_submissions(self):

        return self.accepted_submissions
