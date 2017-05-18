# Automatic_Grader

This is a simple tool. various optimizations can be done. I wrote in very short
duration to get my work done.

Preconditions:

1. Put the sql files of all students in a folder known as submissions.
2. This tool also contain code to extract sql commands from doc file to create a
folder containing sql files. The python code to run for it is docToSql.py.
3. Create a master_query.sql file which has all the answers/key for each question.
4. In the beginning, this tool first run the master_query.sql file to create a 
master_query_out.txt and then run each file in submissions folder.
5. You need to provide/Insert own your ip-address, username, password, database_name
in command mdb.connect in driver.py file. This will establish a connection to the sql
server.


Descriptions:

1. This tool basically takes in input various submission files which are 
sql files containing commands for each question and grades if it is the correct
response for that question.

2. Run driver.py to get the mark-sheet of all students.

3. A folder known as results will also get created containing the comment file 
corresponding to each submission file.

4. At the end, a Marksheet.xls file will get created containing the marks of 
individual students.

5. Currently submissions folder consists of Doe_John.sql file.
