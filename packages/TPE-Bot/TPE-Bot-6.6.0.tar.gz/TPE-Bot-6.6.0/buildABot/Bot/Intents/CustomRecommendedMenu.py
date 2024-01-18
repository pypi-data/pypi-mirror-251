import os
import json
import pandas as pd

from buildABot.Bot.Intents.CustomTeleResponse import CustomTeleResponse
from buildABot.Bot.Intents.CustomResponse import CustomResponse

from buildABot.Bot.Intents.Usersays import Usersays

from buildABot.Bot.Intents.Type.ButtonCard import ButtonCard
from buildABot.Bot.Intents.Type.Chips import Chips

class CustomRecommendedMenu(CustomTeleResponse, CustomResponse, ButtonCard, Usersays, Chips):
  def __init__(self) -> None:
    pass
  
  def write_file_json(file, data):
    with open(file, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)

  def getIntentTemplate():
    return {
        "id": "b6b5f5c1-04fb-4745-b8e1-1aa250d684ec",
        "name": "",
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
                "name": "loggedIn",
                "lifespan": 5
                }
            ],
            "parameters": [
               #getParameters()
              ],
            "messages": [
              #getPayload()
            ],
            "speech": []
            }
        ],
        "priority": 500000,
        "webhookUsed": False , #trueForMainMenu, falseForTopicalMenu
        "webhookForSlotFilling": False,
        "fallbackIntent": False,
        "events": [],
        "conditionalResponses": [],
        "condition": "",
        "conditionalFollowupEvents": []
    }
  
  def getResponse():
    return {
        "type": "4",
        "title": "",
        "payload": {
            "richContent": [
              [

              ]
            ]
        }
    }
  def getParameters():
    return {
        "id": "4986e1b6-aad9-49bb-ac4c-d0e3e7d6016e",
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
  
  def getMenuPayload():
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

  def getAssignmentIntentTemplate():
    return {
      "id": "0013b598-76db-416f-85c1-b7458d40609d",
      "name": "Menu - Recommended - Assignment 1",
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
              "name": "loggedIn",
              "lifespan": 5
            }
          ],
          "parameters": [
            {
              "id": "74af42c9-686b-430c-996f-b65f163e78e9",
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
              "type": "0",
              "title": "",
              "textToSpeech": "",
              "lang": "en",
              "condition": ""
            }
          ],
          "speech": []
        }
      ],
      "priority": 500000,
      "webhookUsed": True,
      "webhookForSlotFilling": False,
      "fallbackIntent": False,
      "events": [],
      "conditionalResponses": [],
      "condition": "",
      "conditionalFollowupEvents": []
    }
  
  def getInfo(resultFile, rubrics):
    # Extract topics tested in assessment from Rubrics
    sheets = pd.ExcelFile(resultFile).sheet_names # list all sheets in the file
    assignments = sheets[1:] # get list of assignments

    criteria = list(rubrics['Criteria'])

    subTopic = list(rubrics['Sub Topic'])

    counts = rubrics.groupby(['Assessment']).count()

    return assignments, criteria, subTopic, counts
  
  def createRecommendedMainMenu(listOfAssignments):
    intent = CustomRecommendedMenu.getIntentTemplate()

    # Name
    intent["name"] = 'Menu - Recommended'

    placeholder = intent["responses"][0]["messages"]

    teleMenu = CustomTeleResponse.getTeleMenuKeyboard()
    webMenu = CustomRecommendedMenu.getResponse()

    for a in listOfAssignments:
      # Telegram
      teleMenu["title"] = "Available Recommended Menu:"
      teleMenu["payload"]["telegram"]["text"] = 'Available Recommended Menu:'
      teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"].append(CustomTeleResponse.getTexts(a))

      # Web
      webMenu["payload"]["richContent"][0].append(ButtonCard.createButtonCard(text=a, event=a.replace(" ", ""), redirect=''))
    
    placeholder.append(teleMenu)
    placeholder.append(webMenu)

    CustomRecommendedMenu.write_file_json(os.getenv('intentsReco'), intent)
    Usersays.createRecoMenuUserSays()

    intent["name"] = 'Login - Results'
    intent['events'].append({
      "name": "RECOMENU"
    })

    CustomRecommendedMenu.write_file_json(os.getenv('intentsLoginResults'), intent)
    Usersays.createResultsMenuUserSays()

  def createRecommendedAssignmentMenu(listOfAssignments):
    intent = CustomRecommendedMenu.getAssignmentIntentTemplate()

    for l in listOfAssignments:
        name = 'Menu - Recommended - {}'.format(l)

        # Name
        intent['name'] = name
        intent['events'] = [{
            "name": "" + str(l.replace(" ", ""))
        }]

        # # Parameters
        # intent["responses"][0]["parameters"] = CustomRecommendedMenu.getParameters()

        # # Webhook
        # intent["webhookUsed"] = True

        CustomRecommendedMenu.write_file_json(os.getenv('intentsRecommended').format(name), intent)
        Usersays.createCustomUserSays(l, os.getenv('intentsRecommendedUsersays').format(name))

  def createRecommendedCriteriaMenu(rubrics):
    listOfAssignments = rubrics['Assessment'].unique()

    for a in listOfAssignments:
      df = rubrics.loc[rubrics['Assessment'] == a]

      listOfCriteria = df['Criteria'].to_list()
      listOfSubTopic = df['Sub Topic'].to_list()

      CustomRecommendedMenu.getCriteriaMenu(a, listOfCriteria, listOfSubTopic)
  
  def getCriteriaMenu(a, listOfCriteria, listOfSubTopic):

    for i in range(len(listOfSubTopic)):
      intent = CustomRecommendedMenu.getIntentTemplate()
      teleMenu = CustomTeleResponse.getTeleMenuKeyboard()
      webMenu = CustomRecommendedMenu.getMenuPayload()
      chips = CustomRecommendedMenu.getMenuPayload()

      criteria = listOfCriteria[i]
      subTopic = listOfSubTopic[i]
      subTopicsName = subTopic.split(', ')

      # Name
      name = "Menu - Recommended - {} - {}".format(a, criteria)
      intent['name'] = name
      
      for s in subTopicsName:
        # Telegram
        teleMenu["payload"]["telegram"]["text"] = 'Pick a topic:'
        teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"].append(CustomTeleResponse.getTexts(s))
        
        # Web
        webMenu["payload"]["richContent"][0].append(ButtonCard.createButtonCard(text=s, event=s.replace(" ", ""), redirect=''))

      # Return To Chips
      chips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnRecommendedChips())
      chips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnMainChips())

      # Return to Main Menu
      teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"].append(CustomTeleResponse.getTexts("Back to Main Menu"))
      teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"].append(CustomTeleResponse.getTexts("Back to Recommended Menu"))
      
      placeholder = intent["responses"][0]["messages"]
      placeholder.append(teleMenu)
      placeholder.append(webMenu)
      placeholder.append(chips)

      CustomRecommendedMenu.write_file_json(os.getenv('intentsRecommended').format(name), intent)
      Usersays.createRecoUserSays(a, criteria, name)






