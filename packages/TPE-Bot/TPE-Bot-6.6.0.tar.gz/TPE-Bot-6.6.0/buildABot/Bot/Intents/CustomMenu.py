import json
import os

from buildABot.Bot.Intents.Type.Chips import Chips
from buildABot.Bot.Intents.Type.ButtonCard import ButtonCard
from buildABot.Bot.Intents.CustomResponse import CustomResponse
from buildABot.Bot.Intents.CustomTeleResponse import CustomTeleResponse
from buildABot.Bot.Intents.Usersays import Usersays

class CustomMenu(Chips, ButtonCard, CustomTeleResponse, Usersays):
    def write_file_json(QA_Data, data):
        with open(QA_Data, "w", encoding="utf-8") as jsonfile:
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
                    # payloads
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

    def getMenuPayload():
        return {
            "type": "4",
            "title": "",
            "payload": {
                "richContent": [
                    [
                        # button payloads
                    ]      
                ]
            }
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
    
    def getReturnSubChips(subTopic):
        return {
            "text": "Back to " + subTopic, #Back to ['Sub Topic']
            "image": {
                "src": {
                    "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/left-arrow-curved-black-symbol.png?alt=media&token=f0225665-02e7-459f-b8e9-1c19618a7234"
                }
            }
        }
    
    def getReturnMainChips():
        return {
            "text": "Back to Main Menu",
            "image": {
                "src": 
                {
                    "rawUrl": "https://firebasestorage.googleapis.com/v0/b/almgtbot.appspot.com/o/home%20(1).png?alt=media&token=c8b0db13-9aeb-48ab-ad44-6134a55049e2"
                }
            }
        }
    
    
    def createLearnMenu(listOfMainTopics):
        intent = CustomMenu.getIntentTemplate()
        placeholder = intent["responses"][0]["messages"]
        intent["name"] = 'Menu - Learn'
        intent['events'][0]['name'] = 'LEARNMENU'

        teleMenu = CustomTeleResponse.getTeleMenuKeyboard()
        messengerSelection = CustomMenu.getMenuPayload()

        for l in listOfMainTopics:
        
            # Telegram Selection - Main Topics
            texts = CustomTeleResponse.getTexts(l)
            telePlaceholder = teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"]
            telePlaceholder.append(texts)

            # Messenger Selection - Main Topics
            messPlaceholder = messengerSelection["payload"]["richContent"][0]
            messPlaceholder.append(ButtonCard.createButtonCard(text=l, event=l.replace(" ", ""), redirect=''))

        placeholder.append(teleMenu)
        placeholder.append(messengerSelection)

        # Write completed payload to files
        CustomMenu.write_file_json(os.getenv('learnMenu'), intent)
        Usersays.createMenuUserSays()
        

    def createSubMenu(df):
        for i in df["Main Topic"].unique():
            intent = CustomMenu.getIntentTemplate()
            placeholder = intent["responses"][0]["messages"]

            intent["name"] = i
            intent['events'][0]['name'] = i.replace(" ", "")
            
            teleMenu = CustomTeleResponse.getTeleMenuKeyboard()
            telePlaceholder = teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"]

            messengerSelection = CustomMenu.getMenuPayload()
            messPlaceholder = messengerSelection["payload"]["richContent"][0]

            reutrnChips = Chips.getReturnChipsPayload()

            dfTopic = df.loc[df["Main Topic"] == i]

            listOfSubTopics = dfTopic['Sub Topic'].unique()

            ## For 2 layer
            mainTopicName = dfTopic['Main Topic'].unique()[0]

            names = dfTopic['Name'].to_list()

            ## check
            for l in listOfSubTopics:
                if(l == ''): # 2 layer
                    for n in names:
                        # Telegram Selection
                        texts = CustomTeleResponse.getTexts(n)
                        telePlaceholder.append(texts)

                        # Messenger Selection
                        messPlaceholder.append(ButtonCard.createButtonCard(text=n, event=n.replace(" ", ""), redirect=''))

                else: #3 layer
                    # Telegram Selection - Sub Topic
                    texts = CustomTeleResponse.getTexts(l)
                    telePlaceholder.append(texts)

                    # Messenger Selection
                    messPlaceholder.append(ButtonCard.createButtonCard(text=l, event=l.replace(" ", ""), redirect=''))

            # Return to Main Menu                
            reutrnChips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnMainChips())

            # Return to Main Menu
            telePlaceholder.append(CustomTeleResponse.getTexts("Back to Main Menu"))

            placeholder.append(teleMenu)
            placeholder.append(messengerSelection)
            placeholder.append(reutrnChips)
                
            # Write completed payload to files
            CustomMenu.write_file_json(os.getenv('intents').format(i), intent)
            Usersays.createSubMenuUserSays(i)

    def createIntentsMenu(df):
        # 3 Layers Intents
        subTopics = df['Sub Topic'].unique()
        for s in subTopics:
            if(s != ''):
                intent = CustomMenu.getIntentTemplate()
                placeholder = intent["responses"][0]["messages"]

                teleMenu = CustomTeleResponse.getTeleMenuKeyboard()
                telePlaceholder = teleMenu["payload"]["telegram"]["reply_markup"]["keyboard"]

                messengerSelection = CustomMenu.getMenuPayload()
                messPlaceholder = messengerSelection["payload"]["richContent"][0]

                reutrnChips = Chips.getReturnChipsPayload()
                
                dfSubTopic = df.loc[df["Sub Topic"] == s]
                
                mainTopicName = dfSubTopic['Main Topic'].unique()[0]
                names = dfSubTopic['Name'].to_list()

                for n in names:
                    intent["name"] = mainTopicName + ' - ' + s
                    intent['events'][0]['name'] = s.replace(" ", "")

                    # Telegram Selection
                    texts = CustomTeleResponse.getTexts(n)
                    telePlaceholder.append(texts)

                    # Messenger Selection
                    messPlaceholder.append(ButtonCard.createButtonCard(text=n, event=n.replace(" ", ""), redirect=''))

                # Return to Sub Menu / Main Menu
                reutrnChips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnMainChips())
                reutrnChips["payload"]["richContent"][0][0]["options"].append(Chips.getReturnSubChips(mainTopicName))
            
                # Return to Main Menu
                telePlaceholder.append(CustomTeleResponse.getTexts("Back to Main Menu"))
                telePlaceholder.append(CustomTeleResponse.getTexts("Back to " + mainTopicName))


                placeholder.append(teleMenu)
                placeholder.append(messengerSelection)
                placeholder.append(reutrnChips)

                # Write completed payload to files
                CustomMenu.write_file_json(os.getenv('intentsTopic').format(mainTopicName, s), intent)
                Usersays.createIntentsUserSays(mainTopicName, s)