import json
import os
import pandas as pd

from .CustomResponse import CustomResponse
from .CustomTeleResponse import CustomTeleResponse
from .RelatedIntents import RelatedIntents
from .Usersays import Usersays
from .Type.Chips import Chips

class CustomIntents(CustomResponse, CustomTeleResponse, RelatedIntents, Usersays):
    def write_file_json(QA_Data, data):
        with open(QA_Data, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4)

    def getIntentTemplate():
        return {
        "id": "",
        "name": "", # INTENT  NAME
        "auto": True,
        "contexts": ["loggedIn"],
        "responses": [
        {
            "resetContexts": False,
            "action": "",
            "affectedContexts": [
            {
                "name": "loggedIn",
                "lifespan": 50
            }
            ],
            "parameters": [
                {
                    "id": "f01c8262-a826-461b-ba66-ec3eb9667a0f",
                    "name": "loginID",
                    "required": False,
                    "dataType": "@LoginID",
                    "value": "#loggedIn.loginID",
                    "defaultValue": "",
                    "isList": False,
                    "prompts": [],
                    "promptMessages": [],
                    "noMatchPromptMessages": [],
                    "noInputPromptMessages": [],
                    "outputDialogContexts": []
                }
            ],
            "messages": [
                # PAYLOADS
            ],
            "speech": []
        }
        ],
        "priority": 500000,
        "webhookUsed": False,
        "webhookForSlotFilling": False,
        "fallbackIntent": False,
        "events": [
            {
                "name": ""
            }
        ],
        "conditionalResponses": [],
        "condition": "",
        "conditionalFollowupEvents": []
    }

    def getReturnChipsPayload():
        return {
                "type": "4",
                "title": "",
                "payload": {
                    "richContent": [[
                        {
                            "options": [
                                #ReturnChips
                            ],
                            "type": "chips"
                        }
                    ]]
                },
                "textToSpeech": "",
                "lang": "en",
                "condition": ""
            }  

    def createIntentResponse(df):
        '''
        delete existing files to avoid being port into new deployment
        '''
        dir = os.getenv('learnIntents')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
            
        # get length of response
        df["Response Length"] = df.Response.apply(lambda x: len(str(x).split(' ')))
        
        for index, row in df.iterrows():
            intentResponse = CustomIntents.getIntentTemplate()
            placeholder = intentResponse["responses"][0]["messages"]

            # Formatting intentName
            intentName = str(row['Main Label']) + '.' + str(row['Intent Label']) + ' ' + row['Main Topic'] + ' - ' + row['Name']
            intentName = intentName.strip()
            if(len(intentName) > 100):
                intentName = intentName[:100]

            # Getting required columns
            title = row['Name']
            image = row['Image Link']
            response = row['Response']
            redirect = row['External Link']
            length = row["Response Length"]

            mainTopic = row["Main Topic"]

            # Putting data into placeholders
            intentResponse["name"] = intentName
            intentResponse['events'][0]['name'] = title.replace(" ", "")
            
            # Telegram Response
            placeholder.append(CustomTeleResponse.createTeleRepsonse(title, image, response, redirect))
            placeholder.append(CustomTeleResponse.createFeedbackQuickReplies())
            placeholder.append(CustomTeleResponse.createTeleKeyboard(mainTopic))
            
            # Messenger Response
            placeholder.append(CustomResponse.createResponseType(title, image, response, redirect, length)) #Messenger response
            placeholder.append(CustomResponse.getFeedbackChips()) #feedback

            # Related Intents
            dfRelated = (row.filter(like="Related Intent")).to_frame().transpose() # error here when parsed into function createRelated Pauload
            df2 = df[['S/N', 'Q1']]
            if ((row["Related Intent 1"])):
                placeholder.append(RelatedIntents.createRelatedTextWeb())
                
                recResponseWeb, recResponseTele = RelatedIntents.createRelatedPayload(dfRelated, df2)
                placeholder.append(recResponseWeb)
                placeholder.append(recResponseTele)
            
            reutrnChips = Chips.getReturnChipsPayload()
            reutrnChips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnMainChips())
            reutrnChips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnSubChips(mainTopic))
            
            placeholder.append(reutrnChips)

            # Write completed payload to files
            CustomIntents.write_file_json(os.getenv('intents').format(intentName[:80]), intentResponse)

        
            
