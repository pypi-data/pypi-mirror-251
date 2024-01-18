import openai
import json
import pandas as pd
import time

class Para:
    def __init__(self) -> None:
        pass
    
    def genPara(df, api_key):
        openai.api_key = api_key
        para = []

        for index, rows in df.iterrows():
            content = "Give me 10 paraphrases of the following in bullet list: " + rows["Q1"]
            message = [{"role": "user", "content": content}]
            
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            max_tokens= 2000, # max no. of tokens to generate in completion (max 4097)
            temperature = 0.3, # close to 1 = creativity, close to 0 well-defined answers
            #n=3 # no. of chat completion choices to generate for each input message
            )

            chat_response = completion.choices[0].message.content
            para.append(chat_response.split('\n'))

            time.sleep(15)

        data = pd.DataFrame(para, columns = ['Q51', 'Q52', 'Q53', 'Q54', 'Q55', 'Q56', 'Q57', 'Q58', 'Q59', 'Q60'])
            
        result = pd.concat([df, data], axis=1)
        return result

