"""
1. Delete results folder before run
2. Convert output to xls file
3. Simultaneously read each query from input file in a folder and each query
   from master_query file. Compare the results and generate the out file in
   a different folder.
4. Output: A comment file for each student with feedback and their marks
   obtained.
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
from os.path import basename
import os
import sys
from pandas import DataFrame
import shutil
import time


def printQueryOutput(description, results):
    widths = []
    columns = []
    tavnit = '|'
    separator = '+'

    if not description:
        print "No result"
        return
    for cd in description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-" + "%ss |" % (w,)
        separator += '-' * w + '--+'

    print(separator)
    # print(tavnit.format(tuple(columns)))
    print(tavnit % tuple(columns))
    print(separator)

    try:
        for row in results:
            print(tavnit % row)
    except TypeError, msg:
        print msg
        pass
    print(separator)


def execute_slave_command(cursor, connection, command, mcommand, count, subs, marks):
    # print "command is ", command
    if "Select" not in command and "select" not in command and "SELECT" not in command:
        print "<< Question", count - subs, ">>: 0 Marks as One Correct SQL Query can be: "
        print mcommand
        print '\n'
        print "While your SQL query is empty."
        print '\n'
        return marks
    cursor.execute(command)
    connection.commit()
    results = cursor.fetchall()
    cursor_desc = cursor.description

    cursor.execute(mcommand)
    connection.commit()
    mresults = cursor.fetchall()
    master_cursor_desc = cursor.description

    if results == mresults:
        marks += 5
    else:
        print "<< Question", count - subs, ">>: -2.5 Mark as One Correct SQL Query can be: "
        print mcommand
        print '\n'
        print "While your SQL query is: "
        print command
        print '\n'
        print "Correct output should be: "
        printQueryOutput(master_cursor_desc, mresults)

        print '\n'
        if len(results) > 1000:
            print "While your result is too big. I think you missed something: "
            printQueryOutput(cursor_desc, results[:50])
            print '...'
        else:
            print "While your result is: "
            printQueryOutput(cursor_desc, results)

        print '------------------------------------------------------------------------------------------------------------------------'
        print '\n'
        marks += 2.5

    return marks


def run_sql_file(filename, masterFile, connection1, connection2):
    """
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection
    """
    orig_stdout = sys.stdout

    if not os.path.exists('results/'):
        os.makedirs('results/')

    # extract file name string from input file
    inputFileBaseName = basename(filename)
    # Remove extension of file
    inputFileString = os.path.splitext(inputFileBaseName)[0]

    # Find an output file name based on input file
    outputFilename = inputFileString + '_out.txt'
    # Create an output file
    outFile = open('results/' + outputFilename, 'w')
    sys.stdout = outFile

    # Read the input sql file
    inputFile = open(filename, 'r')
    sqlFile = " ".join(inputFile.readlines())
    sqlCommands = sqlFile.split(';')

    # Read the master_query.sql file
    mFile = open(masterFile, 'r')
    msqlFile = " ".join(mFile.readlines())
    mResults = msqlFile.split(';')

    cursor1 = connection1.cursor()
    cursor2 = connection2.cursor()

    # Execute every command from the input file
    marks = 0
    count = 1
    for command, mcommand in zip(sqlCommands, mResults):
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        # print "Result for Query", count, ":"

        # if not command:
        #     continue
        if count in (1, 2, 8, 9, 10, 14):
            count += 1
            continue
        elif count in (3, 4, 5, 6, 7):
            if count == 3:
                print "\n******************************************* Table being used is final_company ******************************************\n"

            try:
                marks = execute_slave_command(cursor1, connection1, command, mcommand, count, 2, marks)

            except mdb.OperationalError, msg:
                print "<<Question", count - 2, ">>: 0 Marks as Your SQL query is wrong"
                print "Error Returned is: ", msg
                print '\n'
                print "One Correct SQL Query can be: "
                print mcommand
                print '\n'
                print "While your SQL query is: "
                print command
                print '------------------------------------------------------------------------------------------------------------------------'
                print '\n'
                pass

            except mdb.Error, msg:
                print "<<Question", count - 2, ">>: 0 Marks as Your SQL query is wrong"
                print "Error Returned is: ", msg
                print '\n'
                print "One Correct SQL Query can be: "
                print mcommand
                print '\n'
                print "While your SQL query is: "
                print command
                print '------------------------------------------------------------------------------------------------------------------------'
                print '\n'
                pass

        else:
            if count == 11:
                print "\n\n******************************************* Table being used is final_sales ********************************************\n"

            try:
                marks = execute_slave_command(cursor2, connection2, command, mcommand, count, 10, marks);

            except mdb.OperationalError, msg:
                print "<<Question", count - 10, ">>: 0 Marks as Your SQL query is wrong"
                print "Error Returned is: ", msg
                print '\n'
                print "One Correct SQL Query can be: "
                print mcommand
                print '\n'
                print "While your SQL query is: "
                print command
                print '------------------------------------------------------------------------------------------------------------------------'
                print '\n'
                pass

            except mdb.Error, msg:
                print "<<Question", count-10, ">>: 0 Marks as Your SQL query is wrong"
                print "Error Returned is: ", msg
                print '\n'
                print "One Correct SQL Query can be: "
                print mcommand
                print '\n'
                print "While your SQL query is: "
                print command
                print '------------------------------------------------------------------------------------------------------------------------'
                print '\n'
                pass

        count += 1
        # time.sleep(1)

    print '\n'
    print "Marks Obtained = ", marks
    if marks == 40:
        print 'Good'

    sys.stdout = orig_stdout

    outFile.close()
    inputFile.close()
    mFile.close()
    return marks


def executeCommand(cursor, connection, mcommand, count, subs):
    try:
        cursor.execute(mcommand)
        connection.commit()
        mresults = cursor.fetchall()
        # mrc = cursor.rowcount
        master_cursor_desc = cursor.description

        print "<< Question", count - subs, ">>: "
        print mcommand + ';'
        print '\n'
        # print "print called for ",
        printQueryOutput(master_cursor_desc, mresults)
        print '------------------------------------------------------------------------------------------------------------------------'
        print '\n'

    except mdb.OperationalError, msg:
        print "Command skipped: ", msg

    except mdb.Error, msg:
        print "<< Question", count - subs, ">>: 0 Marks as Your SQL query is wrong"
        print "Error Returned is: ", msg
        print '\n'
        print "One Correct SQL Query can be: "
        print mcommand
        print '\n'
        print "While your SQL query is: "
        print mcommand
        print '\n'
        print '------------------------------------------------------------------------------------------------------------------------'
        pass


def run_master_sql_file(masterFile, connection1, connection2):
    """
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection
    """
    orig_stdout = sys.stdout

    # extract file name string from input file
    inputFileBaseName = basename(masterFile)
    # Remove extension of file
    inputFileString = os.path.splitext(inputFileBaseName)[0]

    # Find an output file name based on input file
    outputFilename = inputFileString + '_out.txt'
    # Create an output file
    outFile = open(outputFilename, 'w')
    sys.stdout = outFile

    # Read the master_query.sql file
    mFile = open(masterFile, 'r')
    msqlFile = " ".join(mFile.readlines())
    mResults = msqlFile.split(';')

    cursor1 = connection1.cursor()
    cursor2 = connection2.cursor()

    # Execute every command from the input file
    # marks = 0
    count = 1
    for mcommand in mResults:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        # print "Result for Query", count, ":"

        if count in (1, 2, 8, 9, 10, 14):
            count += 1
            continue
        elif count in (3, 4, 5, 6, 7):
            if count == 3:
                print "\n******************************************* Table being used is final_company ******************************************\n"
            executeCommand(cursor1, connection1, mcommand, count, 2)

        else:
            if count == 11:
                print "\n\n******************************************* Table being used is final_sales ********************************************\n"
            executeCommand(cursor2, connection2, mcommand, count, 10)

        count += 1

    print '\n'

    sys.stdout = orig_stdout

    outFile.close()
    mFile.close()
    # return marks


def main():
    # *** Insert own your ip-address, username, password, database_name over here
    # Here we are establishing connection with 2 servers
    connection1 = mdb.connect('ip_address', 'user_name', 'pass_word', 'database_name')
    connection2 = mdb.connect('ip_address', 'user_name', 'pass_word', 'database_name')

    masterFile = 'master_query.sql'
    print "Running " + masterFile
    run_master_sql_file(masterFile, connection1, connection2)

    if os.path.exists('results/'):
        # print "Lets delete the results folder"
        shutil.rmtree('results/')

    DIR = 'submissions/'
    total_subm_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    print "\nRunning submission files..."
    count = 1
    for fle in os.listdir('submissions/'):
        fle = 'submissions/' + fle

        marks = run_sql_file(fle, masterFile, connection1, connection2)

        # extract file name string from input file
        inputFileBaseName = basename(fle)
        # Remove extension of file
        inputFileString = os.path.splitext(inputFileBaseName)[0]

        name = inputFileString.split('_')
        print "Running " + str(count) + '/' + str(total_subm_files) + ': ' + inputFileBaseName

        # print "length name", len(name)
        if count == 1:
            if len(name) == 1:
                df = DataFrame({'First Name': name, 'Marks': marks}, index=[0])
            else:
                df = DataFrame({'Last Name': name[0], 'First Name': name[1], 'Marks': marks}, index=[0])
        else:
            if len(name) == 1:
                data = {'First Name': name, 'Marks': marks}
            else:
                data = {'Last Name': name[0], 'First Name': name[1], 'Marks': marks}
            df = df.append(data, ignore_index=True)
        count += 1
        # time.sleep(2)

    df.to_excel('Marksheet.xlsx', sheet_name='sheet1', index=False)

    print '\nAll submitted files have run!!!'
    connection1.close()
    connection2.close()


if __name__ == "__main__":
    main()
