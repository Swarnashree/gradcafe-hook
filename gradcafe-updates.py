from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
from datetime import datetime
import sys
from notify_run import Notify
import json


def run_program(previous_count):
    content = (requests.get("https://www.thegradcafe.com/survey/index.php?q=Computer+Science&t=a&o=&pp=50")).text

    #print(content.text)

    soup = BeautifulSoup(content,"html.parser")
    print(soup.prettify())

    total_results_count = soup.find_all("section")[0].contents[1].contents[2]
    total_results_count = int((total_results_count.text.split()[6]).replace(',', ''))


    submissions_table = soup.find("table", attrs={"class": ["submission-table"]})
    imp_table_contents = submissions_table.contents[3:]

    new_contents = []

    #print(imp_table_contents[3:])

    for each_row in imp_table_contents:
        new_update = OrderedDict()

        if each_row == '\n':
            continue
        else:
            for each_col in each_row:
                attributes = each_col.attrs["class"]
                #print(attributes)
                if len(each_col.contents) == 0:
                    col_content = ''
                else:
                    col_content = each_col.contents[0]
                #print(col_content)
                if "instcol" in attributes and "tcol1" in attributes:
                    new_update["Instituition"] = col_content
                if "tcol2" in attributes:
                    new_update["Program"] = col_content
                if "tcol3" in attributes:
                    if "other" in attributes:
                        new_update["Some_info"] = col_content
                    elif "rejected" in attributes:
                        new_update["STATUS"] = "REJECTED"
                    else:
                        if "accepted" in attributes:
                            new_update["STATUS"] = "ACCEPTED"
                if "tcol4" in attributes:
                    new_update["student_type"] = col_content
                if "tcol5" in attributes and "datecol" in attributes:
                    new_update["Date"] = col_content
                if "tcol6" in attributes:
                    li_info = col_content.contents[1].contents
                    info = li_info[0] if len(li_info) != 0 else ''
                    new_update["Notes"] = info
        new_contents.append(new_update)
    print(new_contents)
    print(total_results_count)

    return total_results_count, new_contents[0:total_results_count-previous_count+1]


def main(previous_count):
    results_count, content = run_program(int(previous_count))
    if results_count != int(previous_count):
        print(results_count)
        #notify = Notify()
        #notify.send(json.dumps(content))
    else:
        print('no change')
    print('time execute '+str(datetime.now()))

if __name__ == '__main__':
    main(sys.argv[1])




