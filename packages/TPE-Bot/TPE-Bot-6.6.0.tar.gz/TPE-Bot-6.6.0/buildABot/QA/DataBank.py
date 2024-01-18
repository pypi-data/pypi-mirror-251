"""
Produce entries of common questions and answers for the subject: Writing in APA Styles in JSON format.
Focus on the following main topics: Reference List, In-text Citations and Elements of an APA Paper.
Question will be the value of the key question 1 and paraphrases of questions should be stored as questions 2 and 3.
JSON should include the following keys: Main Topic, Sub Topic, Name, Question 1, Question 2, Question 3, Answer.
"""
'''
Produce entries of common questions and answers for the subject: Biology (GCE A Levels) in array of JSON format with no main key value. 
Focus on the following main topics: Stem Cells, Cell Membrane & Cellular Transport, Organelles & Cellular Structures, Biomolecules of Life. 
Question will be the value of the key question 1. Name should be the title of the content.
JSON should include the following keys: Main Topic, Sub Topic, Name, Question 1, Answer.

Using the GCE A Levels Biology as a guideline, produce entries of questions and answers for the subject in array of JSON format with no main key value. Focus on the following main topics: Stem Cells, Cell Membrane & Cellular Transport, Organelles & Cellular Structures, Biomolecules of Life. Question will be the value of the key question 1. Name should be the title of the content. JSON should include the following keys: Main Topic, Sub Topic, Name, Question 1, Answer.
'''

import openai
import json
import pandas as pd
import os

class DataBank:
    def __init__(self) -> None:
        pass

    def getContent(api_key):
        openai.api_key = api_key # own api key
        messages = []
        mainTopics, subTopics, intentNames, q1s, responses = [], [], [], [], []

        while True:
            content = input("\n User: ")
            if (content == 'exit'):
                break
            print()
            print("Generating QA...\n")
            messages.append({"role": "user", "content": content})
            
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                #prompt="Produce at least 50 entries of common questions and answers for the subject: Writing in APA Styles in JSON format. Focus on the following main topics: Reference List, In-text Citations and Elements of an APA Paper. Question will be the value of the key question 1 and paraphrases of questions should be stored as questions 2 and 3. JSON should include the following keys: Main Topic, Sub Topic, Name, Question 1, Question 2, Question 3, Answer.",
                messages=messages,
                #max_tokens= 3900, # max no. of tokens to generate in completion
                temperature = 0.3, # close to 1 = creativity, close to 0 well-defined answers
                n=3 # no. of chat completion choices to generate for each input message
            )

            chat_response = completion.choices[0].message.content
            messages.append({"role": "assistant", "content": chat_response})

            # -- Extract content and put into respective placeholders -- #
            print(chat_response)
            chat_response_json = json.loads(chat_response)
            
            for i in range(len(chat_response_json)):
                intentRow = chat_response_json[i]
                #intent = json.loads(intentRow)
                

                mainTopic = intentRow['Main Topic']
                subTopic = intentRow['Sub Topic']
                intentName = intentRow['Name']
                q1 = intentRow['Question 1']
                response = intentRow['Answer']

                mainTopics.append(mainTopic)
                subTopics.append(subTopic)
                intentNames.append(intentName)
                q1s.append(q1)
                responses.append(response)

        return mainTopics, subTopics, intentNames, q1s, responses
    
    def extractNLoad(qaFile, mainTopics, subTopics, intentNames, q1s, responses):
        qaFile["Main Topic"] = mainTopics
        qaFile["Sub Topic"] = subTopics
        qaFile["Name"] = intentNames
        qaFile["Q1"] = q1s
        qaFile["Response 1"] = responses

        return qaFile