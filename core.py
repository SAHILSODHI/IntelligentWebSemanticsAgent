from bs4 import BeautifulSoup
import requests, pprint
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDFS
import rdflib.namespace as RDFnamespace

class core:
    courseSubject = []
    courseName = []
    courseNumber = []
    courseDescription = []

    def __init__(self):
        pass

    def get_course_html_to_csv(self):
        URL = 'https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='wysiwyg parbase section')
        for i in range(0, len(results)):
            quoteTags = results[i].find_all('span', class_='large-text')
            if i == 2:
                count = 0
                for quoteTag in quoteTags:
                    if count > 1:
                        s = quoteTag.text.split("\n", 1)
                        if len(s) > 1:
                            self.courseDescription.append(s[1])
                        else:
                            self.courseDescription.append("Description not available")
                        course = quoteTag.find('b').text
                        x = course.split(' ', 2)
                        self.courseSubject.append(x[0])
                        x[1] = x[1][0:4]
                        self.courseNumber.append(x[1])
                        self.courseName.append(x[2])
                    count = count + 1
        df = pd.DataFrame({'Course Subject': self.courseSubject, 'Course Number': self.courseNumber, 'Course Name': self.courseName,
                           'Course Description': self.courseDescription})
        df.to_csv('data/courses.csv', index=False, encoding='utf-8')


    def create_graph_from_csv(self):
        """Creating rdf graph from the Dataset"""
        FOCUDATA = Namespace("http://focu.io/data#")
        FOCU = Namespace("http://focu.io/schema#")
        DBO = Namespace("http://dbpedia.org/ontology/")

        g = Graph()
        g.parse('kb.ttl', format='n3')

        df = pd.read_csv('data/courses.csv')
        self.courseSubject = df['Course Subject']
        self.courseName = df['Course Name']
        self.courseDescription = df['Course Description']
        self.courseNumber = df['Course Number']

        for (course_num,course_subject, course_name, course_desc) in zip(self.courseNumber, self.courseSubject,self.courseName, self.courseDescription):
            g.add((FOCUDATA.course_name, RDFnamespace.RDF.type, FOCU.Course))
            g.add((FOCUDATA.course_name, FOCU.course_subject, FOCU.course_subject))
            g.add((FOCUDATA.course_name, FOCU.course_number, FOCU.course_num))
            g.add((FOCUDATA.course_name, FOCU.course_description, FOCU.course_desc))
            g.add((FOCUDATA.course_name, RDFS.seeAlso, Literal('Nothing to see ')))
            pprint.pprint(g.serialize(format='turtle'))

        # g.add((bob, RDFnamespace.RDF.type, RDFnamespace.FOAF.Person))
        # g.add((bob, RDFnamespace.FOAF.name, name))
        # g.add((bob, FOAF.knows, linda))
        # g.add((linda, RDF.type, FOAF.Person))
        # g.add((linda, FOAF.name, Literal('Linda')))
        #
        # print(g.serialize(format='turtle'))


