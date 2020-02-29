import rdflib

g = rdflib.Graph()
result = g.parse("ab.ttl", format='n3')

s = g.serialize(format='n3')
print()
print()
# queryOne = g.query("""SELECT (count(?s) as ?count)
#                     WHERE
#                     {
#                       ?s ?p ?o
#                     }""")
#
# for row in queryOne:
#     print('Total number of triples in the KB: ' + row[0])
# print()
#
#
# queryTwo = g.query("""
#                     PREFIX focu: <http://focu.io/schema#>
#                     SELECT DISTINCT(count(?s) as ?NumberOfStudents) (count(?c) as ?NumberOfCourses)
#                     WHERE
#                     {
#                         {?c a focu:Course.}
#                         UNION
#                         {?s a focu:Student.}
#                     }""")
# print()
# for row in queryTwo:
#     print('Count of students: ' + row[0])
#     print('Number of Courses: ' + row[1])
# #
# queryThree = g.query("""
#                     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#                     Prefix focu: <http://focu.io/schema#>
#                     PREFIX focudata: <http://focu.io/data#>
#                     SELECT  ?topicLink ?topicName
#                     WHERE {
#                       <http://focu.io/data#Parallel_Programming_%28%2A%29> focu:contains ?topicLink.
#                       ?topicLink foaf:name ?topicName
#                     }""")
#
# print()
# print()
# print('For the given course, list all covered topics using their (English) labels and their link to DBpedia: ')
# print()
# for row in queryThree:
#     x = row[0]
#     x = x.replace('http://focu.io/data#', '')
#     print('Topic Link: ' + x)
#     print('Topic English Name: ' + row[1])
#     print()
# #
# queryFour = g.query("""
#                     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#                     Prefix focu: <http://focu.io/schema#>
#                     PREFIX focudata: <http://focu.io/data#>
#                     SELECT  ?courseName ?courseGrade
#                     WHERE {
#                         focudata:Akeem_Cotton focu:graded_courses ?course .
#                         ?course focu:Course ?courseName .
#                         ?course focu:course_grade ?courseGrade .
#                         FILTER((?courseGrade) != '') .
#                     }""")
# print()
# print()
# print('For a given student, list all courses this student completed, together with the grade')
# print()
# for row in queryFour:
#     x = row[0]
#     x = x.replace('http://focu.io/data#', '')
#     print('Course Name: ' + x)
#     print('Course Grade: ' + row[1])
#     print()
#
#
# queryFive = g.query("""
#                     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#                     Prefix focu: <http://focu.io/schema#>
#                     PREFIX focudata: <http://focu.io/data#>
#                     PREFIX dbpedia: <http://dbpedia.org/resource/>
#                     SELECT ?studentName
#                     WHERE {
#                          <http://focu.io/data#http://dbpedia.org/resource/Cloud_computing> focu:containInverse ?course .
#                          ?studentSubjectID focu:Course ?course .
#                          ?studentName focu:graded_courses ?studentSubjectID .
#                          ?studentSubjectID focu:course_grade ?studentCourseGrade .
#                          FILTER((?studentCourseGrade) != 'F') .
#                          FILTER((?studentCourseGrade) != '') .
#                     }
#                     """)
# print()
# print()
# print(
#     'For a given topic, list all students that are familiar with the topic (i.e., took, and did not fail, a course that covered the topic)')
# print()
# print('Student names: ')
# print()
# for row in queryFive:
#     x = row[0]
#     x = x.replace('http://focu.io/data#', '')
#     print(x)
# #
# querySix = g.query("""
#                     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#                     Prefix focu: <http://focu.io/schema#>
#                     PREFIX focudata: <http://focu.io/data#>
#                     SELECT  DISTINCT ?topicName
#                     WHERE {
#                       focudata:Honorato_Mccarty focu:graded_courses ?courseNameWithID .
#                       ?courseNameWithID focu:Course ?courseName .
#                       ?courseNameWithID focu:course_grade ?courseGrade .
#                       ?topic a focu:Topic .
#                       ?topic focu:containInverse ?courseName .
#                       ?topic foaf:name ?topicName
#                       FILTER((?courseGrade) != '')
#                       FILTER((?courseGrade) != 'F')
#                       }
#                     """)
# print()
# print()
# print('List all topics (no duplicates) that this student is familiar with: ')
# print()
# for row in querySix:
#     print(row[0])
