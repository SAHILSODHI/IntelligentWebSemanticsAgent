from bs4 import BeautifulSoup
import requests, pprint
import re
import pandas as pd

class Core:
    def __init__(self):
        print("Hello")

    def get_Html(self):
        URL = 'https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='wysiwyg parbase section')
        for i in range(0, len(results)):
            quoteTags = results[i].find_all('span', class_='large-text')
            if i == 2:
                count = 0
                courseSubject = []
                courseName = []
                courseNumber = []
                courseDescription = []
                for quoteTag in quoteTags:
                    if count > 1:
                        s = quoteTag.text.split("\n", 1)
                        if len(s) > 1:
                            courseDescription.append(s[1])
                        else:
                            courseDescription.append("Description not available")
                        course = quoteTag.find('b').text
                        x = course.split(' ', 2)
                        courseSubject.append(x[0])
                        x[1] = x[1][0:4]
                        courseNumber.append(x[1])
                        courseName.append(x[2])
                    count = count + 1
        df = pd.DataFrame({'Course Subject': courseSubject, 'Course Number': courseNumber, 'Course Name': courseName,
                           'Course Description': courseDescription})
        df.to_csv('courses.csv', index=False, encoding='utf-8')

p1 = Core()
p1.get_Html()