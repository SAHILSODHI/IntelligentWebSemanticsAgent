import spacy
import rdflib
from tkinter import *


def chatbot_response(msg):
    g = rdflib.Graph()
    result = g.parse(
        "knowledge_base/knowledgeBase_final.ttl",
        format='n3')

    nlp = spacy.load("en_core_web_sm")
    string = msg
    doc = nlp(msg)

    # “What is the <course> about?”
    # "What is Software_Verification_and_Testing about?"
    expression = r"What is [a-zA-Z_]* about?"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            course = string.split("What is ", 1)[1]
            courseName = course.split(" about")[0]
            print(courseName)
            courseName = courseName.replace(' ', '_')
            queryOne = g.query("""prefix focu: <http://focu.io/schema#>
                                  prefix focudata: <http://focu.io/data#>
                                  SELECT ?courseDescription
                                  where{
                                    focudata:""" + courseName + """ focu:course_description ?courseDescription
                                  }""")
            courseName = courseName.replace('_', ' ')
            x = "The course description for " + courseName + " is : \n"
            for row in queryOne:
                x = x + row[0]
            return x

    # “Which courses did <Student> take?”
    # "Which courses did Akeem_Cotton take?"
    expression = r"Which courses did [a-zA-Z_]* take?"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            student = string.split("Which courses did ", 1)[1]
            studentName = student.split(" take?")[0]
            queryOne = g.query("""prefix focu:     <http://focu.io/schema#>
                                  prefix focudata: <http://focu.io/data#>
                                  SELECT ?courseName
                                  where{
                                    focudata:Akeem_Cotton focu:graded_courses ?course .
                                    ?course focu:Course ?courseName .
                                  }""")
            studentName = studentName.replace('_', ' ')
            res = "Courses completed by " + studentName + " :\n\n"
            for row in queryOne:
                x = row[0]
                x = x.replace('http://focu.io/data#', '')
                x = x.replace('_', ' ')
                res = res + x + '\n'
            return res

    # “Which courses cover <Topic>?”
    # "Which courses cover Conflict_resolution?"
    expression = r"Which courses cover [a-zA-Z_]* ?"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            topic = string.split("Which courses cover ", 1)[1]
            topicName = topic[:-1]
            queryOne = g.query("""prefix focu:     <http://focu.io/schema#>
                                  prefix focudata: <http://focu.io/data#>
                                  SELECT ?courseName
                                  where{
                                    ?courseName a focu:Course .
                                    ?courseName focu:contains focudata:""" + topicName + """
                                }""")
            topicName = topicName.replace('_', ' ')
            res = "Courses covered by the topic " + topicName + " are:\n\n"
            print()
            for row in queryOne:
                x = row[0]
                x = x.replace('http://focu.io/data#', '')
                res = res + x + '\n'
            return res

    # “Who is familiar with <Topic>?”
    # "Who is familiar with Graph_theory?"
    expression = r"Who is familiar with [a-zA-Z_]* ?"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            topic = string.split("Who is familiar with ", 1)[1]
            topicName = topic[:-1]
            queryOne = g.query("""PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                                  Prefix focu: <http://focu.io/schema#>
                                  PREFIX focudata: <http://focu.io/data#>
                                  PREFIX dbpedia: <http://dbpedia.org/resource/>
                                  SELECT ?studentName
                                  WHERE {
                                    focudata:""" + topicName + """ focu:containInverse ?course .
                                    ?studentSubjectID focu:Course ?course .
                                    ?studentName focu:graded_courses ?studentSubjectID .
                                    ?studentSubjectID focu:course_grade ?studentCourseGrade .
                                    FILTER((?studentCourseGrade) != 'F') .
                                    FILTER((?studentCourseGrade) != '') .
                                  }""")
            res = "List of students familiar with " + topicName + " :\n\n"
            for row in queryOne:
                x = row[0]
                x = x.replace('http://focu.io/data#', '')
                res = res + x + '\n'
            return res

    # “What does <Student> know?”
    # "What does Honorato_Mccarty know?"
    expression = r"What does [a-zA-Z_]* know?"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            student = string.split("What does ", 1)[1]
            studentName = student.split(" know?")[0]
            queryOne = g.query("""PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                                  Prefix focu: <http://focu.io/schema#>
                                  PREFIX focudata: <http://focu.io/data#>
                                  SELECT  DISTINCT (lcase(?topicName) as ?topicNames) 
                                  WHERE {
                                    focudata:""" + studentName + """ focu:graded_courses ?courseNameWithID .
                                    ?courseNameWithID focu:Course ?courseName .
                                    ?courseNameWithID focu:course_grade ?courseGrade .
                                    ?topic a focu:Topic .
                                    ?topic focu:containInverse ?courseName .
                                    ?topic foaf:name ?t
                                    FILTER((?courseGrade) != '')
                                    FILTER((?courseGrade) != 'F')
                                    BIND(REPLACE(STR(?t),"-"," ") AS ?topicName)
                                  }""")
            res = "List of all topics " + studentName + " is familiar with :\n\n"
            print()
            for row in queryOne:
                x = row[0]
                x = x.replace('http://focu.io/data#', '')
                res = res + x + '\n'
            return res


def input():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#00FF00", font=("Calibri", 14))

        res = chatbot_response(msg)
        if res is None:
            ChatLog.insert(END, "Bot: What do you mean by " + msg + "?\n\n")
        else:
            ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("University Based Chatbot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="black", height="10", width="55", font="Calibri", )

ChatLog.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

# Ask Button
AskButton = Button(base, font=("Calibri", 14, 'bold'), text="Ask", width="12", height=5,
                    bd=0, bg="black", activebackground="black", fg='black', activeforeground='#00FF00',
                    background='black',foreground='#00FF00', highlightbackground='black',
                    command=input)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="black", width="29", height="5", font="Calibri", foreground='#00FF00')

# widget placement
scrollbar.place(x=380, y=7, height=388)
ChatLog.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
AskButton.place(x=6, y=401, height=90)
base.mainloop()
