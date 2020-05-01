import rdflib

g = rdflib.Graph()
result = g.parse("knowledgeBase_final.ttl", format='ttl')

def generate_out(query, name, out):
    if out is False:
        f = open('{}.txt'.format(name), "w")
        f.write(query)
        f.close()
    else:
        file = open('{}-out.ttl'.format(name), 'w')
        return file

queries = {1: """SELECT (count(?s) as ?count)
                    WHERE
                    {
                      ?s ?p ?o
                    }""",
           2: """
                    PREFIX focu: <http://focu.io/schema#>
                    SELECT DISTINCT(count(?s) as ?NumberOfStudents) (count(?c) as ?NumberOfCourses) (count(?t) as ?NumberOfTopics)
                    WHERE
                    {
                      {?c a focu:Course.}
                      UNION
                      {?s a focu:Student.}
                      UNION
                      {?t a focu:Topic.}
                    }""",
           3: """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    Prefix focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    SELECT DISTINCT (lcase(?t) as ?topicName) ?topicLink
                    WHERE {
                        focudata:Computer_Networks_and_Protocols focu:contains ?topic.
                        ?topic owl:sameAs ?topicLink .
                        ?topic foaf:name ?t
                    }""",
           4: """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    Prefix focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    SELECT  ?courseName ?courseGrade
                    WHERE {
                        focudata:Akeem_Cotton focu:graded_courses ?course .
                        ?course focu:Course ?courseName .
                        ?course focu:course_grade ?courseGrade .
                        FILTER((?courseGrade) != '') .
                    }""",
           5: """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    Prefix focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    PREFIX dbpedia: <http://dbpedia.org/resource/>
                    SELECT ?studentName
                    WHERE {
                      focudata:Graph_theory focu:containInverse ?course .
                      ?studentSubjectID focu:Course ?course .
                      ?studentName focu:graded_courses ?studentSubjectID .
                      ?studentSubjectID focu:course_grade ?studentCourseGrade .
                      FILTER((?studentCourseGrade) != 'F') .
                      FILTER((?studentCourseGrade) != '') .
                    }
                    """,
           6: """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    Prefix focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    SELECT  DISTINCT (lcase(?topicName) as ?topicNames) 
                    WHERE {
                      focudata:Honorato_Mccarty focu:graded_courses ?courseNameWithID .
                      ?courseNameWithID focu:Course ?courseName .
                      ?courseNameWithID focu:course_grade ?courseGrade .
                      ?topic a focu:Topic .
                      ?topic focu:containInverse ?courseName .
                      ?topic foaf:name ?t
                      FILTER((?courseGrade) != '')
                      FILTER((?courseGrade) != 'F')
                      BIND(REPLACE(STR(?t),"-"," ") AS ?topicName)
                    }
                    """
           }

generate_out(queries[1],"q1",False)
generate_out(queries[2],"q2",False)
generate_out(queries[3],"q3",False)
generate_out(queries[4],"q4",False)
generate_out(queries[5],"q5",False)
generate_out(queries[6],"q6",False)

# s = g.serialize(format='n3')
##################QUERY ONE##################################

print()
print()
queryOne = g.query(queries[1])
print('Query One')
f1 = generate_out("", "q1", True)
for row in queryOne:
    print('Total number of triples in the KB: ' + row[0], file= f1)
f1.close()
print()

##################QUERY TWO##################################

queryTwo = g.query(queries[2])
print()
print('Query Two')
f1 = generate_out("", "q2", True)
for row in queryTwo:
    print('Number of Students: ' + row[0], file=f1)
    print('Number of Courses: ' + row[1], file=f1)
    print('Number of Topics: ' + row[2], file=f1)
f1.close()

##################QUERY THREE##################################

queryThree = g.query(queries[3])

print()
print()
print('Query Three')
print('For the given course, list all covered topics using their (English) labels and their link to DBpedia: ')
print()
f1 = generate_out("", "q3", True)
for row in queryThree:
    print('Topic English Name: ' + row[0], file=f1)
    print('Topic Link: ' + str(row[1]), file=f1)
    print()
f1.close()

##################QUERY FOUR##################################

queryFour = g.query(queries[4])
print()
print()
print('Query Four')
print('For a given student, list all courses this student completed, together with the grade')
print()
f1 = generate_out("", "q4", True)
for row in queryFour:
    x = row[0]
    x = x.replace('http://focu.io/data#', '')
    print('Course Name: ' + x, file=f1)
    print('Course Grade: ' + row[1], file=f1)
    print()
f1.close()

##################QUERY FIVE##################################

queryFive = g.query(queries[5])
print()
print()
print('Query Five')
print(
    'For a given topic(focudata:Graph_theory), list all students that are familiar with the topic (i.e., took, and did not fail, a course that covered the topic)')
print()
print('Student names: ')
print()
f1 = generate_out("", "q5", True)
for row in queryFive:
    x = row[0]
    x = x.replace('http://focu.io/data#', '')
    print(x,file=f1)
f1.close()


##################QUERY SIX##################################

querySix = g.query(queries[6])
print()
print()
print('Query Six')
print('List all topics (no duplicates) that this student(focudata:Honorato_Mccarty) is familiar with: ')
print()
f1 = generate_out("", "q6", True)
for row in querySix:
    print(row[0],file=f1)
f1.close()




