import openai
import json
import pandas as pd
import time

class Responses:
    def __init__(self) -> None:
        pass

    def createResp(df, api_Key):
        openai.api_key = api_Key
        chat_responses = []

        for index, rows in df.iterrows():
            content = rows["Q1"]
            message = [{"role": "user", "content": content}]
            
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            max_tokens= 3800, # max no. of tokens to generate in completion (max 4097)
            temperature = 0.3, # close to 1 = creativity, close to 0 well-defined answers
            #n=3 # no. of chat completion choices to generate for each input message
            )

            chat_response = completion.choices[0].message.content
            chat_responses.append(chat_response)

            time.sleep(20)

        df["Response 2"] = chat_responses   
        return df