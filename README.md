# IntelligentAgent
Building an Intelligent Agent using Web Semantics and Knowledge Graphs.
This project is aimed at building an intelligent agent. The knowledge graph is made using Concordia university courses and fake student database.
The data is retrieved using SPARQL.

40093437 Sahil Singh Sodhi
40080981 Gursimran Singh 

HOW TO RUN?

Change directory to  IntelligentAgent_assginment1

The query.py is used to run the queries and generate the query txt files.

The core.py contains the methods which are run from main.py

Since the dataset for the courses provided for various programs is already put in cumulativeCoursesDataset.csv file, to create the knowledgeBase, in the main.py file, run three functions.
•	create_graph_schema(), to create the schema of the knowledgeBase automatically.
•	Then run, create_graph_from_csv() to create the graph for the courses, and respected topics. 
•	And finally, run add_student_data_to_graph() to add the student records in the knowledgeBase. 

On Terminal, 
run python main.py to run all the functions.

This will create the knowledge_base.ttl file.
