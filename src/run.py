#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from QStandings import Standings

if __name__ == "__main__":

    contest_id = str(input("Please enter Quera Contest ID : "))

    url = "https://quera.ir/course/assignments/" + contest_id + "/scoreboard/"

    print("\n[-] Collect data from '{}' please wait...\n".format(url))

    st = Standings(contest_id)

    print("[+] Problem Number: {}\n".format(st.problem_number))

    print("[+] Page Number: {}\n".format(st.page_number))

    print("[+] Submission Status: \n")

    st.show()

    show = input("\nDo you want to show bar chart of submission status? (Y|N) : ")

    if show == 'Y' or show == 'y':

        print("\n[-] Showing bar chart, please wait...")

        st.show_barcharts()

    else:
        exit()
