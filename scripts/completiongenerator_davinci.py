import openai
import os
import sys
import datetime

# add your tuned model here 
model = "davinci"

# get the api key from your environment variables
apiKey = os.getenv('OPENAI_API_KEY')
openai.api_key = apiKey

# completion directory
completionDirectory = sys.argv[1];

# check for an input argument
if len(sys.argv) > 2:
    promptText = sys.argv[2]
else:
    print("\nNO INPUT ARGUMENTS, using prompt: Who is a human?")
    promptText = "Who is a human?"

# print(openai.Engine.list())

# create some completions
print("PROMPT: " + promptText)
print('\n\n---\n\n')
promptFileName = promptText.replace(' ', '_')
t = datetime.datetime.now()
outputFile = open(completionDirectory + promptFileName + '_' + t.strftime("%m_%d_%H_%M_%S") + ".txt", "w")
outputFile.write("MODEL: " + model + "\n\n")
outputFile.write("PROMPT: " + promptText)
outputFile.write('\n\n---\n\n')
for x in range(6):
    # generate the completion
    completion = openai.Completion.create(engine=model, prompt=promptText, max_tokens=300, stop='.')
    # print the completion
    print(completion.choices[0].text + '.')
    print('\n\n---\n\n')
    # write to file
    outputFile.write(completion.choices[0].text + '.')
    outputFile.write('\n\n---\n\n')