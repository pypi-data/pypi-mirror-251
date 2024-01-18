import pandas as pd
import json
import os
import pkgutil

class FallbackSocialTag():
  def __init__(self) -> None:
      pass
  def getFallbackIntent():
    return {
      "id": "57bedbfc-4c92-4817-9f80-fafc167c38a0",
      "name": "Login - Fallback - no",
      "auto": True,
      "contexts": [
        "loggedIn"
      ],
      "responses": [
        {
          "resetContexts": False,
          "action": "",
          "affectedContexts": [
            {
              "name": "Login-Fallback-followup",
              "lifespan": 1
            }
          ],
          "parameters": [],
          "messages": [
            {
              "type": "0",
              "platform": "telegram",
              "title": "",
              "textToSpeech": "",
              "lang": "en",
              "speech": [ ],
              "condition": ""
            },
            {
              "type": "1",
              "platform": "telegram",
              "title": "Do you know the answer?",
              "buttons": [
                {
                  "postback": "Yes",
                  "text": "Yes"
                },
                {
                  "postback": "No",
                  "text": "No"
                }
              ],
              "textToSpeech": "",
              "lang": "en",
              "condition": ""
            }
          ],
          "speech": []
        }
      ],
      "priority": 500000,
      "webhookUsed": False,
      "webhookForSlotFilling": False,
      "fallbackIntent": True,
      "events": [],
      "conditionalResponses": [],
      "condition": "",
      "conditionalFollowupEvents": []
    }
  def createSocialTagFallbackNo(df):
    intent = FallbackSocialTag.getFallbackIntent()
    msg = []
    intent['name'] = 'Login - Fallback - no'
    intent['parentId'] = "57bedbfc-4c92-4817-9f80-fafc167c38a0"
    intent["rootParentId"] = "57bedbfc-4c92-4817-9f80-fafc167c38a0"
    
    intent['contexts'].append("Login-Fallback-followup")
    intent['responses'][0]['action'] = 'Login-Fallback.Login-Fallback-no'
    intent['responses'][0]['affectedContexts'].append({
          "name": "loggedIn",
          "lifespan": 1
        })

    for index, row in df.iterrows():
      msg.append('Hmm... @' + row["Telegram ID"] + " What about you?")

    intent["responses"][0]["messages"][0]["speech"] = msg
    return intent
  
  def createSocialTagStrings(df):
    intent = FallbackSocialTag.getFallbackIntent()
    msg = []

    for index, row in df.iterrows():
      msg.append('@' + row["Telegram ID"] + " do you know the answer?")

    return msg