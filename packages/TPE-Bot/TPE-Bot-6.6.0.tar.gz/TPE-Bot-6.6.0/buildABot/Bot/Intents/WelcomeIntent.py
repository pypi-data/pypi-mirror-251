import pandas as pd
import os
import json

class WelcomeIntent():

    def __init__(self) -> None:
        pass

    def write_file_json(QA_Data, data):
      with open(QA_Data, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)

    def getIntentTemplate():
        return {
        "id": "b67e1e55-5fb5-4516-bb48-861e5be9334e",
        "name": "Default Welcome Intent - Telegram",
        "auto": True,
        "contexts": [],
        "responses": [
            {
            "resetContexts": False,
            "action": "DefaultWelcomeIntent",
            "affectedContexts": [
                {
                    "name": "loggedIn",
                    "lifespan": 50
                }
            ],
            "parameters": [],
            "messages": [
                
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
            "name": "TELEGRAM_WELCOME"
          }
        ],
        "conditionalResponses": [],
        "condition": "",
        "conditionalFollowupEvents": []
        }

    # def getWebAppResponse():
    #     return {
    #       "type": "4",
    #       "title": "",
    #       "payload": {
    #         "richContent": [
    #           [
    #             {
    #               "image": {
    #                 "src": {
    #                   "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/agenticon.png?alt\u003dmedia\u0026token\u003dacfb8428-4e7e-4225-99dd-c4ec989530dc"
    #                 }
    #               },
    #               "subtitle": "Here\u0027s a tip: \n\n Your login ID \u003d last 5 alphanumeric characters of your admin number. \n\n E.g. If your admin number is 1234567A, key in 4567A.",
    #               "actionLink": "",
    #               "title": "To start, key in your login ID in the chat window below 👇🏼.",
    #               "type": "info"
    #             }
    #           ]
    #         ]
    #       },
    #       "textToSpeech": "",
    #       "lang": "en",
    #       "condition": ""
    #     }
    
    def getTeleText():
        return {
          "type": "0",
          "platform": "telegram",
          "title": "",
          "textToSpeech": "",
          "lang": "en",
          "speech": [
            "👋🏼 Hi there, Welcome to the chatroom! I\u0027m your learning assistant. \n\nCheck out the latest worksheets, hot topics or explore the menu below! 👇🏼 \n\nYou can also ask me anything about the subject, I would love to help! 😍"
          ],
          "condition": ""
        }
    
    def getTeleWorksheet(worksheetArray):
        return {
          "type": "1",
          "platform": "telegram",
          "title": "Lastest Worksheets:",
          "buttons": worksheetArray,
          "textToSpeech": "",
          "lang": "en",
          "condition": ""
        }
    
    def getTeleHotTopics(hotTopicsArray):
        return {
                "type": "1",
                "platform": "telegram",
                "title": "Current Hot Topics:",
                "buttons": hotTopicsArray,
                "textToSpeech": "",
                "lang": "en",
                "condition": ""
            }
    
    def getTeleMenu():
        return {
          "type": "1",
          "platform": "telegram",
          "title": "Menu:",
          "buttons": [
            {
              "postback": "Learn \u0026 Explore",
              "text": "Learn \u0026 Explore"
            }
          ],
          "textToSpeech": "",
          "lang": "en",
          "condition": ""
        }
    
    def createWelcomeIntent(worksheetArray, hotTopicsArray):
        intent = WelcomeIntent.getIntentTemplate()
        payloadPlaceholder = intent["responses"][0]["messages"]

        #payloadPlaceholder.append(WelcomeIntent.getWebAppResponse())

        payloadPlaceholder.append(WelcomeIntent.getTeleText())

        payloadPlaceholder.append(WelcomeIntent.getTeleWorksheet(worksheetArray))

        payloadPlaceholder.append(WelcomeIntent.getTeleHotTopics(hotTopicsArray))

        payloadPlaceholder.append(WelcomeIntent.getTeleMenu())

        WelcomeIntent.write_file_json(os.getenv('DefaultWelcomeIntent'), intent)
