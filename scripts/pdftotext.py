import os
import sys
import re
import datetime
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize

# arguments: ../reading/test outputs/

# creates plaintext file scraped from pdf...string / text manipulation is a bit zany
def createPlaintext(inputDirectory, outputDirectory): 
    # iterate through directory
    for fileName in os.listdir(inputDirectory):
        inputFile = os.path.join(inputDirectory, fileName)
        # check for pdf
        if os.path.isfile(inputFile):
            if inputFile.endswith('.pdf'):
                print('processing: ' + fileName)
                # split path name
                ff = inputFile.split('/')
                fff = ff[2].split('.')
                outputFile = outputDirectory + fff[0] + '.txt'
                # reformat output file path / name with spaces and such...such a mess
                inputFileNoSpaces = inputFile.replace(' ', '\ ')
                outputFileNoSpaces = outputFile.replace(' ', '\ ')
                # print(inputFileNoSpaces, outputFileNoSpaces)
                # run pdftotext with a generic crop box
                # NOTES: 
                # - if you're getting weird pdf to text outputs try adjusting the crop bounday,
                # - -q flag mutes error outputs
                # - scanned pdfs may not work well
                command = 'pdftotext -q -eol unix -x 25 -y 60 -H 500 -W 650 -nopgbrk ' + inputFileNoSpaces + ' ' + outputFileNoSpaces
                # print(command) 
                os.system(command)
                # open the output files
                f1 = open(outputFile, 'r')
                f2 = open(outputFile + '_tmp', 'w')
                # read plaintext
                f1output = f1.read()
                # remove new lines from file
                f1replace = f1output.replace('\n', ' ')
                # write to other output file
                f2.write(f1replace)
                # close the files
                f1.close()
                f2.close()
                # remove the newline file and repalce with noline file
                os.remove(outputFile)
                os.rename(outputFile + '_tmp', outputFile)

# extract sentences from text using nlp toolkit
def getSentences(text):
    sentences = sent_tokenize(text)
    return sentences
                
# write to json file in chunks of N sentences
def writeToJSON(outputfile, title, sentences, N):
    # write initial prompt completion format
    outputfile.write('{"prompt":"' + title + '","completion":" ') 
    # write sentences
    for x in range(len(sentences)):
        sentenceNoQuotes = sentences[x].replace('"', '\\"')
        outputfile.write(' ' + sentenceNoQuotes)
        if x % N == 0:
             outputfile.write('"}\n{"prompt":"' + title + '","completion":" ') 
    # end with closing brace 
    outputfile.write('"}\n') 

# takes plaintext and creates json file with prompts and completions
def createJSON(inputDirectory, outputDirectory):
    print('creating JSON file')
    # open the json file to write to and name it based on datetime
    t = datetime.datetime.now()
    outputFile = open(outputDirectory + '/' + t.strftime("%m_%d_%H_%M_%S") + ".json", "w")
    # iterate over plaintext files
    for fileName in os.listdir(inputDirectory):
        inputFile = os.path.join(inputDirectory, fileName)
        if os.path.isfile(inputFile):
            # make sure we have a txt file
            if inputFile.endswith('.txt'):
                # chop up the path
                title = re.split('\.|\/', inputFile)
                f = open(inputFile, 'r')
                # read the file
                inputText = f.read()
                # split text into sentences
                sentences = getSentences(inputText)
                # write sentences to json file in chunks of 4
                writeToJSON(outputFile, title[1], sentences, 8)


def main():
    # directory with pdfs
    pdfDirectory = sys.argv[1]
    # directory to store plaintext files
    plaintextDirectory = sys.argv[2]
    # directory to store json outputs
    dataOutputDirectory = sys.argv[3]

    print('---- PDF to DATASET SCRIPT for GPT3 ----')
    print('taking pdf inputs from: ' + pdfDirectory)
    print('sending plaintext outputs to: ' + plaintextDirectory)
    print('sending JSON outputs to: ' + dataOutputDirectory)
    print('running....')

    # create plaintext files from pdfs
    createPlaintext(pdfDirectory, plaintextDirectory)
    # create a JSON file from the converted pdfs
    createJSON(plaintextDirectory, dataOutputDirectory)

    print('done!')
    print('sent JSON outputs to: ' + dataOutputDirectory)
    print('----------------------------------------')


if __name__ == "__main__":
    main()