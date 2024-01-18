import pandas as pd
import json
import csv
import os
sentiments = ["Awesome", "Doing Fine", "It's been a rough week", "Still Hanging There"]
text_response = ["Yay, Keep it up! \n\nFeel free to check out the hot topics or explore the menu below! You can also ask me anything about the subject, I would love to help!", 
"That\u0027s good to hear! \n\nFeel free to check out the hot topics or explore the menu below! You can also ask me anything about the subject, I would love to help!", 
"Hang on there and don't give up! Tomorrow will be better. \n\nFeel free to check out the hot topics or explore the menu below! You can also ask me anything about the subject, I would love to help!", 
"Keep pushing and it will get better! \n\nFeel free to check out the hot topics or explore the menu below! You can also ask me anything about the subject, I would love to help!"]

class Worksheets_Learn():
  def __init__(self):
      pass
  
  def getIntentTemplate():
    return {
      "id": "b67e1e55-5fb5-4516-bb48-861e5be9334e",
      "name": "",
      "auto": True,
      "contexts": [
        "loggedIn",
        "sentiment"
      ],
      "responses": [
        {
          "resetContexts": False,
          "action": "",
          "affectedContexts": [
            {
              "name": "loggedIn",
              "lifespan": 1 #50
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
            {
              "type": "info",
              "title": "Yay, Keep it up! 🥳",
              "subtitle": "Feel free to check out the latest worksheets or explore the menu below! You can also ask me anything about the subject, I would love to help!",
              "image": {
                "src": {
                  "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/agenticon.png?alt=media&token=acfb8428-4e7e-4225-99dd-c4ec989530dc"
                }
              },
              "actionLink": ""
            },
            {
              "type": "0",
              "title": "",
              "textToSpeech": "",
              "lang": "en",
              "speech": [
                "Latest Worksheets:"
              ],
              "condition": ""
            },
            {
              "type": "4",
              "title": "",
              "payload": {
                "richContent": [
                  [
                    {
                      "icon": {
                        "type": "chevron_right"
                      },
                      "type": "button",
                      "link": "https://www.youtube.com/",
                      "text": "Worksheet 1"
                    },
                    {
                      "icon": {
                        "type": "chevron_right"
                      },
                      "link": "https://www.youtube.com/",
                      "type": "button",
                      "text": "Worksheet 2"
                    },
                    {
                      "link": "https://www.youtube.com/",
                      "text": "Worksheet 3",
                      "type": "button",
                      "icon": {
                        "type": "chevron_right"
                      }
                    }
                  ]
                ]
              },
              
              "textToSpeech": "",
              "lang": "en",
              "condition": ""
            },
            {
                "type": "0",
                "title": "",
                "textToSpeech": "",
                "lang": "en",
                "speech": [
                    "Current Hot Topics:"
                ],
                "condition": ""
            },
            {
                "type": "4",
                "title": "",
                "payload": {
                    "richContent": [
                        [
                            {
                                "options": [  # FAQ HERE
                                ],
                                "type": "chips"
                            }
                        ]
                    ]
                },
                "textToSpeech": "",
                "lang": "en",
                "condition": ""
            },
            {
              "type": "0",
              "title": "",
              "textToSpeech": "",
              "lang": "en",
              "speech": [
                "Menu:"
              ],
              "condition": ""
            },
            {
              "type": "4",
              "title": "",
              "payload": {
                "richContent": [
                  [
                     {
                      "icon": {
                        "type": "chevron_right"
                      },
                      "event": {
                        "name": "LEARNMENU",
                        "languageCode": "en",
                        "parameters": {}
                      },
                      "link": "",
                      "type": "button",
                      "text": "Learn & Explore"
                    }
                  ]
                ]
              },
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
      "fallbackIntent": False,
      "events": [],
      "conditionalResponses": [],
      "condition": "",
      "conditionalFollowupEvents": []
    }

  def getTrainingIntent():
    return {
      "id": "e5369794-5af3-4884-b591-94c704af567c",
      "data": [
        {
          "text": "Awesome 😄",
          "userDefined": False
        }
      ],
      "isTemplate": False,
      "count": 0,
      "lang": "en",
      "updated": 0
  }

  def getButtonPayload():
    return  {
      "type": "button",
      "icon": {
      "type": "chevron_right"
      },
      "link": "link1",
      "text": "Worksheet 1"
    }

  def getTeleInline():
    return {
        'postback': 'link',
        'text': 'Worksheet'
    }
  
  def getTeleKeyboard(text):
     return [
        {
          'text': text,
          'callback_data': text
        }
     ]
  
  def getTextPayload():
    return {
      "text": "suggested topic"
    }
  
  def write_file_json(QA_Data, data):
      with open(QA_Data, "w", encoding="utf-8") as jsonfile:
          json.dump(data, jsonfile, indent=4)

  def createWsIntent(self, dfWS):
    # Extract from SL Inputs the Worksheets Name & Links
    worksheets = list(filter(None,dfWS["Worksheets"]))
    links = list(filter(None,dfWS["Links"]))
    buttons, cards = [], []

    for i in range(len(worksheets)):
      button = Worksheets_Learn.getButtonPayload()
      button["text"] = worksheets[i]
      button["link"] = links[i]
      buttons.append(button)

      card = Worksheets_Learn.getTeleInline()
      card["text"] = worksheets[i]
      card["postback"] = links[i]
      cards.append(card)

    intent_payload = Worksheets_Learn.getIntentTemplate()
    #intent_payload["responses"][0]["messages"][1]["buttons"] = cards
    intent_payload["responses"][0]["messages"][2]["payload"]["richContent"][0] = buttons

    return intent_payload, cards

  def createHotTopics(self, df, intent_payload):
    hotTopicsIntents = []
    hotTopicsTele = []

    for x, rows in df.iterrows():
      intent_payload.pop("id", None)

      hotTopicTextPayload = Worksheets_Learn.getTextPayload()
      hotTopicTextPayload["text"] = rows["FAQ"] # Put in hot topics chosen into respective placeholder
      hotTopicsIntents.append(hotTopicTextPayload)

      inlineKeyboard = Worksheets_Learn.getTeleKeyboard(rows["FAQ"])
      hotTopicsTele.append(inlineKeyboard)

    # Place collated hot topics text paload into the intent template placeholder
    #intent_payload["responses"][0]["messages"][2]["buttons"] = hotTopicsTele
    intent_payload["responses"][0]["messages"][4]["payload"]["richContent"][0][0]["options"] = hotTopicsIntents

    return intent_payload, hotTopicsTele

  def createSentimentIntents(self, intent_payload):
    '''
    delete existing files to avoid being port into new deployment
    '''
    dir = os.getenv('wsIntents')
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        
    trainingIntent = Worksheets_Learn.getTrainingIntent()
  
    for i in range(4):
        intent_payload['name'] = "Login - Sentiment ({})".format(sentiments[i]) # Intent Name follows Criteria
        # intent_payload["responses"][0]["messages"][0]["speech"][0] = text_response[i]
        # intent_payload["responses"][0]["messages"][4]["speech"][0] = text_response[i]
        
        trainingIntent['data'][0]['text'] = sentiments[i]

        Worksheets_Learn.write_file_json(os.getenv('intentsLogin').format(sentiments[i]), intent_payload)
     
