import re
import os
import sys
from os.path import basename
import docx


# Extract sql commands from a doc file and create 
# a sql file containing sql commands only
def docTosql():
    orig_stdout = sys.stdout

    for fle in os.listdir('docfiles/'):
        fle = 'docfiles/' + fle

        # extract file name string from input file
        inputFileBaseName = basename(fle)
        # Remove extension of file
        inputFileString = os.path.splitext(inputFileBaseName)[0]

        # Find an output file name based on input file
        outputFilename = inputFileString + '.sql'
        # Create an output file
        outFile = open('submissions/' + outputFilename, 'w')
        sys.stdout = outFile

        doc = docx.Document(fle)
        count = 1
        for para in doc.paragraphs:
            # print "paragraph", count
            # print para.text
            parag = para.text
            # parag = para.rstrip()
            # para.text.rstrip()
            # print parag
            if re.search('select(.+?);', parag):
                start = parag.find('select')
                end = parag.find(';')
                print parag[start:end+1].encode("utf-8")

            elif re.search('Select(.+?);', parag):
                start = parag.find('Select')
                end = parag.find(';')
                print parag[start:end + 1].encode("utf-8")

            elif re.search('SELECT(.+?);', parag):
                start = parag.find('SELECT')
                end = parag.find(';')
                print parag[start:end + 1].encode("utf-8")
            # count +=1

        sys.stdout = orig_stdout
        outFile.close()


def main():
    docTosql()

if __name__ == "__main__":
    main()
