import csv
import random
import re
import string
import time
import urllib.parse

import pandas as pd
import rdflib.namespace as RDFnamespace
import requests
from bs4 import BeautifulSoup
from rdflib import Graph, Literal, Namespace

focudata = Namespace("http://focu.io/data#")
focu = Namespace("http://focu.io/schema#")
dbo = Namespace("http://dbpedia.org/ontology/")
dbpedia = Namespace("http://dbpedia.org/resource/")
g = Graph()
g.bind('focudata', focudata)
g.bind('focu', focu)
g.bind('dbo', dbo)
g.bind('dbpedia', dbpedia)
g.bind('foaf', RDFnamespace.FOAF)
g.bind('owl', RDFnamespace.OWL)


class core:
    courseSubject = []
    courseName = []
    courseNumber = []
    courseDescription = []
    seeAlso = []

    def __init__(self):
        pass

    def get_course_html_to_csv(self):
        URL = 'http://www.concordia.ca/academics/graduate/calendar/current/fofa/dart-mdes.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='wysiwyg parbase section')
        for i in range(0, len(results)):
            quoteTags = results[i].find_all('span', class_='large-text')
            if i == 4:
                count = 0
                for quoteTag in quoteTags:
                    if count > 1:
                        s = quoteTag.text.split("\n", 1)
                        if quoteTag.find('b') is None:
                            continue
                        course = quoteTag.find('b').text
                        x = course.split(' ', 2)
                        if len(x) >= 3:
                            self.courseSubject.append(x[0])
                            x[1] = x[1][0:4]
                            self.courseNumber.append(x[1])
                            self.courseName.append(x[2])
                            if len(s) > 1:
                                self.courseDescription.append(s[1])
                            else:
                                self.courseDescription.append("Description not available")
                            self.seeAlso.append(URL)
                        else:
                            continue
                    count = count + 1
        df = pd.DataFrame(
            {'Course Subject': self.courseSubject, 'Course Number': self.courseNumber, 'Course Name': self.courseName,
             'Course Description': self.courseDescription, 'See Also': self.seeAlso})
        df.to_csv('dataset/courses.csv', index=False, encoding='utf-8')

    def create_graph_schema(self):
        """Creating the basic schema of the graph. Adding the classes, properties and subclasses required
        for the university courses and students"""

        ##Classes
        # Person Class
        g.add((RDFnamespace.FOAF.Person, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        # Organization Class
        g.add((RDFnamespace.FOAF.Organization, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))

        # Student Class
        g.add((focu.Student, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.Student, RDFnamespace.RDFS.subClassOf, RDFnamespace.FOAF.Person))
        g.add((focu.Student, RDFnamespace.RDFS.label, Literal("StudentClass")))
        g.add((focu.Student, RDFnamespace.RDFS.comment, Literal("This is a Student Class")))

        # Course Class
        g.add((focu.Course, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.Course, RDFnamespace.RDFS.label, Literal("University Courses")))
        g.add((focu.Course, RDFnamespace.RDFS.comment, Literal("This is a Course Class")))

        # Topic Class
        g.add((focu.Topic, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.Topic, RDFnamespace.RDFS.label, Literal("Course Topic")))
        g.add((focu.Topic, RDFnamespace.RDFS.comment, Literal("Topic extracted for a given course")))

        # University Class
        g.add((focu.University, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.University, RDFnamespace.RDFS.subClassOf, RDFnamespace.FOAF.Organization))
        g.add((focu.University, RDFnamespace.RDFS.label, Literal("Univeristy")))

        ##Properties

        # Course Name
        g.add((focu.course_name, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.course_name, RDFnamespace.RDFS.label, Literal("Course Name")))
        g.add((focu.course_name, RDFnamespace.RDFS.comment, Literal("Course Name")))
        g.add((focu.course_name, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.course_name, RDFnamespace.RDFS.range, RDFnamespace.XSD.string))

        # Course Subject
        g.add((focu.course_subject, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.course_subject, RDFnamespace.RDFS.label, Literal("Course Subject")))
        g.add((focu.course_subject, RDFnamespace.RDFS.comment, Literal("Course Subject")))
        g.add((focu.course_subject, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.course_subject, RDFnamespace.RDFS.range, RDFnamespace.XSD.string))

        # Course Number
        g.add((focu.course_number, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.course_number, RDFnamespace.RDFS.label, Literal("Course Number")))
        g.add((focu.course_number, RDFnamespace.RDFS.comment, Literal("Course Number")))
        g.add((focu.course_number, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.course_number, RDFnamespace.RDFS.range, RDFnamespace.XSD.integer))

        # Course Description
        g.add((focu.course_description, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.course_description, RDFnamespace.RDFS.label, Literal("Course Description")))
        g.add((focu.course_description, RDFnamespace.RDFS.comment, Literal("Course Description")))
        g.add((focu.course_description, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.course_description, RDFnamespace.RDFS.range, RDFnamespace.XSD.string))

        # Student ID
        g.add((focu.student_id, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.student_id, RDFnamespace.RDFS.label, Literal("Student ID")))
        g.add((focu.student_id, RDFnamespace.RDFS.comment, Literal("Student ID")))
        g.add((focu.student_id, RDFnamespace.RDFS.domain, focu.Student))
        g.add((focu.student_id, RDFnamespace.RDFS.range, RDFnamespace.XSD.integer))

        # Graded Courses
        g.add((focu.graded_courses, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.graded_courses, RDFnamespace.RDFS.label, Literal("grade for course", lang="en")))
        g.add((focu.graded_courses, RDFnamespace.RDFS.comment, Literal("Course graded for a student")))
        g.add((focu.graded_courses, RDFnamespace.RDFS.domain, focu.Student))
        g.add((focu.graded_courses, RDFnamespace.RDFS.range, focu.Course))

        # Subject Contains Topics
        g.add((focu.contains, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.contains, RDFnamespace.RDFS.label, Literal("extracted topics", lang="en")))
        g.add((focu.contains, RDFnamespace.RDFS.comment, Literal("Topics extracted from course description")))
        g.add((focu.contains, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.contains, RDFnamespace.RDFS.range, focu.Topic))

        # Topics from Courses
        g.add((focu.containInverse, RDFnamespace.OWL.inverseOf, focu.contains))
        g.add((focu.containInverse, RDFnamespace.RDFS.label, Literal("extracted courses", lang="en")))
        g.add((focu.containInverse, RDFnamespace.RDFS.comment, Literal("Courses extracted from Topics")))
        g.add((focu.containInverse, RDFnamespace.RDFS.domain, focu.Topic))
        g.add((focu.containInverse, RDFnamespace.RDFS.range, focu.Course))

        # Course Term
        g.add((focu.course_term, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.course_term, RDFnamespace.RDFS.label, Literal("course term", lang="en")))
        g.add((focu.course_term, RDFnamespace.RDFS.comment, Literal("The term in which the given course was taken")))
        g.add((focu.course_term, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.course_term, RDFnamespace.RDFS.range, RDFnamespace.XSD.string))

        # Course Grade
        g.add((focu.course_grade, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.course_grade, RDFnamespace.RDFS.label, Literal("course grade", lang="en")))
        g.add((focu.course_grade, RDFnamespace.RDFS.comment, Literal("The grade received for a course")))
        g.add((focu.course_grade, RDFnamespace.RDFS.domain, focu.Course))
        g.add((focu.course_grade, RDFnamespace.RDFS.range, RDFnamespace.XSD.string))

        g.serialize(format='turtle', destination='knowledge_base/schema.ttl')

    def create_graph_from_csv(self):
        """Creating rdf graph from the Dataset, DBpedia"""

        ##Defining the graph
        g.parse('knowledge_base/knowledgeBase_kam_karo1.ttl', format='ttl')

        ##Adding Courses to the Graph
        df = pd.read_csv('dataset/sahil_da_samaan.csv')
        self.courseSubject = df['Course Subject']
        self.courseName = df['Course Name']
        self.courseDescription = df['Course Description']
        self.courseNumber = df['Course Number']
        self.seeAlso = df['See Also']
        for (course_num, course_subject, course_name, course_desc, see_also) in zip(self.courseNumber,
                                                                                    self.courseSubject,
                                                                                    self.courseName,
                                                                                    self.courseDescription,
                                                                                    self.seeAlso):

            g.serialize(destination='knowledge_base/knowledgeBase_kam_karo1.ttl', format='ttl')

            course_name_data = str(course_name).replace("+", "_")
            course_name_data = course_name_data.replace(" ", "_")
            course_name_data = course_name_data.replace("(*)", "")
            course_name_data.translate(str.maketrans('', '', string.punctuation))
            g.add((focudata[course_name_data], RDFnamespace.RDF.type, focu.Course))
            g.add((focudata.term(course_name_data), focu.course_name, Literal(course_name)))
            g.add((focudata.term(course_name_data), focu.course_subject, Literal(course_subject)))
            g.add((focudata.term(course_name_data), focu.course_number, Literal(course_num)))
            g.add((focudata.term(course_name_data), focu.course_description, Literal(course_desc)))
            g.add((focudata.term(course_name_data), RDFnamespace.RDFS.seeAlso, Literal(see_also)))


            """Getting topics from DBpedia from course descriptions."""
            url = urllib.parse.quote(str(course_desc))
            url = 'https://api.dbpedia-spotlight.org/en/annotate?text=' + url
            responseCounter = 0
            while responseCounter < 1:
                if course_desc == "No description available" or course_desc == "Description not available" or bool(re.match("\s+",course_desc)):
                    break
                response = requests.get(url, headers={'accept': 'application/json'})
                if response.status_code == 200:
                    data = response.json()
                    key = "Resources"
                    print(course_desc)
                    if key in data.keys():
                        resources = data["Resources"]
                        for res in resources:
                            if res is None:
                                continue
                            else:
                                topic = res["@URI"]
                                englishName = res["@surfaceForm"]
                                topic = str(topic).replace("http://dbpedia.org/resource/", "")
                                print(res["@URI"])
                                # Adding topic to the course
                                g.add((focudata.term(course_name_data), focu.contains, focudata[topic]))
                                # Adding the topic information
                                g.add((focudata[topic], RDFnamespace.RDF.type, focu.Topic))
                                g.add((focudata[topic], focu.containInverse, focudata.term(course_name_data)))
                                g.add((focudata[topic], RDFnamespace.FOAF.name, Literal(englishName)))
                                g.add((focudata[topic], RDFnamespace.OWL.sameAs, dbpedia.term(topic)))
                    break
                time.sleep(5)
                print('trying')

        # making a ttl from the graph
        g.serialize(destination='knowledge_base/knowledgeBase_kam_karo1.ttl', format='ttl')

    def add_student_data_to_graph(self):
        """Adding Student information to the Graph"""

        # Course Data
        df = pd.read_csv('dataset/courses.csv')
        self.courseSubject = df['Course Subject']
        self.courseName = df['Course Name']
        self.courseDescription = df['Course Description']
        self.courseNumber = df['Course Number']

        # Student Data
        df_stu = pd.read_csv('dataset/student_dataset.csv')
        student_first_name = df_stu['Student First Name']
        student_last_name = df_stu['Student Last Name']
        student_ID = df_stu['ID Number']
        student_email = df_stu['Email']

        for (student_first_name, student_last_name, student_ID, student_email) in zip(student_first_name,
                                                                                      student_last_name,
                                                                                      student_ID,
                                                                                      student_email
                                                                                      ):
            student_name = urllib.parse.quote_plus(student_first_name + "_" + student_last_name)
            grades = ["A+", "A-", "A", "B+", "B-", "B", "C", "F"]
            terms = ["Fall_2018", "Summer_2018", "Winter_2018", "Fall_2019", "Summer_2019", "Winter_2019",
                     "Winter_2020"]
            number_of_courses = random.randint(5, 15)

            g.add((focudata[student_name], RDFnamespace.RDF.type, focu.Student))
            g.add((focudata.term(student_name), RDFnamespace.FOAF.firstName, Literal(student_first_name)))
            g.add((focudata.term(student_name), RDFnamespace.FOAF.lastName, Literal(student_last_name)))
            g.add((focudata.term(student_name), focu.student_id, Literal(student_ID)))
            g.add((focudata.term(student_name), RDFnamespace.FOAF.mbox, Literal(student_email)))

            # sampling some number of courses from courselist
            some_courses_from_list = random.sample(list(self.courseName), number_of_courses)
            for course in some_courses_from_list:
                course_term = random.choice(terms)
                course = str(course)
                course_name_data = course.replace("+", "_")
                course_name_data = course_name_data.replace(" ", "_")
                course_name_data = course_name_data.replace("(*)", "")
                course_name_data.translate(str.maketrans('', '', string.punctuation))
                graded_course_name = course_name_data.strip() + "_" + course_term + "_" + str(student_ID)
                g.add((focudata.term(student_name), focu.graded_courses, focudata[graded_course_name.strip()]))

                # Adding focudata for enrolled courses
                g.add((focudata[graded_course_name], RDFnamespace.RDF.type, focu.Course))
                g.add((focudata[graded_course_name], focu.Course, focudata[course_name_data]))
                g.add((focudata[graded_course_name], focu.course_grade, Literal(random.choice(grades))))
                g.add((focudata[graded_course_name], focu.course_term, Literal(course_term)))

        g.serialize(destination='knowledge_base/knowledgeBase.nt', format='nt')
