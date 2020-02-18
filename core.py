from bs4 import BeautifulSoup
import requests, pprint
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDFS, URIRef, BNode
import rdflib.namespace as RDFnamespace
import urllib.parse
focudata = Namespace("http://focu.io/data#")
focu = Namespace("http://focu.io/schema#")
dbo = Namespace("http://dbpedia.org/ontology/")

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
        df.to_csv('dataset/courses.csv', index=False, encoding='utf-8')


    def create_graph_schema(self):
        """Creating the basic schema of the graph. Adding the classes, properties and subclasses required
        for the university courses and students"""
        g = Graph();
        g.bind('focudata', focudata)
        g.bind('focu', focu)
        g.bind('dbo', dbo)
        g.bind('foaf',RDFnamespace.FOAF)


        ##Classes
        #Person Class
        g.add((RDFnamespace.FOAF.Person,RDFnamespace.RDF.type,RDFnamespace.RDFS.Class))
        #Organization Class
        g.add((RDFnamespace.FOAF.Organization,RDFnamespace.RDF.type,RDFnamespace.RDFS.Class))

        #Student Class
        g.add((focu.Student,RDFnamespace.RDF.type,RDFnamespace.RDFS.Class))
        g.add((focu.Student,RDFnamespace.RDFS.subClassOf,RDFnamespace.FOAF.Person))
        g.add((focu.Student,RDFnamespace.RDFS.label,Literal("StudentClass")))
        g.add((focu.Student,RDFnamespace.RDFS.comment,Literal("This is a Student Class")))

        #Course Class
        g.add((focu.Course, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.Course, RDFnamespace.RDFS.label, Literal("University Courses")))
        g.add((focu.Course, RDFnamespace.RDFS.comment, Literal("This is a Course Class")))

        #Topic Class
        g.add((focu.Topic, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.Topic, RDFnamespace.RDFS.label, Literal("Course Topics")))
        g.add((focu.Topic, RDFnamespace.RDFS.comment, Literal("This is a Course Topic Class")))

        # University Class
        g.add((focu.University, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.University, RDFnamespace.RDFS.subClassOf, RDFnamespace.FOAF.Organization))
        g.add((focu.University, RDFnamespace.RDFS.label, Literal("Univeristy")))

        # Course Grade Class
        g.add((focu.Course_Grade, RDFnamespace.RDF.type, RDFnamespace.RDFS.Class))
        g.add((focu.Course_Grade, RDFnamespace.RDFS.label, Literal("Course Grades")))
        g.add((focu.Course_Grade, RDFnamespace.RDFS.comment, Literal("Grades for Courses")))


        ##Properties

        #Course Name
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

        #Completed Courses
        g.add((focu.completed_course, RDFnamespace.RDF.type, RDFnamespace.RDF.Property))
        g.add((focu.completed_course, RDFnamespace.RDFS.label, Literal("Completed Courses by the Student")))
        g.add((focu.completed_course, RDFnamespace.RDFS.comment, Literal("Completed Courses by the Student")))
        g.add((focu.completed_course, RDFnamespace.RDFS.domain, focu.Student))
        g.add((focu.completed_course, RDFnamespace.RDFS.range, focu.Course_Grade))


        g.serialize(format = 'turtle',destination='knowledge_base/ab.ttl')



    def create_graph_from_csv(self):
        """Creating rdf graph from the Dataset"""

        ##Defining the graph
        g = Graph()
        g.parse('knowledge_base/ab.ttl', format='n3')


        ##Adding Courses to the Graph
        df = pd.read_csv('dataset/courses.csv')
        self.courseSubject = df['Course Subject']
        self.courseName = df['Course Name']
        self.courseDescription = df['Course Description']
        self.courseNumber = df['Course Number']


        for (course_num,course_subject, course_name, course_desc) in zip(self.courseNumber, self.courseSubject, self.courseName, self.courseDescription):
            course_name_data = urllib.parse.quote_plus(course_name)
            g.add((focudata[course_name_data], RDFnamespace.RDF.type, focu.Course))
            g.add((focudata.term(course_name_data), focu.course_name, Literal(course_name)))
            g.add((focudata.term(course_name_data), focu.course_subject, Literal(course_subject)))
            g.add((focudata.term(course_name_data), focu.course_number, Literal(course_num)))
            g.add((focudata.term(course_name_data), focu.course_description, Literal(course_desc)))
            g.add((focudata.term(course_name_data), RDFS.seeAlso, Literal('Nothing to see ')))


        ###Adding Student information to the Graph
        df_stu = pd.read_csv('dataset/student_dataset.csv')
        student_first_name = df_stu['Student First Name']
        student_last_name = df_stu['Student Last Name']
        student_ID = df_stu['ID Number']
        student_email = df_stu['Email']
        some_courses_from_list = self.courseName[0:30]

        for (student_first_name,student_last_name, student_ID, student_email,courses) in zip(student_first_name,student_last_name, student_ID, student_email,some_courses_from_list):
            student_name = urllib.parse.quote_plus(student_first_name+" "+student_last_name)
            course_name_data = urllib.parse.quote_plus(courses)
            g.add((focudata[student_name], RDFnamespace.RDF.type, focu.Student))
            g.add((focudata.term(student_name), RDFnamespace.FOAF.firstName, Literal(student_first_name)))
            g.add((focudata.term(student_name), RDFnamespace.FOAF.lastName, Literal(student_last_name)))
            g.add((focudata.term(student_name), focu.student_id, Literal(student_ID)))
            g.add((focudata.term(student_name), RDFnamespace.FOAF.mbox, Literal(student_email)))
            g.add((focudata.term(student_name), focu.completed_course, focudata[course_name_data]))




        ##making a ttl from the graph
        g.serialize(destination='knowledge_base/ab.ttl',format='ttl')

        # for s, p, o in g.triples((None, focu.course_description, None)):
        #     print( "%s is a %s" % (s, o))



