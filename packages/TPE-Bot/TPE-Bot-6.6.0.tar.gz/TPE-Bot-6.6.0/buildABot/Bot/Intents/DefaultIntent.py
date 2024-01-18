import pandas as pd
import os
import json
from .CustomTeleResponse import CustomTeleResponse
class DefaultIntent():

    def __init__(self) -> None:
        pass

    def write_file_json(QA_Data, data):
      with open(QA_Data, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)

    def getWelcomeIntentTemplate():
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
    
    def getFallbackIntentTemplate():
        return {
            "id": "b3d275b9-bbc5-47ef-9b1d-232cd944cf38",
            "name": "Default Fallback Intent",
            "auto": True,
            "contexts": [],
            "responses": [
            {
                "resetContexts": False,
                "action": "",
                "affectedContexts": [
                {
                    "name": "awaiting_login",
                    "lifespan": 3
                }
                ],
                "parameters": [],
                "messages": [
                {
                    "type": "0",
                    "title": "",
                    "textToSpeech": "",
                    "lang": "en",
                    "speech": [
                    "Hi there, welcome back to the chatroom!\n❗ Login ID \u003d last 4 digits + character of admin number\n(E.g. 1234567A, id \u003d 4567A)\n\nPlease login with your unique ID before exploring the bot, thank you! 😊"
                    ],
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
    
    def getFallbackText():
       return {
          "type": "0",
          "platform": "telegram",
          "title": "",
          "textToSpeech": "",
          "lang": "en",
          "speech": [
            "Welcome back, Type /Start to start chatting with me!"
          ],
          "condition": ""
        }


    def getCheckSubmission():
        return {
          "type": "1",
          "platform": "telegram",
          "title": "Recent Submissions",
          "buttons": [
              {
                "postback": "💡 Check Submission",
                "text": "Check Submission"
              }
          ],
          "textToSpeech": "",
          "lang": "en",
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
          "type": "4",
          "platform": "telegram",
          "title": "",
          "payload": {
            "telegram": {
              "text": "Hot Topics:",
              "reply_markup": {
                "inline_keyboard": hotTopicsArray
              }
            }
          }
        }


    def getTeleLearnMenu():
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
    
    def getTeleRecoMenu():
        return {
          "type": "1",
          "platform": "telegram",
          "title": "Menu:",
          "buttons": [
              {
                "postback": "Learn \u0026 Explore",
                "text": "Learn \u0026 Explore"
              },
              {
                "postback": "Results \u0026 Recommendations",
                "text": "Results \u0026 Recommendations"
              }
          ],
          "textToSpeech": "",
          "lang": "en",
          "condition": ""
        }


    def createWelcomeIntent(worksheetArray, hotTopicsArray):
        intent = DefaultIntent.getWelcomeIntentTemplate()
        payloadPlaceholder = intent["responses"][0]["messages"]

        #payloadPlaceholder.append(DefaultIntent.getWebAppResponse())

        payloadPlaceholder.append(DefaultIntent.getTeleText())
        
        payloadPlaceholder.append(DefaultIntent.getCheckSubmission())

        payloadPlaceholder.append(DefaultIntent.getTeleWorksheet(worksheetArray))

        payloadPlaceholder.append(DefaultIntent.getTeleHotTopics(hotTopicsArray))

        payloadPlaceholder.append(DefaultIntent.getTeleLearnMenu())
        
        DefaultIntent.write_file_json(os.getenv('DefaultWelcomeIntent'), intent)

    def createRecoWelcomeIntent(worksheetArray, hotTopicsArray):
        intent = DefaultIntent.getWelcomeIntentTemplate()
        payloadPlaceholder = intent["responses"][0]["messages"]

        payloadPlaceholder.append(DefaultIntent.getTeleText())

        payloadPlaceholder.append(DefaultIntent.getCheckSubmission())

        payloadPlaceholder.append(DefaultIntent.getTeleWorksheet(worksheetArray))

        payloadPlaceholder.append(DefaultIntent.getTeleHotTopics(hotTopicsArray))

        '''
        Hot Topics & Menu as In-line Keyboard
        '''
        # keyboard = DefaultIntent.getTeleHotTopics()
        # keyboard["payload"]["telegram"]["reply_markup"]["keyboard"] = hotTopicsArray
        
        # payloadPlaceholder.append(keyboard)
        payloadPlaceholder.append(DefaultIntent.getTeleRecoMenu())

        DefaultIntent.write_file_json(os.getenv('DefaultWelcomeIntentReco'), intent)


    def createFallbackIntent(worksheetArray, hotTopicsArray):
      intent = DefaultIntent.getFallbackIntentTemplate()
      payloadPlaceholder = intent["responses"][0]["messages"]

      payloadPlaceholder.append(DefaultIntent.getFallbackText())
      
      # payloadPlaceholder.append(DefaultIntent.getCheckSubmission())

      # payloadPlaceholder.append(DefaultIntent.getTeleWorksheet(worksheetArray))

      # payloadPlaceholder.append(DefaultIntent.getTeleHotTopics(hotTopicsArray))

      # payloadPlaceholder.append(DefaultIntent.getTeleLearnMenu())
      
      DefaultIntent.write_file_json(os.getenv('DefaultFallbackIntent'), intent)

    def createRecoFallbackIntent(worksheetArray, hotTopicsArray):
      intent = DefaultIntent.getFallbackIntentTemplate()
      payloadPlaceholder = intent["responses"][0]["messages"]

      payloadPlaceholder.append(DefaultIntent.getFallbackText())
      
      # payloadPlaceholder.append(DefaultIntent.getCheckSubmission())

      # payloadPlaceholder.append(DefaultIntent.getTeleWorksheet(worksheetArray))

      # payloadPlaceholder.append(DefaultIntent.getTeleHotTopics(hotTopicsArray))

      # payloadPlaceholder.append(DefaultIntent.getTeleRecoMenu())
      
      DefaultIntent.write_file_json(os.getenv('DefaultFallbackIntentReco'), intent)
  