#!/usr/bin/env python

import os
import copy
import logging
import argparse
from os import listdir
from datetime import datetime
from os.path import isfile, join
from striprtf.striprtf import rtf_to_text

LOGGER = logging.getLogger('ReadInputFile')
INPUT_DIR = './lexisnexis'
OUTPUT_FILE = './lexisnexis.txt'
TEMPLATE_FILE = './templates/lexis_rtf_template.txt'
DEBUG = True

class ArgParser:
    def __init__(self):
        LOGGER.debug('Init ArgsParser')

    def parseArguments(self):
        LOGGER.debug('Parsing the arguments')
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--inputDir", "-i", help="Input Directory with the Lexis Nexis RTF file (*** No formatting ***)",
            required=True)
        parser.add_argument(
            "--outputFile", "-o", help="Output file to write the lexis nexis parsed txt file", required=True)
        parser.add_argument(
            '--debug', '-d', help="Enable Debug (** Will flood the screen **)", action='store_true', required=False)
        args = parser.parse_args()
        return args


class Utils:
    def __init__(self):
        LOGGER.debug('Loading the util class')

    def isFile(self, filename):
        LOGGER.debug(f'Checking if the file {filename} is present')
        return os.path.isfile(filename)

    def createDirIdenpotent(self, filename):
        try:
            LOGGER.debug(f'Creating the directory for the filename {filename} if necessary')
            path = os.path.abspath(filename)
            directory = os.path.dirname(path)
            if not os.path.isdir(directory):
                os.makedirs(directory)
            return True
        except Exception as e:
            LOGGER.error(f'Unable to createDirIdenpotent. Error = {e}')
            return False


class ReadInputFile:
    def __init__(self, filename):
        LOGGER.debug('Init ReadInputFile')
        self.filename = filename

    def readFileContents(self):
        fileContent = ''
        try:
            with open(self.filename, 'r', encoding='utf8') as file:
                for line in file:
                    printDebug(f'Reading line: {line}')
                    if line.strip() != '':
                        fileContent = fileContent + line + '\n'
                    else:
                        fileContent = fileContent + line
            return fileContent
        except Exception as e:
            LOGGER.error(f'Error in reading the file {self.filename}. Error = {e}')
            return None


class WriteOutputFile:
    def __init__(self, outputFilePath):
        LOGGER.debug(f'Init Output writer with outputfilePath = {outputFilePath}')
        self.outputFilePath = outputFilePath
        util = Utils()
        if 'noop' not in outputFilePath:
            util.createDirIdenpotent(outputFilePath)
        with open(self.outputFilePath, 'w', encoding='utf8') as writeFileObj:
            writeFileObj.write('')

    def writeOutput(self, text):
        try:
            LOGGER.info(f'Writing output to the file {self.outputFilePath}')
            with open(self.outputFilePath, 'a+', encoding='utf8') as writeFileObj:
                writeFileObj.write(text + '\n')
            LOGGER.info(f'Completed Writing output to the file {self.outputFilePath}')
        except Exception as e:
            LOGGER.error(f'Error in writing to the file {self.outputFilePath}. Error = {e}')


def printDebug(string):
    if DEBUG:
        print(string)


def extractValue(data):
    if ':' in data:
        return data.split(':')[1].strip()
    else:
        return data.strip()


def parseDocumentsFromRTF(parsedText):
    documents = []
    docBody = False
    counter = 0
    body = ''
    documentTemplate = {'title': '',
                        'source': 'Unknown Newspaper',
                        'date': datetime.now().strftime('%B %d, %Y %A %I:%M %p GMT'),
                        'copyright': 'Copyright None Found',
                        'length': '99 words',
                        'section': 'A,A; Pg 1',
                        'language': 'ENGLISH',
                        'pubtype': 'Newspaper',
                        'subject': '',
                        'geographic': '',
                        'loaddate': datetime.now().strftime('%B %d, %Y %A %I:%M %p GMT'),
                        'byline': 'No Author',
                        'body': ''}
    document = copy.deepcopy(documentTemplate)
    for line in parsedText.split('\n'):
        printDebug(counter)
        tempLine = line.strip()
        printDebug(tempLine)
        if tempLine != '':
            counter += 1
            if counter == 1:
                printDebug('Title')
                document['title'] = line
                continue
            if counter == 2:
                printDebug('Source')
                document['source'] = line
                continue
            if counter == 3:
                printDebug('Date')
                document['date'] = line
                continue
            if tempLine.startswith('Copyright '):
                printDebug('CR')
                document['copyright'] = line
                continue
            if tempLine.startswith('Length:'):
                printDebug('Len')
                document['length'] = extractValue(line)
                continue
            if tempLine.startswith('Section:'):
                printDebug('Sec')
                document['section'] = extractValue(line)
                continue
            if tempLine.startswith('Language:'):
                printDebug('Lang')
                document['language'] = extractValue(line)
                continue
            if tempLine.startswith('Publication-Type:'):
                printDebug('Pub Type')
                document['pubtype'] = extractValue(line)
                continue
            if tempLine.startswith('Subject:'):
                printDebug('Sub')
                document['subject'] = extractValue(line)
                continue
            if tempLine.startswith('Geographic:'):
                printDebug('Geog')
                document['geographic'] = extractValue(line)
                continue
            if tempLine.startswith('Load-Date:'):
                printDebug('Load Date')
                document['loaddate'] = extractValue(line)
                document['body'] = body
                body = ''
                docBody = False
                continue
            if tempLine.startswith('Byline:'):
                printDebug('Byline')
                document['byline'] = extractValue(line)
                continue
            if tempLine == 'Body':
                printDebug('body-start')
                body = ''
                docBody = True
                continue
            if tempLine.startswith('[readmore]'):
                printDebug('meta')
                continue
            if tempLine == 'End of Document':
                printDebug('End of Doc')
                documents.append(document)
                document = copy.deepcopy(documentTemplate)
                counter = 0
                continue
            if docBody:
                printDebug('body-line')
                body += line + '\n'
                continue
    return documents


def writeParsedDocumentsToFile(writer, documents, templateString):
    totalDocs = len(documents)
    counter = 1
    for doc in documents:
        writer.writeOutput(templateString.format(doc['copyright'],
                                                 counter,
                                                 totalDocs,
                                                 doc['source'],
                                                 doc['date'],
                                                 doc['title'],
                                                 doc['byline'],
                                                 doc['section'],
                                                 doc['length'],
                                                 doc['body'],
                                                 doc['loaddate'],
                                                 doc['language'],
                                                 doc['pubtype']))
        print(f'Written doc {counter} of {totalDocs} into {OUTPUT_FILE}')
        counter += 1


def readFiles(inputDir):
    files = [join(inputDir, f) for f in listdir(inputDir) if isfile(join(inputDir, f))]
    if len(files) == 0:
        printDebug(f'No files in the directory {inputDir}')
        os.exit(1)
    return files


def parseCLI():
    global INPUT_DIR
    global OUTPUT_FILE
    global DEBUG
    argParser = ArgParser()
    args = argParser.parseArguments()
    DEBUG = args.debug
    if args.inputDir:
        INPUT_DIR = args.inputDir
        print(f'Input Directory set to {INPUT_DIR}')
    if args.outputFile:
        OUTPUT_FILE = args.outputFile
        print(f'Output File set to {OUTPUT_FILE}')


def rtfToTxt(inputDir, templateFile, outputFile):
    print(f"{datetime.now().strftime('%B %d, %Y %A %I:%M %p GMT')}: *** Parsing Started ***")
    args = parseCLI()
    files = readFiles(inputDir)
    templateReader = ReadInputFile(templateFile)
    templateString = templateReader.readFileContents()
    writer = WriteOutputFile(outputFile)
    superDocs = []
    for file in files:
        reader = ReadInputFile(file)
        text = reader.readFileContents()
        parsedText = rtf_to_text(text)
        documents = parseDocumentsFromRTF(parsedText)
        superDocs.extend(documents)
    writeParsedDocumentsToFile(writer, superDocs, templateString)
    print(f"{datetime.now().strftime('%B %d, %Y %A %I:%M %p GMT')}: *** Parsing Completed ***")


if __name__ == "__main__":
    rtfToTxt(INPUT_DIR, TEMPLATE_FILE, OUTPUT_FILE)
